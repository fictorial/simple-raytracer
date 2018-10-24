global_settings { assumed_gamma 2.2 }
#include "colors.inc" 

camera {
  perspective
  right -4/3*x
  up y
  location <0, 20, 50>
  look_at <0,10,-15>
  angle 60
}

background { color red 0.2 green 0.2 blue 0.2 }

light_source { <15,40,-25> color White }
light_source { <-25,50,5>  color White } 

#declare RMat =
texture { 
  pigment { color red 1 green 0 blue 0 }
  finish  { diffuse 1 phong 0 }
}
    
#declare GMat =
texture { 
  pigment { color red 0 green 1 blue 0 }
  finish  { diffuse 1 phong 0 }
}
    
#declare BMat =
texture { 
  pigment { color red 0 green 0 blue 1 }
  finish  { diffuse 1 phong 0 }
}
    
#declare GroundMat =
texture { 
  pigment { color red 0.4 green 0.4 blue 0.6 }
  finish  { diffuse 1 phong 0 }
}
    
sphere { <-15,10,-15>, 5 texture { RMat } }
sphere { <0,10,-15>,   5 texture { GMat } }
sphere { <15,10,-15>,  5 texture { BMat } }

plane { +y 0 texture { GroundMat } }

