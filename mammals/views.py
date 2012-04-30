from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.template import RequestContext, TemplateDoesNotExist
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.db import connection 
from django.db.models import get_model, DateField
from django.contrib.auth.decorators import login_required
from django.conf import settings
from datetime import datetime, date
from django.contrib.auth.decorators import user_passes_test
from django.utils import simplejson
from django.contrib.gis.geos import  * 
from django.contrib.gis.measure import D # D is a shortcut for Distance 
from django.template.loader import get_template
from mammals.grid_math import *
from django.utils import simplejson
from django.shortcuts import render_to_response
from django.template import RequestContext,  TemplateDoesNotExist
from blackrock.mammals.models import *
from operator import attrgetter
from string import uppercase
from random import *

def get_float (request, name, default):
    number = request.POST.get(name, default)
    return float (number)

def get_int (request, name, default):
    number = request.POST.get(name, default)
    return int (number)

class rendered_with(object):
    def __init__(self, template_name):
        self.template_name = template_name

    def __call__(self, func):
        def rendered_func(request, *args, **kwargs):
            items = func(request, *args, **kwargs)
            if type(items) == type({}):
                return render_to_response(self.template_name, items, context_instance=RequestContext(request))
            else:
                return items

        return rendered_func

#@rendered_with('mammals/sandbox_grid.html')
@rendered_with('mammals/grid.html')
@csrf_protect
def sandbox_grid(request):
    default_lat  = 41.400
    default_lon  = -74.0305
    default_size = 250.0
    
    if (request.method != 'POST'):
        grid_center                             = [default_lat, default_lon]
        height_in_blocks,  width_in_blocks,     = [3, 4]
        block_size_in_m  = default_size
        grid_center_y, grid_center_x = grid_center
        
    else:
        height_in_blocks =                      get_int( request,   'height_in_blocks',         21)
        width_in_blocks   =                     get_int( request,   'width_in_blocks',          27)
        block_size_in_m =                       get_float( request, 'block_size_in_m',        default_size)
        grid_center_y          =                get_float( request, 'grid_center_y',            default_lat)
        grid_center_x           =               get_float( request, 'grid_center_x',            default_lon)
        grid_center = grid_center_y, grid_center_x
    
    grid_height_in_m = block_size_in_m * height_in_blocks
    grid_width_in_m  = block_size_in_m  * width_in_blocks
    
    block_height, block_width  = to_lat_long (block_size_in_m,  block_size_in_m )
    grid_height,  grid_width   = to_lat_long (grid_height_in_m,   grid_width_in_m  )
    grid_bottom,  grid_left  = grid_center[0] - (grid_height / 2), grid_center[1] - (grid_width/2)
    grid_json = []
    
    for i in range (0, height_in_blocks):
        new_column = []
        for j in range (0, width_in_blocks):
            bottom_left = grid_bottom + i * block_height, grid_left + j * block_width
            block = {}
            block['corner_obj'] = set_up_block (bottom_left, block_height, block_width)
            block['row'] = height_in_blocks - i 
            block['column'] = width_in_blocks +  j + 1
            # label them left-to-right, top-to-bottom:
            block['label'] =  (height_in_blocks - i - 1) * width_in_blocks +  j + 1
            grid_json.append (block)
        
    return {
        'grid_json'                                  : simplejson.dumps(grid_json)
        ,'grid_center_y'                             :  grid_center_y
        ,'grid_center_x'                             :  grid_center_x
        ,'height_in_blocks'                          :  height_in_blocks
        ,'width_in_blocks'                           :  width_in_blocks
        ,'block_size_in_m'                           :  block_size_in_m
        ,'sandbox'                                   :  True
    }

@csrf_protect
@rendered_with('mammals/grid.html')
def grid(request):


    grid = [gs.info_for_display() for gs in GridSquare.objects.all() if gs.display_this_square]
    
    #import pdb
    #pdb.set_trace()
    
    
    return {
        'grid_json'                                  :  simplejson.dumps(grid)
        ,'grid_center_y'                             :  41.400
        ,'grid_center_x'                             :  -74.0305
        ,'height_in_blocks'                          :  22
        ,'width_in_blocks'                           :  27
        ,'block_size_in_m'                           :  250.0
        ,'sandbox'                                   :  False
    }

