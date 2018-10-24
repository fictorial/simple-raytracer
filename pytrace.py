#!/usr/bin/env pythonw
# PyTrace - A raytracer in Python
# Brian Hammond http://brianhammond.com
# Summer, 2003

# TODO
# - Camera model messed up wrt focal length
# - disallow focal length <= 0
# - eye ray generator incorrect -- 
# - Viewport WRONG -- Why is -V*1/2fh needed instead of +???
# - matrices for camera orientation (see http://www.makegames.com/3drotation/3dsrce.html)

import os.path, sys, math, time, optparse

import observer

class TracerApp(observer.Observer):
  NAME = "PyTrace"
  VERSION = "0.1"
  
  def __init__(self, world, img_size, farm):
    pygame.init()
    pygame.event.set_blocked(range(NUMEVENTS))
    pygame.event.set_allowed([KEYDOWN, MOUSEMOTION, MOUSEBUTTONDOWN, QUIT])
    self.view = TracerView(img_size)
    self.tracer = RayTracer(world, self.view)
    self.tracer.row_traced_subject.attach(self)
    self.tracer.row_traced_subject.attach(self.view)
    self.farm = farm
    self._status('Ready')

  def trace(self, output_path):
    start = time.clock()
    self.tracer.trace()
    elapsed = time.clock() - start
    if output_path is not None:
      if output_path[-4:] != '.tga':
        print "WARNING! non .tga extension in output path"
      pygame.image.save(self.view.screen, output_path)
      print "%s written" % output_path
    return elapsed

  def subject_changed(self, subject):
    "Called when another row has been raytraced"
    self._check_quit()

  def _check_quit(self):
    event_list = pygame.event.get()
    for event in event_list:
      if event.type in (QUIT,MOUSEBUTTONDOWN) or (event.type == KEYDOWN and event.key == K_ESCAPE):
        import sys
        sys.exit(1)

  def wait_quit(self):
    while True:
      self._check_quit()
      time.sleep(0.5)
  
  def _status(self, status):
    self.status = status
    pygame.display.set_caption("%s - %s" % (TracerApp.NAME, status))

class TracerView(observer.Observer):
  def __init__(self, img_size):
    self.img_size = img_size
    self.screen = pygame.display.set_mode(img_size, DOUBLEBUF)
    self.magbox = pygame.Surface((40,40))
  def subject_changed(self, subject):
    "Called when another row has been raytraced"
    pygame.display.flip()


class RenderFarm(object):
  "Defines a set of hosts that help in raytracing"
  # TODO

def parse_farm_cfg(path):
  # TODO 
  return None

