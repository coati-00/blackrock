from math import cos, sin, sqrt, atan2, pi
from random import uniform

# http://en.wikipedia.org/wiki/World_Geodetic_System
# http://home.online.no/~sigurdhu/Grid_1deg.htm
# according to WGS 84:
# Latitude	   minute of latitude   minute of longitude
# 41 deg       1850.90              1402.25	

one_lat_degree  = 111054.0
one_long_degree = 84135.0

def meters_to_degrees_lat (y):
    return y / one_lat_degree
    
def meters_to_degrees_long (x):
    return x / one_long_degree

def degrees_lat_to_meters (dly):
    return dly * one_lat_degree
    
def degrees_long_to_meters(dlx):
    return dlx * one_long_degree

def to_lat_long_point (p):
    return to_lat_long (p[0], p[1])

def to_lat_long (y, x):
    return meters_to_degrees_lat (y), meters_to_degrees_long  (x)

def to_meters  (y, x):
    return degrees_lat_to_meters (y), degrees_long_to_meters  (x)

def to_meters_point (p):
    return to_meters (p[0], p[1])

def degrees_to_radians(angle):
    return angle * pi / 180.0 

def hypotenuse (x, y):
    return sqrt( x ** 2 + y ** 2 )


def walk (start_point, meters, heading):
    """ Returns the lat and long of where you get after walking x meters from a starting point following a certain heading. Heading is assumed to be in radians clockwise from north."""
    
    y, x = to_meters_point (start_point)
    return to_lat_long( y + cos(heading) * meters, x + sin(heading) * meters)

def to_heading (angle_in_radians):
    """converts to counterclockwise from east (trig standard) to clockwise from north (map standard)"""
    a = (pi / 2) - angle_in_radians
    if a < 0:
        a += 2 * pi
    return a

def length_of_transect (heading_in_radians, side_of_square):
    """Returns the length of a line connecting the center of a square to its side."""
    #headings are in radians measured clockwise from north.
    a = to_heading (heading_in_radians)
    s = side_of_square / 2
    for q in [1, 3, 5, 7, 9]:
        if a < (q * pi / 4):
            return  s / cos(a - (q - 1) * (pi / 4))


def pick_transect_heading():
    return uniform(0,  pi * 2)


#def pick_transect_headings(how_many):
#    return uniform(0,  pi * 2)


#angles are meant to be in radians
def circular_mean(angles):
    x = y = 0.
    for angle in angles:
        x += cos(angle)
        y += sin(angle)
    result =  atan2(y, x)
    if result < 0:
        result += 2*pi
    return result

def angle_difference (x, y):
    return min((2 * pi) - abs(x - y), abs(x - y))


def smallest_difference (asd):        
    return min (angle_difference(asd[a], asd[a+1]) for a in range (len(asd) - 1))


def nicely_distributed (angles):
    #print "............."
    mean = circular_mean(angles)
    sum_of_diffs = 0
    for a in angles:
        sum_of_diffs += angle_difference (mean, a)
        
    if sum_of_diffs  / len(angles) < 0.5:
        #print "these are all pointing in one direction."
        return False
    
    #import pdb
    #pdb.set_trace()
    
    ideal_angle = 2*pi / len(angles)
    
    #print "ideal angle"
    #print ideal_angle
    
    #print "ideal angle / 5"
    #print ideal_angle / 5
    
    #print "smallest_difference"
    #print smallest_difference(angles)
    
    return smallest_difference(angles) > ideal_angle / 5
    

def pick_transect_angles (number_needed):
    #import pdb
    #pdb.set_trace()
    number_of_tries = 10
    for a in range (number_of_tries):
        transects = [pick_transect_heading() for n in range(number_needed)]
        #print transects
        #print nicely_distributed(transects)
        if nicely_distributed(transects) or a == number_of_tries:
            return transects


def radians_to_degrees(angle):
    a = angle * 180.0 / pi
    if a < 0:
        a += 360.0
    return a

    
def rotate_points( points, center, angle):
    result = []
    for point in points:
        result.append (rotate_about_a_point(point, center, angle))
    return result
    
def rotate_about_a_point(point, center, angle_to_rotate):
    """ This is no longer used."""
    if angle_to_rotate == 0:
        return point
    
    if point[0] == center [0] and point[1] == center [1]:
        return point
        
    a = degrees_to_radians (angle_to_rotate)
    y, x =               to_meters_point (point)
    center_y, center_x = to_meters_point(center)
    
    delta_y = center_y - y
    delta_x = center_x - x
    r = hypotenuse (delta_x, delta_y)
    new_angle = atan2 (delta_x , delta_y) + a
    
    return to_lat_long( center_y + cos(new_angle) * r, center_x + sin(new_angle) * r)
    
def set_up_block (bottom_left, height, width):
    """
    Return a quincunx of lat/long points arranged as follows:
    
    1       2
    
        4        
    
    0       3
    
    """   
    box = [list()] * 5
    for i in range(len(box)):
        box[i] = list(bottom_left)
    #move the y for 1 and 2 right by one block width:
    box[1][0] += height
    box[2][0] += height
    # move the x for 2 and 3 right by one block width:
    box[2][1] += width
    box[3][1] += width
    #move the center up and right half a width:
    box[4][0] += height /  2
    box[4][1] += width  /  2
    return box
    