def pick_transects (center, side_of_square, number_of_transects, number_of_points_per_transect, magnetic_declination):
    result = []    
    
    if number_of_transects > 15:
        number_of_transects = 15
    
    
    
    new_transects = pick_transect_angles (number_of_transects)
    
    for tr in new_transects:
        transect = {}
        transect_heading =  tr
        transect_length = length_of_transect (transect_heading, side_of_square)
        transect ['heading'] = radians_to_degrees (transect_heading)
        transect ['heading_radians'] = transect_heading
        
        tmp = radians_to_degrees (transect_heading ) + magnetic_declination
        if tmp < 0:
            tmp += 360
        transect ['heading_wrt_magnetic_north'] = tmp
        transect ['length'] = transect_length
        transect ['edge'] = walk (center, transect_length, transect_heading)
        points = []
        
        
        for j in range (number_of_points_per_transect):
            new_point = {}
            distance = triangular (0, transect_length, transect_length)
            point = walk (center, distance, transect_heading)
            new_point['point']    = point
            new_point['heading']  = radians_to_degrees (transect_heading)
            new_point['distance'] = distance
            points.append (new_point)
        transect['points'] = sorted(points, key= lambda p: (p['distance']))
        result.append (transect)
    sorted_transects = sorted(result, key= lambda t: (t['heading']))
    transect_index, point_index = 0, 0
    
    
    for t in sorted_transects:
        transect_index += 1
        t['transect_id'] = transect_index
        t['team_letter'] = uppercase[transect_index - 1]
        for p in t['points']:
            point_index += 1
            p['point_id'] = point_index
            p['transect_id'] = transect_index
          
    
    if 1 == 0:
            asd = [a['heading_radians'] for a in sorted_transects] 
            print asd
            
            print "mean:"
            
            print circular_mean(asd)  
            print "nicely_distributed?"
            
            print nicely_distributed(asd)
            
            print "smallest difference:"
            print smallest_difference (asd)
    
    #import pdb
    #pdb.set_trace()
    return sorted_transects
    

@csrf_protect
@rendered_with('mammals/grid_block.html')
def grid_block(request):


    pick_transect_angles (10)




    default_lat = 41.400
    default_lon = -74.0305
    default_size = 250.0
    
    if (request.method != 'POST'):
        #does it really make sense to just do a get on grid square? not really.
        num_transects                           = 2
        points_per_transect                     = 2 
        height_in_blocks,  width_in_blocks,     = [22, 27]
        radius_of_circles                       = 0.0 # degrees
        magnetic_declination                    = -13.0 # degrees
        block_center                            = [default_lat, default_lon]
        block_size_in_m                         = default_size
        grid_center_y, grid_center_x            = [default_lat, default_lon]
        selected_block_center_y, selected_block_center_x = block_center
    else:
        num_transects        =                  get_int  ( request, 'num_transects',            2 )
        points_per_transect  =                  get_int  ( request, 'points_per_transect',      2 )
        radius_of_circles    =                  get_float( request, 'radius_of_circles',        30.0 )
        magnetic_declination =                  get_float( request, 'magnetic_declination',     -13.0 )
        block_size_in_m =                       get_float( request, 'block_size_in_m',        default_size)
        selected_block_center_y =               get_float( request, 'selected_block_center_y',  default_lat)
        selected_block_center_x =               get_float( request, 'selected_block_center_x',  default_lon)
        grid_center_y           =               get_float( request, 'grid_center_y',            default_lat)
        grid_center_x           =               get_float( request, 'grid_center_x',            default_lon)
        height_in_blocks =                      get_int( request,   'height_in_blocks',         21)
        width_in_blocks   =                     get_int( request,   'width_in_blocks',          27)
        block_center = selected_block_center_y, selected_block_center_x
        
        
    block_height, block_width    = to_lat_long (block_size_in_m,  block_size_in_m )
    
    transects = []
    transects = pick_transects (block_center, block_size_in_m, num_transects, points_per_transect, magnetic_declination)

    bottom_left = block_center[0] - (block_height / 2), block_center[1] - (block_width/2)
    block = set_up_block (bottom_left, block_height, block_width)

    return {
        'block_json': simplejson.dumps(block)
        ,'radius_of_circles'                         :  radius_of_circles # meters
        ,'magnetic_declination'                      :  magnetic_declination # degrees
        ,'points_per_transect'                       :  points_per_transect # meters
        ,'num_transects'                             :  num_transects # degrees
        ,'selected_block_center_y'                   :  selected_block_center_y
        ,'selected_block_center_x'                   :  selected_block_center_x
        ,'block_size_in_m'                           :  block_size_in_m
        ,'grid_center_y'                             :  grid_center_y
        ,'grid_center_x'                             :  grid_center_x
        ,'height_in_blocks'                          :  height_in_blocks
        ,'width_in_blocks'                           :  width_in_blocks
        ,'transects_json'                            :  simplejson.dumps(transects)
        ,'sandbox'                                   :  False
        ,'transects'                                 :  transects
    
    }
    
       
