# PyTrace World Module
# 
# Module : $File$
# Author : $Author$
# Version: $Version$
# Status : $Status$
# 
# Copyright (C) 2002 Brian Hammond. All Rights Reserved

from cgtypes                   import *

from pytrace.world             import World
from pytrace.material          import Material
from pytrace.camera            import Camera
from pytrace.light             import Light
from pytrace.color             import RGB, RGBA
from pytrace.primitives.sphere import Sphere
from pytrace.primitives.plane  import Plane 

def make_world(image_size):
  w=World("single sphere on plane")
  w.bgcolor=RGB(1,1,1)
  
  s=Sphere(c=vec3(0,0,-40), r=10)
  s.material=Material(diffuse=RGB(1,0,0), Ks=2.8, shininess=12)
  w.primitives.append(s)
  
  l=Light(pos=vec3(10,20,10), color=RGB(1,1,1))
  w.lights.append(l)

  c=Camera(image_size)
  c.fovx=40
  c.lookat(eye=vec3(0,0,0), at=s.c)
  w.cameras.append(c)
  w.active_camera=c
  
  return w

