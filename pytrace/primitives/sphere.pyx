# <<Description Here>>
#
# Module : $File$
# Author : $Author$
# Version: $Version$
# Status : $Status$
#
# Copyright (C) 2002 Brian Hammond. All Rights Reserved

import math

class Sphere:
  def __init__(self, c, r):
    "Sphere with center C and radius R"
    assert r>0
    self.c = c
    self.r = r
    self.r2 = r*r
    self.material = None
    
  def intersect(self, Ro, Rd):
    # Geometric method
    
    L  = self.c - Ro
    D  = L * Rd
    L2 = L * L
    
    if D < 0 and L2 > self.r2:
      return None
    
    M2 = L2 - D * D
    
    if M2 > self.r2:
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