#@rendered_with('mammals/sandbox_grid_block.html')


@csrf_protect
@rendered_with('mammals/grid_block.html')
def sandbox_grid_block(request):
    default_lat = 41.400
    default_lon = -74.0305
    default_size = 250.0
    
    if (request.method != 'POST'):
        #does it really make sense to just do a get on grid square? not really.
        num_transects                           = 2
        points_per_transect                     = 2 
        height_in_blocks,  width_in_blocks,     = [3, 4]
        radius_of_circles                       = 0.0 # degrees
        magnetic_declination                    = -13.0 # degrees
        block_center                            = [default_lat, default_lon]
        block_size_in_m                         =  default_size
        grid_center_y, grid_center_x            = [default_lat, default_lon]
        selected_block_center_y, selected_block_center_x = block_center
    else:
        num_transects        =                  get_int  ( request, 'num_transects',            2 )
        points_per_transect  =                  get_int  ( request, 'points_per_transect',      2 )
        radius_of_circles    =                  get_float( request, 'radius_of_circles',        30.0 )
        magnetic_declination =                  get_float( request, 'magnetic_declination',     -13.0 )
        block_size_in_m =                       get_float( request, 'block_size_in_m',        default_size)
        selected_block_center_y =               get_float( request, 'selected_block_center_y',  default_lat)
        selected_block_center_x =               get_float( request, 'selected_block_center_x',  default_lon)
        grid_center_y           =               get_float( request, 'grid_center_y',            default_lat)
        grid_center_x           =               get_float( request, 'grid_center_x',            default_lon)
        height_in_blocks =                      get_int( request,   'height_in_blocks',         21)
        width_in_blocks   =                     get_int( request,   'width_in_blocks',          27)
        block_center = selected_block_center_y, selected_block_center_x
    
    block_height, block_width    = to_lat_long (block_size_in_m,  block_size_in_m )
    
    transects = []
    transects = pick_transects (block_center, block_size_in_m, num_transects, points_per_transect, magnetic_declination)

    bottom_left = block_center[0] - (block_height / 2), block_center[1] - (block_width/2)
    block = set_up_block (bottom_left, block_height, block_width)

    return {
        'block_json': simplejson.dumps(block)
        ,'radius_of_circles'                         :  radius_of_circles # meters
        ,'magnetic_declination'                      :  magnetic_declination # degrees
        ,'points_per_transect'                       :  points_per_transect # meters
        ,'num_transects'                             :  num_transects # degrees
        ,'selected_block_center_y'                   :  selected_block_center_y
        ,'selected_block_center_x'                   :  selected_block_center_x
        ,'block_size_in_m'                           :  block_size_in_m
        ,'grid_center_y'                             :  grid_center_y
        ,'grid_center_x'                             :  grid_center_x
        ,'height_in_blocks'                          :  height_in_blocks
        ,'width_in_blocks'                           :  width_in_blocks
        ,'transects_json'                            :  simplejson.dumps(transects)
        ,'sandbox'                                   :  True
        ,'transects'                                 :  transects
    
    }

