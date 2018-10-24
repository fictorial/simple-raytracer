#!/usr/bin/env pythonw

# World Composer for PyTrace - PyOpenGL/PyGame 
# Setup entities, cameras

import sys, os, random, math, optparse

try:
  import pygame
  from   pygame.locals  import *
  
  from   cgtypes        import *
  
  from   OpenGL.GL      import *
  from   OpenGL.GLU     import *
  from   OpenGL.GLUT    import *
  
  from   pytrace.ray               import Ray
  from   pytrace.camera            import Camera
  from   pytrace.primitives.sphere import Sphere
  from   pytrace.primitives.plane  import Plane

except ImportError, err:
  print "Failed to import module(s). %s" % err
  sys.exit(1)

window_size = 800,600
current_pixel = [0,0]
from_camera = False

def render_axes(extent=10):
  glBegin(GL_LINES)
  glColor3f(1,0,0)
  glVertex3f(0,0,0)
  glVertex3f(extent,0,0)
  glColor3f(1,1,0)
  glVertex3f(0,0,0)
  glVertex3f(0,extent,0)
  glColor3f(0,1,0)
  glVertex3f(0,0,0)
  glVertex3f(0,0,extent)
  glEnd()

def render_grid(x0, z0, x1, z1, steps=10):
  dx = (x1-x0)/ float(steps)
  dz = (z1-z0)/ float(steps)
  glBegin(GL_LINES)
  z = z0
  while z <= z1:
    glVertex3f(x0, 0, z)
    glVertex3f(x1, 0, z)
    z += dz
  x = x0
  while x <= x1:
    glVertex3f(x, 0, z0)
    glVertex3f(x, 0, z1)
    x += dx
  glEnd()
  
def render_camera(cam):
  glPushMatrix()
  
  # Camera frame of reference (CCS).

  # Eye
  glEnable(GL_LIGHTING)
  glTranslatef(cam.eye[0], cam.eye[1], cam.eye[2])
  glColor3f(.75,.5,0)
  glutSolidSphere(0.15,10,10)
  glDisable(GL_LIGHTING)
  
  # U,V,N
  glLineWidth(3)
  glBegin(GL_LINES)
  glColor3f(1,0,0)
  glVertex3f(0,0,0)
  glVertex3fv(cam.U)
  glColor3f(1,1,0)
  glVertex3f(0,0,0)
  glVertex3fv(cam.V)
  glColor3f(0,1,0)
  glVertex3f(0,0,0)
  glVertex3fv(cam.N)
  glEnd()
  glPopMatrix()
  
  # eye -> principal pt
  glPushMatrix()
  glBegin(GL_LINES)
  glColor3f(1,0,0)
  glVertex3fv(cam.eye)
  c = cam.vp_center
  glVertex3fv(c)
  
  # eye to ground (XZ plane)
  glColor3f(.4,.4,.4)
  glVertex3f(cam.eye[0], cam.eye[1], cam.eye[2])
  glVertex3f(cam.eye[0], 0, cam.eye[2])
  
  # viewport on focal plane.
  tl=cam.vp_origin
  tr=tl+cam.U*cam.frame_area[0]
  bl=tl-cam.V*cam.frame_area[1]
  br=tr-cam.V*cam.frame_area[1]
  
  # lines to viewport on focal plane.
  glColor3f(1,.5,.5)
  glVertex3fv(cam.eye)
  glVertex3fv(tl)
  glColor3f(.75,.75,.75)
  glVertex3fv(cam.eye)
  glVertex3fv(tr)
  glVertex3fv(cam.eye)
  glVertex3fv(br)
  glVertex3fv(cam.eye)
  glVertex3fv(bl)

  # lines through center of viewport on focal plane (top to bottom, left to right)
  glColor4f(0, 0.2, 0.5, .65)
  glVertex3fv(c+cam.V*cam.frame_area[1]*.5)  # t
  glVertex3fv(c-cam.V*cam.frame_area[1]*.5)  # b
  glVertex3fv(c-cam.U*cam.frame_area[0]*.5)  # l
  glVertex3fv(c+cam.U*cam.frame_area[0]*.5)  # r
  glEnd()

  # filled version of viewport on focal plane.
  glColor4f(0, 0.4, 0.5, 0.55)
  glBegin(GL_QUADS)
  glVertex3fv(tl)
  glVertex3fv(tr)
  glVertex3fv(br)
  glVertex3fv(bl)
  glEnd()
  
  # viewport outline.
  glColor3f(0,1,1)
  glBegin(GL_LINES)
  glVertex3fv(tl)
  glVertex3fv(tr)
  glVertex3fv(tr)
  glVertex3fv(br)
  glVertex3fv(br)
  glVertex3fv(bl)
  glVertex3fv(bl)
  glVertex3fv(tl)
  glEnd()

  # to current pixel.
  glDisable(GL_DEPTH_TEST)
  global current_pixel
  glColor3f(0,0,1)
  glBegin(GL_LINES)
  glVertex3fv(cam.eye)
  pt=cam.screen2world(current_pixel[0], current_pixel[1])
  glVertex3fv(pt)
  glEnd()

  glPushMatrix()
  glColor3f(.5,.5,.85)
  glTranslatef(pt[0],pt[1],pt[2])
  glutSolidSphere(.15, 5,5)
  glPopMatrix()
  glEnable(GL_DEPTH_TEST)

  glPopMatrix()  
  glEnable(GL_LIGHTING)
    
