# <<Description Here>>
#
# Module : $File$
# Author : $Author$
# Version: $Version$
# Status : $Status$
#
# Copyright (C) 2002 Brian Hammond. All Rights Reserved

import math
import isect

class Sphere(object):
  tests = 0
  tests_failed = 0

  def __init__(self, c, r):
    "Sphere with center C and radius R"
    assert r>0
    self.c = c
    self.r = r
    self.r2 = r*r
    self.material = None
    
    self.isph=isect.sphere()
    self.isph.c=isect.v3(c.x,c.y,c.z)
    self.isph.r=r
    self.isph.r2=r*r
  
  def intersect(self, Ro, Rd):
    r=isect.ray()
    r.o=isect.v3(Ro.x,Ro.y,Ro.z)
    r.d=isect.v3(Rd.x,Rd.y,Rd.z)
    h=isect.ray_sphere(r,self.isph)
    if h.t > 0:
      return { 'I':h.I, 't':h.t, 'P':h.P, 'N':h.N, 'prim':self }    
  
  def __intersect(self, Ro, Rd):
    Sphere.tests += 1
    
    # Geometric method
    
    L  = self.c - Ro
    D  = L * Rd
    L2 = L * L
    
    if D < 0 and L2 > self.r2:
      Sphere.tests_failed += 1
      return None
    
    M2 = L2 - D * D
    
    if M2 > self.r2:
      Sphere.tests_failed += 1
      return None
    
    Q = math.sqrt(self.r2 - M2)
    
    if L2 > self.r2:
      t = D - Q
    else: 
      t = D + Q
    
    P = Ro + t * Rd
    N = (P - self.c).normalize()
    
    return { 'I':Rd, 't':t, 'P':P, 'N':N, 'prim':self }    
    
  def __str__(self):
    return "Sphere(c=%s, r=%.2f)" % (self.c, self.r)
