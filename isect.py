# This file was created automatically by SWIG.
# Don't modify this file, modify the SWIG interface instead.
# This file is compatible with both classic and new-style classes.
import _isect
def _swig_setattr(self,class_type,name,value):
    if (name == "this"):
        if isinstance(value, class_type):
            self.__dict__[name] = value.this
            if hasattr(value,"thisown"): self.__dict__["thisown"] = value.thisown
            del value.thisown
            return
    method = class_type.__swig_setmethods__.get(name,None)
    if method: return method(self,value)
    self.__dict__[name] = value

def _swig_getattr(self,class_type,name):
    method = class_type.__swig_getmethods__.get(name,None)
    if method: return method(self)
    raise AttributeError,name

import types
try:
    _object = types.ObjectType
    _newclass = 1
except AttributeError:
    class _object : pass
    _newclass = 0


class v3(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, v3, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, v3, name)
    __swig_setmethods__["x"] = _isect.v3_x_set
    __swig_getmethods__["x"] = _isect.v3_x_get
    if _newclass:x = property(_isect.v3_x_get,_isect.v3_x_set)
    __swig_setmethods__["y"] = _isect.v3_y_set
    __swig_getmethods__["y"] = _isect.v3_y_get
    if _newclass:y = property(_isect.v3_y_get,_isect.v3_y_set)
    __swig_setmethods__["z"] = _isect.v3_z_set
    __swig_getmethods__["z"] = _isect.v3_z_get
    if _newclass:z = property(_isect.v3_z_get,_isect.v3_z_set)
    def __init__(self,*args):
        self.this = apply(_isect.new_v3,args)
        self.thisown = 1
    def __del__(self, destroy= _isect.delete_v3):
        try:
            if self.thisown: destroy(self)
        except: pass
    def __repr__(self):
        return "<C v3 instance at %s>" % (self.this,)

class v3Ptr(v3):
    def __init__(self,this):
        self.this = this
        if not hasattr(self,"thisown"): self.thisown = 0
        self.__class__ = v3
_isect.v3_swigregister(v3Ptr)

class ray(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, ray, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, ray, name)
    __swig_setmethods__["o"] = _isect.ray_o_set
    __swig_getmethods__["o"] = _isect.ray_o_get
    if _newclass:o = property(_isect.ray_o_get,_isect.ray_o_set)
    __swig_setmethods__["d"] = _isect.ray_d_set
    __swig_getmethods__["d"] = _isect.ray_d_get
    if _newclass:d = property(_isect.ray_d_get,_isect.ray_d_set)
    def __init__(self,*args):
        self.this = apply(_isect.new_ray,args)
        self.thisown = 1
    def __del__(self, destroy= _isect.delete_ray):
        try:
            if self.thisown: destroy(self)
        except: pass
    def __repr__(self):
        return "<C ray instance at %s>" % (self.this,)

class rayPtr(ray):
    def __init__(self,this):
        self.this = this
        if not hasattr(self,"thisown"): self.thisown = 0
        self.__class__ = ray
_isect.ray_swigregister(rayPtr)

class hit(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, hit, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, hit, name)
    __swig_setmethods__["t"] = _isect.hit_t_set
    __swig_getmethods__["t"] = _isect.hit_t_get
    if _newclass:t = property(_isect.hit_t_get,_isect.hit_t_set)
    __swig_setmethods__["I"] = _isect.hit_I_set
    __swig_getmethods__["I"] = _isect.hit_I_get
    if _newclass:I = property(_isect.hit_I_get,_isect.hit_I_set)
    __swig_setmethods__["P"] = _isect.hit_P_set
    __swig_getmethods__["P"] = _isect.hit_P_get
    if _newclass:P = property(_isect.hit_P_get,_isect.hit_P_set)
    __swig_setmethods__["N"] = _isect.hit_N_set
    __swig_getmethods__["N"] = _isect.hit_N_get
    if _newclass:N = property(_isect.hit_N_get,_isect.hit_N_set)
    def __init__(self,*args):
        self.this = apply(_isect.new_hit,args)
        self.thisown = 1
    def __del__(self, destroy= _isect.delete_hit):
        try:
            if self.thisown: destroy(self)
        except: pass
    def __repr__(self):
        return "<C hit instance at %s>" % (self.this,)

class hitPtr(hit):
    def __init__(self,this):
        self.this = this
        if not hasattr(self,"thisown"): self.thisown = 0
        self.__class__ = hit
_isect.hit_swigregister(hitPtr)

class sphere(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, sphere, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, sphere, name)
    __swig_setmethods__["c"] = _isect.sphere_c_set
    __swig_getmethods__["c"] = _isect.sphere_c_get
    if _newclass:c = property(_isect.sphere_c_get,_isect.sphere_c_set)
    __swig_setmethods__["r"] = _isect.sphere_r_set
    __swig_getmethods__["r"] = _isect.sphere_r_get
    if _newclass:r = property(_isect.sphere_r_get,_isect.sphere_r_set)
    __swig_setmethods__["r2"] = _isect.sphere_r2_set
    __swig_getmethods__["r2"] = _isect.sphere_r2_get
    if _newclass:r2 = property(_isect.sphere_r2_get,_isect.sphere_r2_set)
    def __init__(self,*args):
        self.this = apply(_isect.new_sphere,args)
        self.thisown = 1
    def __del__(self, destroy= _isect.delete_sphere):
        try:
            if self.thisown: destroy(self)
        except: pass
    def __repr__(self):
        return "<C sphere instance at %s>" % (self.this,)

class spherePtr(sphere):
    def __init__(self,this):
        self.this = this
        if not hasattr(self,"thisown"): self.thisown = 0
        self.__class__ = sphere
_isect.sphere_swigregister(spherePtr)

class plane(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, plane, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, plane, name)
    __swig_setmethods__["n"] = _isect.plane_n_set
    __swig_getmethods__["n"] = _isect.plane_n_get
    if _newclass:n = property(_isect.plane_n_get,_isect.plane_n_set)
    __swig_setmethods__["d"] = _isect.plane_d_set
    __swig_getmethods__["d"] = _isect.plane_d_get
    if _newclass:d = property(_isect.plane_d_get,_isect.plane_d_set)
    def __init__(self,*args):
        self.this = apply(_isect.new_plane,args)
        self.thisown = 1
    def __del__(self, destroy= _isect.delete_plane):
        try:
            if self.thisown: destroy(self)
        except: pass
    def __repr__(self):
        return "<C plane instance at %s>" % (self.this,)

class planePtr(plane):
    def __init__(self,this):
        self.this = this
        if not hasattr(self,"thisown"): self.thisown = 0
        self.__class__ = plane
_isect.plane_swigregister(planePtr)

test = _isect.test

ray_sphere = _isect.ray_sphere

ray_plane = _isect.ray_plane


