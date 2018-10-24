import math
from   cgtypes        import *
from   pytrace.entity import Entity

class Camera(Entity):
  _num_cameras = 1
  
  def __init__(self, image_size, name=None):
    assert len(image_size) == 2 and image_size[0] > 0 and image_size[1] > 0
    
    if name is None: 
      name = "Camera %d" % Camera._num_cameras 
    
    Entity.__init__(self, name) 
    Camera._num_cameras = Camera._num_cameras + 1
    
    self._image_size = image_size
    self._frame_area = (32.0, 24.0)  # 35mm film
    self._u = vec3(1,0,0)
    self._v = vec3(0,1,0)
    self._n = vec3(0,0,-1)
    self._eye = vec3(0,0,0)
    self.set_focal_length(20.0)   # NB: calls _setup()
  
  def lookat(self, eye, at, up=vec3(0,1,0)):
    self._eye = eye
    self._n = (at-eye).normalize()
    self._u = self._n.cross(up).normalize()
    self._v = self._u.cross(self._n)
    self._setup()

  def get_eye(self): 
    return self._eye
  
  eye = property(get_eye)
  
  def get_u(self): 
    return self._u
  
  U = property(get_u)
  
  def get_v(self): 
    return self._v
  
  V = property(get_v)
  
  def get_n(self): 
    return self._n

  N = property(get_n)

  # TODO - Use matrix representation of camera basis
  #      - Extract U,V,N from matrix
  # TODO - xform by matrix (in order to rotate, etc)
  # TODO - change of base

  def set_frame_area(self, frame_area):
    assert len(frame_area) == 2 and frame_area[0] > 0 and frame_area[1] > 0
    
    self._frame_area = frame_area
    self._fovx = 2.0 * math.atan((self._frame_area[0] * 0.5) / self._focal_length)
    self._setup()
  
  def get_frame_area(self): 
    return self._frame_area
  
  frame_area = property(get_frame_area, set_frame_area, doc="film aspect ratio")

  def film_aspect_ratio(self):
    "Returns the film aspect ratio (film width / film height)"
    return float(self._frame_area[0] / self._frame_area[1])

  def set_image_size(self, s):
    self._image_size = s
    self._setup()
  
  def get_image_size(self): 
    return self.image_size
  
  image_size = property(get_image_size, set_image_size, doc="Output image dimensions")

  def set_fovx(self, fovx):
    self._fovx = math.radians(fovx)
    self._focal_length = (self._frame_area[0] * 0.5) / math.tan(self._fovx * 0.5)
    self._setup()
  
  def get_fovx(self): 
    return math.degrees(self._fovx)
  
  fovx = property(get_fovx, set_fovx, doc="HFOV (degrees)")

  def get_fovy(self):
    return math.degrees(2.0 * math.atan((self._frame_area[1] * 0.5) / self._focal_length))
  
  fovy = property(get_fovy, doc="VFOV (degrees)")

  def set_focal_length(self, f):
    assert f > 0

    self._focal_length = float(f)
    self._fovx = 2.0 * math.atan((self._frame_area[0] * 0.5) / self._focal_length)
    self._setup()
  
  def get_focal_length(self): 
    return self._focal_length
  
  focal_length = property(get_focal_length, set_focal_length)

  def _setup(self):
    self._pixel_size = (
      self._frame_area[0] / float(self._image_size[0]),
      self._frame_area[1] / float(self._image_size[1]))
  
    self._vp_center = self._eye + self._n*self._focal_length
    self._vp_origin = self._vp_center - self._u*self._frame_area[0]*0.5 + self._v*self._frame_area[1]*0.5

  def get_pixel_size(self): 
    return self._pixel_size
  
  pixel_size = property(get_pixel_size, doc="w,h of pixel in world coords (mm/pixel)")

  def get_vp_center(self):
    return self._vp_center

  vp_center = property(get_vp_center, doc="principal pt; center of viewport on focal plane")
  
  def get_vp_origin(self):
    return self._vp_origin

  vp_origin = property(get_vp_origin, doc="origin of viewport on focal plane (top, left)")
  
  def cam2world(self, v):
    "Returns V transformed from CCS to WCS"
    return self._eye + v[0]*self._u + v[1]*self._v + v[2]*self._n
  
  def world2cam(self, v):
    "Returns V transformed from WCS to CCS"
    s = v - self._eye
    return vec3(self._u*s, self._v*s, self._n*s)

  def cam2world_matrix(self):
    "Returns a matrix that transforms pts in CCS to WCS"
    #TODO
    return mat4()

  def world2cam_matrix(self):
    "Returns a matrix that transforms pts in WCS to CCS"
    #TODO
    return mat4()

  def primary_ray(self, i, j):
    "Return ray from eye through pixel (i,j) (WCS)"
    u_weight, v_weight = i * self._pixel_size[0], j * self._pixel_size[1]
    p = self._vp_origin + self._u * u_weight - self._v * v_weight
    return self._eye, (p - self._eye).normalize()

  def screen2world(self, i, j):
    "Return point on focal plane in WCS for pixel (i,j)"
    u_weight, v_weight = i * self._pixel_size[0], j * self._pixel_size[1]
    return self._vp_origin + self._u * u_weight - self._v * v_weight

  def __str__(self):
    return "Camera \"%s\" E=%s U=%s V=%s N=%s fovx=%.2f deg " \
    "fovy=%.2f deg focallength=%.2fmm image=(W:%d pix H:%d pix AR:%.2f) " \
    "film=(W:%dmm H:%dmm AR:%.2f) pixel in world=(W:%.2fmm H:%.2fmm) " \
    "vp_center=%s vp_origin=%s" % (self.name, self.eye, self._u, self._v, self._n, 
    self.fovx, self.fovy, self._focal_length, self._image_size[0], 
    self._image_size[1], self._image_size[0] / float(self._image_size[1]),
    self._frame_area[0], self._frame_area[1], self._frame_area[0] / float(self._frame_area[1]),
    self._pixel_size[0], self._pixel_size[1], 
    self._vp_center, self._vp_origin)

