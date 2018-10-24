import math
#from   pytrace.config import eps

class Plane(object):
  def __init__(self, n, d):
    "Normal N at distance D"
    self.n = n
    self.d = d
    
  def intersect(self, Ro, Rd):
    # Plugin ray eq into point normal form of plane eq
    # You get Np . (Ro + t*Rd) + Dp = 0.  Solve for t.

    D = self.n * Rd

    # Check if coplanar
    
    if math.fabs(D) < 1e-7:
      return None  
    
    t = -(self.n * Ro + self.d) / D 
    
    if t < 0: 
      return None
   
    return { 'I':Rd, 't':t, 'P':Ro + t * Rd, 'N':self.n, 'prim':self }    

  def __str__(self):
    return "Plane(n=%s, d=%.2f)" % (self.n, self.d)

