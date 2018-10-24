# <<Description Here>>
#
# Module : $File$
# Author : $Author$
# Version: $Version$
# Status : $Status$
#
# Copyright (C) 2002 Brian Hammond. All Rights Reserved

import math, time 

import observer  # Homebrew observer pattern impl.

import pytrace.config as config
from   pytrace.color    import *
from   pytrace.material import Material, DEFAULT_MATERIAL

class RayTracer(object):
  class RowTracedSubject(observer.Subject):
    """
    Subject that notifies attached observers when a row of the image has been raytraced.
    An example observer might progressively update the final display as each new row is completed.
    row - Row most recently traced (int); [0, image height)
    total_rows - Total number of rows (= image height) 
    """

  def __init__(self, world, view):
    assert len(view.img_size)==2 and view.img_size[0] > 0 and view.img_size[1] > 0
    self.view = view
    self._world = world
    self.row_traced_subject = RayTracer.RowTracedSubject()
    self.doshadows = True
    self.stats = { 
      'shadow tests':0,
      'shadow tests failed':0,
      'pixels': self.view.img_size[0] * self.view.img_size[1],
      'samples':0,
      'traces':0,
      'reflections':0,
      'refractions':0
    }

  def trace(self):
    """
    trace() -> Numeric array (shape: w,h,3; type:UInt8).
    Raytrace world from view of active camera.
    Returns 24-bit color image buffer.
    """
    assert self._world is not None
    assert self._world.active_camera is not None

    iw, ih = self.view.img_size[0], self.view.img_size[1]
    
    # TODO Threading is actually SLOWER than single-threaded!!

    if config.num_threads > 0:
      import threading, Queue, time
      class TracerThread(threading.Thread):
        work_done = {}
        def __init__(self, tid, ray_queue, hit_queue, tracer):
          threading.Thread.__init__(self)
          self.ray_queue = ray_queue
          self.hit_queue = hit_queue
          self.tracer = tracer
          self.tid = tid
          TracerThread.work_done[self.tid] = 0
        def run(self):
          while True:
            try:
              token = self.ray_queue.get(True, 0.2)
              if not token:
                break
              x, y, Ro, Rd = token
              self.hit_queue.put((x, y, self.tracer._trace(Ro, Rd)))
              TracerThread.work_done[self.tid] += 1
            except Queue.Empty:
              break
          
      class ShaderThread(threading.Thread):
        work_done={}
        def __init__(self, tid, hit_queue, tracer):
          threading.Thread.__init__(self)
          self.tid = tid
          self.hit_queue = hit_queue
          self.tracer = tracer
          ShaderThread.work_done[self.tid]=0
        def run(self):
          while True:
            try:
              token = self.hit_queue.get(True, 0.2)
              if not token:
                break
              x, y, hit = token
              c = self.tracer.shade(hit)
              self.tracer.view.screen.set_at((x, y), 
                (int(c[0]*255.0), int(c[1]*255), int(c[2]*255))) 
              ShaderThread.work_done[self.tid] += 1
            except Queue.Empty:
              break
      
      import pygame
      class DisplayUpdateThread(threading.Thread):
        def __init__(self, tracer, hit_queue, threshold, Hz=0.5):
          threading.Thread.__init__(self)
          self.tracer = tracer
          self.hit_queue = hit_queue
          self.threshold = threshold
          self.stop = False
          self.Hz = Hz
        def run(self):
          while not self.stop:
            self.tracer.row_traced_subject.notify()
            pygame.display.set_caption("%s %s" % (primary_ray_queue.qsize(), hit_queue.qsize()))
            time.sleep(self.Hz)
          print "display thread asked to stop"
          self.tracer.row_traced_subject.notify()

      primary_ray_queue = Queue.Queue()
      hit_queue = Queue.Queue()

      # Start the tracer threads.
      
      tracer_threads = []
      for i in range(config.num_threads):
        if config.verbose:
          print "Starting tracer thread %d of %d ..." % (i+1, config.num_threads)
        wt=TracerThread(i, primary_ray_queue, hit_queue, self)
        wt.start()
        tracer_threads.append(wt)

      # Start the tracer threads.
      
      shader_threads = []
      for i in range(config.num_threads*2):
        if config.verbose:
          print "Starting shader thread %d of %d ..." % (i+1, config.num_threads)
        st=ShaderThread(i, hit_queue, self)
        st.start()
        shader_threads.append(st)

      # Start the display thread.  Update once every row is complete.

      if config.verbose:
        print "Creating display thread ..."
      dt=DisplayUpdateThread(self, hit_queue, self.view.img_size[0])
      dt.start()

      # Generate primary rays and place into a work queue.

      if config.verbose:
        print "Generating work for tracer threads ..."

      start = 0
      for fields in range(2):
        for y in range(start, ih, 2):
          for x in range(iw):
            Ro, Rd = self._world.active_camera.primary_ray(x, y)
            primary_ray_queue.put((x, y, Ro, Rd))
        start=1
        
      # Wait for all the work to be done.

      if config.verbose:
        print "Work generated. Waiting for all threads to complete work ..."

      while hit_queue.qsize() > 0:
        time.sleep(0.2)

      if config.verbose:
        print "threads have finished work."

      # Last update

      self.row_traced_subject.notify()

      # Destroy threads.
  
      if config.verbose:
        print "killing tracer threads..."
     
      for t in tracer_threads:
        primary_ray_queue.put(None)
        t.join()
        
      if config.verbose:
        print "killing shader threads..."
     
      for s in shader_threads:
        hit_queue.put(None)
        s.join()

      if config.verbose:
        print "killing display thread..."
     
      dt.stop=True
      dt.join()

      if config.verbose:
        for k in TracerThread.work_done:
          print "Tracer thread %d traced %d samples" % (k, TracerThread.work_done[k])
        for k in ShaderThread.work_done:
          print "Shader thread %d shaded %d hits" % (k, ShaderThread.work_done[k])

    else:
      # Threading not enabled.

      for start in range(2):
        for y in range(start,ih,2):
          for x in range(iw):
            Ro, Rd = self._world.active_camera.primary_ray(x, y)
            self.stats['samples'] += 1
            if __debug__:
              print "\num_primary_raysel (%3d,%3d) %s %s" % (x,y,Ro,Rd)
            hit = self._trace(Ro, Rd)
            c = self.shade(hit)
            self.view.screen.set_at((x, y), 
              (int(c[0]*255.0), int(c[1]*255), int(c[2]*255))) 
          self.row_traced_subject.notify()
      self.row_traced_subject.notify()

  def _trace(self, Ro, Rd, exact = True):
    "Find closest intersecting object in world along ray (Ro,Rd)"

    self.stats['traces'] += 1
    
    closest = None

    # TODO clearly simplistic, ends up testing the ray against every primitive.
    # TODO even view frustum culling would be great. something, please! 

    for p in self._world.primitives:
      hit = p.intersect(Ro, Rd)

      if hit is None: 
        continue
      
      if closest is None:
        closest = hit
      elif hit['t'] > 0 and hit['t'] < closest['t']:
        closest = hit
    
    return closest

  def _shadow(self, Ro, Rd, P):
    """
    Determine shadow factor of ray (Ro,Rd) trying to 'see' point P.
    Returns 1.0 if Ro can see P, 0.0 if completely in shadow, or a
    value in [0,1) if in the penumbra of a light source (partially 
    shadowed).
    """
   
    # TODO currently only testing all or nothing
   
    self.stats['shadow tests'] += 1   
    closest = self._trace(Ro, Rd)
    
    if closest is None:
      return 1.0

    # If ray hit something, the closest such hit is returned.
    # If it is further away than P then P is visible to Ro.
    
    dist_isect = closest['P'] - Ro
    dist_p = P - Ro
    
    if dist_p * dist_p < dist_isect * dist_isect:
      return 1.0
    
    self.stats['shadow tests failed'] += 1
    return 0.0

  def shade(self, hit, level=0, weight=1.0):
    """
    Determine illumination at primitive hit['prim']'s surface point hit['P'] 
    which has normal hit['N'] at point hit['P'].  hit['I'] is the incident 
    ray to the surface point hit['P']
    """

    if hit is None:
      return self._world.bgcolor
    
    I, P, N, mat = hit['I'], hit['P'], hit['N'], hit['prim'].material
    V = -I
    
    if mat is None:
      mat = DEFAULT_MATERIAL
    
    # Initially no illumination; this should start out at black but 
    # standard raytracing is not a real global illumination algorithm.
    # The algorithm thus compensates with a global ambient term.
    
    Iamb = RGB(self._world.ambient[0] * mat.diffuse[0], 
               self._world.ambient[1] * mat.diffuse[1], 
               self._world.ambient[2] * mat.diffuse[2])
    
    # Determine contribution of each light (Light "j"; Lj) in world to 
    # P's illumination.