class View:
  def __init__(self, window_size, world):
    pygame.display.init()
    screen = pygame.display.set_mode(window_size, OPENGL|DOUBLEBUF)
    pygame.display.set_caption("PyTrace -- Camera Tester")
    self.window_size=window_size
    self.world=world
    self.setup()

  def setup(self):
    glViewport(0, 0, self.window_size[0], self.window_size[1])
    glClearColor(0,0,0,0)
    glEnable(GL_DEPTH_TEST)
    glDisable(GL_LIGHTING)
    glEnable(GL_LIGHTING)
    glEnable(GL_NORMALIZE)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glShadeModel(GL_SMOOTH)
    
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    glLightfv(GL_LIGHT0,GL_POSITION,[20,20,20,0])
    glLightfv(GL_LIGHT0,GL_DIFFUSE,[1,0,0,1])
    glLightfv(GL_LIGHT0,GL_SPECULAR,[1,1,1,1])
    glEnable(GL_LIGHT0)
    
    #global window_size
    #self.cam = Camera(window_size)
    #self.cam.lookat(eye=vec3(0,50,60), at=vec3(0,0,0))
    #self.cam.focal_length=60
    #self.cam.frame_area=(2.35*20, 20)
    #print self.cam

  def render(self):
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT);
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
   
    cam = self.world.active_camera
   
    global from_camera
    if not from_camera:
      P = mat4(1).perspective(45, 1.3333, 0.2, 20000)
    else:
      P = mat4(1).perspective(cam.fovy, cam.film_aspect_ratio(), 0.2, 20000)
    
    glMultMatrixd(P.toList())
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glPushMatrix()

    if not from_camera:
      we=cam.eye + cam.N*-15 + cam.V*5 + cam.U*2
      gluLookAt(we[0],we[1],we[2], 0,0,0, 0,1,0)
    else:
      gluLookAt(cam.eye[0], cam.eye[1], cam.eye[2],
        cam.eye[0] + cam.N[0], cam.eye[1] + cam.N[1], cam.eye[2] + cam.N[2], 
        0,1,0)
    
    glDisable(GL_LIGHTING)
    glColor4f(1,1,1,.1)
    glLineWidth(1)
    render_grid(-100, -100, 100, 100, 200)
    
    glPushMatrix()
    glDisable(GL_DEPTH_TEST)
    render_axes(1)
    glEnable(GL_DEPTH_TEST)
    glPopMatrix()
    
    self._render_world()
    
    glPopMatrix()
    pygame.display.flip()

  def _render_world(self):
    # render little spheres for all the point lights
    for l in self.world.lights:
      glColor3f(l.color[0], l.color[1], l.color[2])
      glPushMatrix()
      glTranslatef(l.pos[0], l.pos[1], l.pos[2])
      glutSolidSphere(1, 10, 10)
      glPopMatrix()

    # render the primitives 
    # TODO -- can we make this more OOP by augmenting INSTANCES with render() methods?

    for p in self.world.primitives:
      if isinstance(p, Sphere):
        glColor3fv(p.material.c)
        glPushMatrix()
        glTranslatef(p.c[0], p.c[1], p.c[2])
        glutSolidSphere(p.r, 10, 10)
        glPopMatrix()
      elif isinstance(p, Plane):
        s = 25.0
        
        tl = vec3(-s,0,-s)
        tr = vec3(s,0,-s)
        br = vec3(s,0,s)
        bl = vec3(-s,0,s)
        
        ang = p.n * vec3(0.0,1.0,0.0)
        axis = p.n.cross(vec3(0,1,0))
        
        pygame.display.set_caption('%s %f %s' % (p.n,math.degrees(ang),axis))
        
        glColor4f(p.material.c[0], p.material.c[1], p.material.c[2], 0.5)
        glPushMatrix()
        glRotatef(math.degrees(ang), axis[0], axis[1], axis[2])
        glTranslatef(0, -p.d, 0)
        glBegin(GL_QUADS)
        glVertex3fv(tl)
        glVertex3fv(tr)
        glVertex3fv(br)
        glVertex3fv(bl)
        glEnd()
        glPopMatrix()
      
    global from_camera
    if not from_camera:
      render_camera(self.world.active_camera)
    
