# A test world for PyTrace.
#
# This file is loaded and compiled dynamically by PyTrace.
# The only really important constraint to remember is that there
# must be an exported module-level function named make_world()
# that returns a pytrace.world.World instance.
#
# Module : $File$
# Author : $Author$
# Version: $Version$
# Status : $Status$
#
# Copyright (C) 2003 Brian Hammond. All Rights Reserved

from random  import random, randrange
from cgtypes import *

from pytrace.world             import World
from pytrace.material          import Material
from pytrace.camera            import Camera
from pytrace.light             import Light
from pytrace.color             import RGB, RGBA
from pytrace.primitives.sphere import Sphere
from pytrace.primitives.plane  import Plane 

def make_world(image_size):
  w=World("Test1")
  w.bgcolor=RGB(1,1,1)
  w.ambient=RGB(.2,.2,.2)

  room_size=50
  num_spheres=8
  num_lights=3
  
  # Primitives
  
  for x in range(num_spheres):
    r=randrange(room_size/5, room_size/3)
    s=Sphere(c=vec3(
             randrange(int(-room_size+r), int(room_size-r)), 
             randrange(int(-room_size+r), int(room_size-r)),
             randrange(int(-room_size+r), int(room_size-r))), 
             r=r)
    s.material=Material("Sphere%d" % x)
    s.material.diff=RGB(0.5+random()-0.5, 0.5+random()-0.5, 0.5+random()-0.5)
    w.materials.append(s.material)
    w.primitives.append(s)
  
  wall_material=Material(name="Wall", diff=RGB(0.5,0.5,0.5))
  w.materials.append(wall_material)
  
  floor_material=Material(name="Floor", diff=RGB(0.2,0.2,0.2))
  w.materials.append(floor_material)

  ceil_material=Material(name="Ceiling", diff=RGB(0.6, 0.4, 0.4))
  w.materials.append(ceil_material)
  
  floor_plane=Plane(n=vec3(0,1,0), d=room_size)
  floor_plane.material=floor_material
  w.primitives.append(floor_plane)

  ceil_plane=Plane(n=vec3(0,-1,0), d=room_size)
  ceil_plane.material=ceil_material
  w.primitives.append(ceil_plane)

  back_plane=Plane(n=vec3(0,0,1), d=room_size)
  back_plane.material=wall_material
  w.primitives.append(back_plane)

  left_plane=Plane(n=vec3(1,0,0), d=room_size)
  left_plane.material=wall_material
  w.primitives.append(left_plane)

  right_plane=Plane(n=vec3(-1,0,0), d=room_size)
  right_plane.material=wall_material
  w.primitives.append(right_plane)

  c=Camera(image_size)
  c.lookat(eye=vec3(0,20,100), at=vec3(0,0,0))
  c.focal_length=20
  w.cameras.append(c)
  w.active_camera=c

  # Lights
  
  for z in range(num_lights):
    l = Light(pos=vec3(randrange(-room_size,room_size), randrange(-room_size,room_size), 
              randrange(-room_size,room_size)), color=RGB(1,1,0))
    w.lights.append(l)
    
  return  w