# TODO These eqs don't take the light color into account!!

    Ilights = RGB(0,0,0)
    
    for Lj in self._world.lights:
      # shadow factor (0=full shadow, 1=none).

      Lorig = Lj.pos - P
      L = Lorig.normalize()
      
      if self.doshadows:
        # TODO this is a fudge factor (1.00001) in order to avoid
        # TODO self-intersections.  Need a more robust method.
        
        S = self._shadow(Ro = P + L * 1.00001, Rd = L, P = Lj.pos)
        
        if S == 0.0:
          continue
      else:
        S = 1.0
        
      # diffuse component
      
      NdotL = N*L
      
      if NdotL < 0.0:
        Idiff = RGB(0,0,0)
      else:
        Idiff = mat.Kd * mat.diffuse * NdotL

      # specular component
      
      H = (L + V) * 0.5
      Ispec = mat.Ks * mat.specular * math.pow(N * H, mat.shininess)
      
      # add to total illumination by all light sources.
      
      Ilights = Ilights + S*(Idiff + Ispec)

    Irefl = RGB(0,0,0) 
    Itrans = RGB(0,0,0)
    
    if level + 1 < config.max_depth:
      # Recurse on reflection if any.

      if mat.Ks * weight > config.min_weight:
        self.stats['reflections'] += 1
      
        # Reflect incident ray about normal.  Start ray at current
        # intersection point and fire it. If it hits anything, shade
        # it, recursively. If it won't contribute much to the final
        # illumination, stop. Stop also when we've reached an arbitrary
        # depth.

        R = I - 2.0 * (N * I) * N
       
        # TODO -- If we just use P for the new ray origin, we get lots of
        # TODO    artifacts as the point may intersect with the surface we're
        # TODO    already on!  Need a better method to move the point out beyond
        # TODO    the intersected surface.
       
        refl_hit = self._trace(P+N*1.0001, R)
        
        if refl_hit is not None:
          Irefl = mat.Ks * self.shade(hit=refl_hit, level=level+1, weight=mat.Ks * weight)
        else:
          Irefl = mat.Ks * self._world.bgcolor 
    
        if __debug__:
          print "level=%d weight=%.2f" % (level, weight)
          #print "  I=%s P=%s N=%s R=%s" % (I,P,N,R)

      if mat.Kt * weight > config.min_weight:
        self.stats['refractions'] += 1
        
        # TODO
        Itrans = RGB(0,0,0)

    c = Iamb + Ilights + Irefl + Itrans
    
    if __debug__:
      print "  Amb%s+Lights%s+Refl%s+Trans%s=%s" % (Iamb, Ilights, Irefl, Itrans, c)
      
    # Scale (don't clamp!) colors with components > 1.
    # E.g. if we'd clamp 2.5,1.5,.5 which is bright orange, we'd end up
    # with 1.,1.,.5 which is yellow.  We should instead scale all comps
    # by 1/2.5 to maintain the bright orange, but in the correct range.

    max_comp = c[0]
    if c[1] > max_comp: max_comp = c[1]
    if c[2] > max_comp: max_comp = c[2]
    if max_comp > 1.0:  c *= 1.0 / max_comp

    return c

  #def get_pixels(self):
  #  return self._pixels
  
  #pixels = property(get_pixels)

  def get_image_size(self):
    return self.view.img_size
  
  image_size = property(get_image_size)

  def dump_stats(self, file=None):
    "Print stats to file or stdout if None"

    # TODO just to stdout right now

    print "\nstatistics:\n"

    for s in self.stats:
      print "%-30s: %s" % (s, self.stats[s])
    
    prim_stats = {}
    for p in self._world.primitives:
      k=type(p).__name__
      prim_stats[k]=(p.tests-p.tests_failed, p.tests,
        (p.tests-p.tests_failed) / float(p.tests) * 100.0)

    for kv in prim_stats.keys():
      print "%-30s: %d of %d passed (%4.2f%%)" % \
        (kv+" tests", prim_stats[kv][0], prim_stats[kv][1], prim_stats[kv][2])

    print ""