def main():
  global window_size, current_pixel
  
  optparser = optparse.OptionParser(usage="%prog --world=WORLD [options]")
  optparser.add_option("--width", type="int", 
    dest="width", default=800, metavar="WIDTH",
    help="width of window")
  optparser.add_option("--height", type="int", 
    dest="height", default=600, metavar="HEIGHT",
    help="height of window")
  optparser.add_option("--world", type="string", 
    dest="worldmodule",
    help="path to Python file defining world (e.g. myworlds.testworld)")
  optparser.add_option("-v", "--verbose", action="store_true",
    default=False, dest="verbose", 
    help="verbose output")
  options, args = optparser.parse_args()
  
  window_size = options.width, options.height
  
  if options.worldmodule is None:
    optparser.error("Missing --world required argument.")

  if options.verbose:
    print "loading world from module %s" % options.worldmodule

  # TODO need to put make_world under restricted execution mode... 
  # TODO don't need world-definitions doing something dirty.

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
    world = module.make_world(window_size)
    assert world is not None
  except SystemExit:
    print "World tried to call sys.exit() -- Bad World!"
    print "Fix world module or use another..."
    sys.exit(1)
  
  if options.verbose:
    print "world created.\ninitializing view..."

  pygame.init()
  view = View(window_size, world)
  
  while True:
    evt = pygame.event.poll()
    
    def myexit():
      print "Quitting..."
      sys.exit(0)
    
    if evt.type is QUIT:
      myexit()
    
    if evt.type == KEYDOWN:
      if evt.key == K_ESCAPE:
        myexit()
      if evt.key == K_SPACE:
        global from_camera
        from_camera = not from_camera
        print "Viewing from camera: %s" % from_camera
    
    keys = pygame.key.get_pressed()
    
    if keys[K_UP]:   
      view.world.active_camera.focal_length += 1.0
    
    if keys[K_DOWN]: 
      if view.world.active_camera.focal_length - 1.0 <= 0.0:
        view.world.active_camera.focal_length = 1.0
      else:
        view.world.active_camera.focal_length -= 1.0
          
    if keys[K_i]:
      current_pixel[0] += 1
      if current_pixel[0] >= window_size[0]:
        current_pixel[0] = 0
        current_pixel[1] += 1
      if current_pixel[1] >= window_size[1]:
        current_pixel[1] = window_size[1] - 1

    if keys[K_j]:
      current_pixel[1] += 1
      if current_pixel[1] >= window_size[1]:
        current_pixel[1] = window_size[1] - 1
        
    view.render()

if __name__ == "__main__": 
  main()

