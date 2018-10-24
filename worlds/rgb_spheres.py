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
from sphere import Sphere
from plane  import Plane

def make_world(image_size):
  w=World("reflective spheres on plane")
  
  w.bgcolor=RGB(.0,.0,.0)
  w.ambient=RGB(.1,.1,.1)
  
  radius=5.0
 
  # TODO better param names?
  # shininess controls how spread out the specular highlight is
  # Ks controls the intensity of the specular highlight
  # specular controls the color of the specular highlight
 
  rs=Sphere(c=vec3(-radius*3,radius*2,-radius*3), r=radius)
  rsmat = Material(name="Red", diffuse=RGB(1,0,0), Ks=0.6, shininess=16.0)
  w.materials.append(rsmat)
  rs.material=rsmat
  w.primitives.append(rs)

  gs=Sphere(c=vec3(0,radius*2,-radius*3), r=radius)
  gsmat = Material(name="GrayGreen", diffuse=RGB(.4,.6,.4), Ks=0.8, shininess=12.0)
  w.materials.append(gsmat)
  gs.material=gsmat
  w.primitives.append(gs)

  bs=Sphere(c=vec3(radius*3,radius*2,-radius*3), r=radius)
  bsmat = Material(name="Blue", diffuse=RGB(0,0,1), Ks=0.75, shininess=12.0)
  w.materials.append(bsmat)
  bs.material=bsmat
  w.primitives.append(bs)

  p=Plane(n=vec3(0,1,0), d=0)
  pmat = Material(name="Ground", diffuse=RGB(.4,.4,.6), Ks=0.1, shininess=8.0)
  w.materials.append(pmat)
  p.material=pmat
  w.primitives.append(p)
 
  c=Camera(image_size)
  c.lookat(eye=rs.c-gs.c+vec3(-1,0,0)*rs.r*2+vec3(0,0,1)*rs.r*1.45+vec3(0,1,0)*rs.r*4, at=rs.c+vec3(6,0,4))
  c.fovx=65
  w.cameras.append(c)
  w.active_camera=c

  s=gs
 
  l = Light(pos=vec3(s.c + s.r *  3 * vec3(1,0,0) + 
                           s.r *  5 * vec3(0,1,0) + 
                           s.r * -2 * vec3(0,0,1)), color=RGB(1,1,1))
  w.lights.append(l)
    
  l = Light(pos=vec3(s.c + s.r * -4 * vec3(1,0,0) + 
                           s.r *  4 * vec3(0,1,0) + 
                           s.r * +2 * vec3(0,0,1)), color=RGB(1,1,1))
  w.lights.append(l)
  
  return w

