# Popular film formats (aka "backs") of the 20th century.
#
# Sources: 
#  - http://www.film-center.com/formats.html
#  - Alias Wavefront Camera Editor documentation
#
# Brian Hammond <brianhammond at users.sourceforge.net>

# TODO What are the FORMATs for TV,PAL,Anamorphic?
# TODO Seeing conflicting ARs for IMAX: 1.25, 1.34, 1.43 -- which is it?
# TODO HDTV format? Size? AR=1.78 (16:9)
# TODO Seen Super 16 at 1.78 -- ?
# TODO What's the deal with PROJECTORS?

# TODO Does anyone really care about ACTUAL FILM DIMENSIONS or just the aspect ratio?
#      I REALLY think it's just the ratio that matters... 

aspect_ratios = {
'Academy'     : 1.37,
'TV'          : 1.33,
'IMAX'        : 1.38,
'Super 8'     : 1.36,
'Super 16'    : 1.66,
'Panavision'  : 1.85,
'HDTV'        : 1.78,
'CinemaScope' : 2.35
}

db = {
'35mm Standard'      : { 'gauge':35, 'framearea':(24.90,18.67), 'aspect':1.33, 'squeeze':1.0 },
'TV'                 : { 'gauge':35, 'framearea':(10.26, 7.49), 'aspect':1.33, 'squeeze':1.0 },
'Academy'            : { 'gauge':35, 'framearea':(20.95,15.29), 'aspect':1.37, 'squeeze':1.0 },
'VistaVision'        : { 'gauge':35, 'framearea':(37.71,25.17), 'aspect':1.50, 'squeeze':1.0 },
'Panavision'         : { 'gauge':35, 'framearea':(0.839,0.715), 'aspect':2.35, 'squeeze':2.0 },
'35mm 1.85'          : { 'gauge':35, 'framearea':(20.96,11.33), 'aspect':1.85, 'squeeze':1.0 },
'Flat'               : { 'gauge':35, 'framearea':(20.96,11.33), 'aspect':1.85, 'squeeze':1.0 },
'Flat European'      : { 'gauge':35, 'framearea':(-1,-1),       'aspect':1.66, 'squeeze':1.0 },
'Super 8'            : { 'gauge':8,  'framearea':(0.215,0.158), 'aspect':1.36, 'squeeze':1.0 },
'Super 16 1.66'      : { 'gauge':16, 'framearea':(0.464,0.280), 'aspect':1.66, 'squeeze':1.0 },
'Super 16 1.85'      : { 'gauge':16, 'framearea':(0.464,0.251), 'aspect':1.85, 'squeeze':1.0 },

# I've seen all sorts of different reports on this.  IMAX seems to have been replaced by 
# OMNIMAX in 1973 but the name IMAX is still common.  
#
# HowStuffWorks.com has IMAX information.  They say the typical IMAX theatre has a screen that
# is 

'OMNIMAX'            : { 'gauge':70, 'framearea':(2.740,1.980), 'aspect':1.38, 'squeeze':1.0 },

# TODO

'IMAX'               : { 'gauge':70, 'framearea':(69.60,48.51), 'aspect':1.43, 'squeeze':1.0 },
'Anamorphic'         : { 'gauge':-1, 'framearea':(21.95,18.59), 'aspect':1.18, 'squeeze':2.0 },
'PAL'                : { 'gauge':-1, 'framearea':(19.50,14.63), 'aspect':1.33, 'squeeze':1.0 },
'HDTV'               : { 'gauge':-1, 'framearea':(-1,-1),       'aspect':1.78, 'squeeze':1.0 },
'CinemaScope'        : { 'gauge':-1, 'framearea':(-1,-1),       'aspect':2.35, 'squeeze':1.0 },
'35mm TV projection'   : (20.73, 15.54), # 1.33
'70mm projection'      : (52.48, 23.01), # 2.28
}