if __name__ == "__main__":
  optparser = optparse.OptionParser(usage="%prog --world=WORLD [options]")
  optparser.add_option("-V", "--version", action="store_true",
    default=False, dest="showversion", 
    help="print version and quit.")
  optparser.add_option("-W", "--width", type="int", 
    dest="width", default=400, metavar="WIDTH",
    help="width of output image")
  optparser.add_option("-H", "--height", type="int", 
    dest="height", default=300, metavar="HEIGHT",
    help="height of output image")
  optparser.add_option("-O", "--out", dest="output",
    metavar="FILE", default="output.tga",
    help="path to output image. Output in Targa (tga) format") 
  optparser.add_option("-I", "--world", type="string", 
    dest="worldmodule",
    help="path to input (hence -I) Python file defining world (e.g. myworlds.testworld)")
  optparser.add_option("-q", "--quit", action="store_true",
    dest="quitatend", default=False, 
    help="do not pause when image is completed, just quit")
  optparser.add_option("--renderfarm", type="string",
    dest="farmcfg", metavar="FARMCFG",
    help="path to config file for defining a render-farm")
  optparser.add_option("-v", "--verbose", action="store_true",
    default=False, dest="verbose", 
    help="verbose output")
  optparser.add_option("--profile", action="store_true",
    default=False, dest="profile", 
    help="profile execution. stats written to stdout.")
  optparser.add_option("--nopsyco", action="store_true",
    default=False, dest="nopsyco", 
    help="do not attempt to load psyco")
  optparser.add_option("--noshadows", action="store_true",
    default=False, dest="noshadows", 
    help="do not calculate shadows.")
  optparser.add_option("--maxdepth", type="int",
    default=5, dest="max_depth", 
    help="Recursion depth limit for shading. Default: 5")
  optparser.add_option("--threads", type="int",
    default=12, dest="num_threads", 
    help="Number of worker threads to use in tracing primary rays. Default: 12")
    
  options, args = optparser.parse_args()

  if options.showversion:
    print "%s v%s" % (TracerApp.NAME, TracerApp.VERSION)
    sys.exit(0)

  img_size = options.width, options.height
  if img_size[0] <= 0 or img_size[1] <= 0:
    optparser.error("invalid output image resolution")
 
  if options.worldmodule is None:
    optparser.error("no world module specified. use --world.")

  if not options.nopsyco:
    try:
      import psyco
      psyco.full()
    except ImportError:
      print "WARNING: psyco not installed - performance will suffer"
    
  try:
    import pygame
    from   pygame.locals             import *
    from   cgtypes                   import *
    from   pytrace.color             import RGB, RGBA
    import pytrace.config
    from   pytrace.camera            import Camera
    from   pytrace.material          import Material
    from   pytrace.raytracer         import RayTracer
    from   pytrace.world             import World
    from   pytrace.light             import Light
  except ImportError, err:
    print "failed to load required module. %s" % (err)
    sys.exit(2)

  pytrace.config.max_depth = options.max_depth
  pytrace.config.num_threads = options.num_threads
  pytrace.config.verbose = options.verbose

  if options.verbose:
    print "output image: %s (%d x %d)" % \
    (options.output, options.width, options.height)
 
  if options.verbose:
    print "loading world from module %s" % options.worldmodule

  # TODO need to put make_world under restricted execution mode... 
  # TODO don't need world-definitions doing something dirty.

  # TODO psyco and rexec are mutually exclusive.

  #import rexec
  #r = rexec.RExec()

  try:
    #module = r.r_import(options.worldmodule, globals(), locals(), ['make_world'])
    module = __import__(options.worldmodule, globals(), locals(), ['make_world'])
  except ImportError, err:
    print "failed to import world module: %s: %s" % (options.worldmodule, err)
    sys.exit(1)
    
  if options.verbose:
    print "module loaded. calling make_world()..."
    
  try:
    world = module.make_world(img_size)
    assert world is not None
  except SystemExit:
    print "World tried to call sys.exit() -- Bad World!"
    print "Fix world module or use another..."
    sys.exit(1)
  
  if __debug__:
    print world
  
  world.validate()
  
  img_aspect = img_size[0] / float(img_size[1])
  film_aspect = world.active_camera.film_aspect_ratio()
  if math.fabs(img_aspect-film_aspect) > 1e-2:
    print """WARNING: image aspect ratio (%.2f) does not match active camera's film 
  aspect ratio (%.2f).  Output image will have some distortion (%f)""" % \
  (img_aspect, film_aspect, img_aspect-film_aspect)
  
  if options.verbose:
    print "world created.\ncreating render farm..."
  
  farm = parse_farm_cfg(options.farmcfg)

  if farm is None and options.verbose:
    print "... no render farm defined"

  if options.verbose:
    print "initializing app..."
  
  app = TracerApp(world, img_size, farm)

  if options.noshadows:
    if options.verbose:
      print "not calculating shadows..."
    app.tracer.doshadows=False

  if options.verbose:
    print "tracing... I hope you have a good book to read."
    print "press any key or click in the window to quit."
  
  if options.profile:
    # TODO psyco and profile are mutually exclusive -- hmmm...

    import profile
    import pstats

    pr=profile.Profile()
    elapsed = pr.runcall(app.trace, options.output)
    statsfile = "%s.profile" % TracerApp.NAME
    pr.dump_stats(statsfile)
    p = pstats.Stats(statsfile)
    p.strip_dirs().sort_stats('time','cumulative').print_stats()

  else:
    elapsed = app.trace(options.output)

  if options.verbose:
    print "raytrace took %.2f seconds" % elapsed

  if options.verbose:
    app.tracer.dump_stats()

  if not options.quitatend:
    app.wait_quit()

  print "goodbye."

