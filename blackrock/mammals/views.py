from blackrock.mammals.grid_math import to_lat_long, set_up_block, \
    pick_transect_angles, length_of_transect, radians_to_degrees, \
    walk_transect, minimum_distance_between_points, pick_new_distance, \
    hypotenuse, to_meters
from blackrock.mammals.models import GridSquare, \
    whether_this_user_can_see_mammals_module_data_entry, Sighting, Habitat, \
    Species, ObservationType, Expedition, GradeLevel, School, \
    ExpeditionMoonPhase, ExpeditionOvernightTemperature, \
    ExpeditionOvernightPrecipitation, ExpeditionOvernightPrecipitationType, \
    ExpeditionCloudCover, Illumination, AnimalSex, AnimalAge, \
    AnimalScaleUsed, Bait, TrapType, Animal
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator, InvalidPage, EmptyPage, \
    PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from re import match
from string import uppercase
import csv
from datetime import datetime
import json


def get_float(request, name, default):
    try:
        number = request.POST.get(name, default)
        return float(number)
    except ValueError:
        return default


def get_int(request, name, default):
    try:
        number = request.POST.get(name, default)
        return int(number)
    except ValueError:
        return default


class rendered_with(object):

    def __init__(self, template_name):
        self.template_name = template_name

    def __call__(self, func):
        def rendered_func(request, *args, **kwargs):
            items = func(request, *args, **kwargs)
            if isinstance(items, dict):
                return render_to_response(
                    self.template_name, items,
                    context_instance=RequestContext(request))
            else:
                return items
        return rendered_func


@csrf_protect
@rendered_with('mammals/login.html')
def mammals_login(request):
    return {}


@csrf_protect
def process_login(request):
    if (not ('username' in request.POST and
             'password' in request.POST)):
        return HttpResponseRedirect('/mammals/login/')

    if (request.GET):
        return HttpResponseRedirect('/mammals/login/')

    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None and user.is_active:
        login(request, user)
        return HttpResponseRedirect('/mammals/grid/')
    else:
        return HttpResponseRedirect('/mammals/login/')


@csrf_protect
@rendered_with('mammals/sandbox_grid.html')
def sandbox_grid(request):
    """"YES SANDBOX."""""
    default_lat = 41.400
    default_lon = -74.0305
    default_size = 15

    if (request.method != 'POST'):
        grid_center = [default_lat, default_lon]
        height_in_blocks, width_in_blocks, = [3, 4]
        block_size_in_m = default_size
        grid_center_y, grid_center_x = grid_center
    else:
        height_in_blocks = get_int(request, 'height_in_blocks', 21)
        width_in_blocks = get_int(request, 'width_in_blocks', 27)
        block_size_in_m = get_float(
            request, 'block_size_in_m', default_size)
        grid_center_y = get_float(request, 'grid_center_y', default_lat)
        grid_center_x = get_float(request, 'grid_center_x', default_lon)
        grid_center = grid_center_y, grid_center_x

    # we need a minimum block size.
    if block_size_in_m < 10:
        block_size_in_m = 10

    grid_height_in_m = block_size_in_m * height_in_blocks
    grid_width_in_m = block_size_in_m * width_in_blocks

    block_height, block_width = to_lat_long(
        block_size_in_m, block_size_in_m)
    grid_height, grid_width = to_lat_long(
        grid_height_in_m, grid_width_in_m)
    grid_bottom, grid_left = grid_center[
        0] - (grid_height / 2), grid_center[1] - (grid_width / 2)
    grid_json = []

    for i in range(0, height_in_blocks):
        for j in range(0, width_in_blocks):
            bottom_left = grid_bottom + i * \
                block_height, grid_left + j * block_width
            block = {}
            block['corner_obj'] = set_up_block(
                bottom_left, block_height, block_width)
            block['row'] = height_in_blocks - i
            block['column'] = width_in_blocks + j + 1
            # label them left-to-right, top-to-bottom:
            block['label'] = (
                height_in_blocks - i - 1) * width_in_blocks + j + 1
            grid_json.append(block)

    return {
        'grid_json': json.dumps(grid_json),
        'grid_center_y': grid_center_y,
        'grid_center_x': grid_center_x,
        'height_in_blocks': height_in_blocks,
        'width_in_blocks': width_in_blocks,
        'block_size_in_m': block_size_in_m,
        'sandbox': True
    }


@csrf_protect
@rendered_with('mammals/grid_block.html')
def sandbox_grid_block(request):
    """YES SANDBOX"""
    default_lat = 41.400
    default_lon = -74.0305
    default_size = 250.0

    if (request.method != 'POST'):
        # does it really make sense to just do a get on grid square? not
        # really.
        num_transects = 2
        points_per_transect = 2
        height_in_blocks, width_in_blocks, = [3, 4]
        magnetic_declination = -13.0  # degrees
        block_center = [default_lat, default_lon]
        block_size_in_m = default_size
        grid_center_y, grid_center_x = [default_lat, default_lon]
        selected_block_center_y, selected_block_center_x = block_center
    else:
        num_transects = get_int(request, 'num_transects', 2)
        points_per_transect = get_int(request, 'points_per_transect', 2)
        magnetic_declination = get_float(
            request, 'magnetic_declination', -13.0)
        block_size_in_m = get_float(request, 'block_size_in_m', default_size)
        selected_block_center_y = get_float(
            request, 'selected_block_center_y', default_lat)
        selected_block_center_x = get_float(
            request, 'selected_block_center_x', default_lon)
        grid_center_y = get_float(request, 'grid_center_y', default_lat)
        grid_center_x = get_float(request, 'grid_center_x', default_lon)
        height_in_blocks = get_int(request, 'height_in_blocks', 21)
        width_in_blocks = get_int(request, 'width_in_blocks', 27)
        block_center = selected_block_center_y, selected_block_center_x

    if num_transects > 20:
        num_transects = 20

    if points_per_transect > 4:
        points_per_transect = 4

    block_height, block_width = to_lat_long(
        block_size_in_m, block_size_in_m)

    transects = pick_transects(
        block_center, block_size_in_m, num_transects,
        points_per_transect, magnetic_declination)

    bottom_left = block_center[
        0] - (block_height / 2), block_center[1] - (block_width / 2)
    block = set_up_block(bottom_left, block_height, block_width)

    return {
        # degrees
        # meters
        # degrees
        'block_json': json.dumps(block),
        'magnetic_declination': magnetic_declination,
        'points_per_transect': points_per_transect,
        'num_transects': num_transects,
        'selected_block_center_y': selected_block_center_y,
        'selected_block_center_x': selected_block_center_x,
        'block_size_in_m': block_size_in_m,
        'grid_center_y': grid_center_y,
        'grid_center_x': grid_center_x,
        'height_in_blocks': height_in_blocks,
        'width_in_blocks': width_in_blocks,
        'transects_json': json.dumps(transects),
        'sandbox': True,
        'transects': transects,
        'show_save_button': False
    }


# RESEARCH_GRID:

@csrf_protect
@rendered_with('mammals/grid.html')
def grid(request):
    """"NOT SANDBOX."""""
    grid = [gs.info_for_display()
            for gs in GridSquare.objects.all() if gs.display_this_square]

    # TODO: remove
    # 'grid_center_y','grid_center_x','height_in_blocks','width_in_blocks'
    # ,'block_size_in_m'

    selected_block = None

    if 'selected_block_database_id' in request.POST:
        selected_block_database_id = int(
            request.POST.get('selected_block_database_id'))
        selected_block = GridSquare.objects.get(
            id=selected_block_database_id)

    return {
        # TODO: remove
        'grid_json': json.dumps(grid),
        'grid_center_y': 41.400,
        'grid_center_x': -74.0305,
        'height_in_blocks': 22,
        'width_in_blocks': 27,
        'block_size_in_m': 250.0,
        'selected_block': selected_block,
        'sandbox': False
    }


@csrf_protect
@rendered_with('mammals/grid_block.html')
def grid_block(request):
    """"NOT SANDBOX."""""
    default_lat = 41.400
    default_lon = -74.0305
    default_size = 250.0
    if (request.method != 'POST'):
        # does it really make sense to just do a get on grid square? not
        # really.
        return index(request)

    selected_block_database_id = int(
        request.POST.get('selected_block_database_id'))
    selected_block = GridSquare.objects.get(id=selected_block_database_id)

    num_transects = get_int(request, 'num_transects', 2)
    points_per_transect = get_int(request, 'points_per_transect', 2)
    magnetic_declination = get_float(request, 'magnetic_declination', -13.0)
    block_size_in_m = get_float(request, 'block_size_in_m', default_size)
    selected_block_center_y = get_float(
        request, 'selected_block_center_y', default_lat)
    selected_block_center_x = get_float(
        request, 'selected_block_center_x', default_lon)
    grid_center_y = get_float(request, 'grid_center_y', default_lat)
    grid_center_x = get_float(request, 'grid_center_x', default_lon)
    height_in_blocks = get_int(request, 'height_in_blocks', 21)
    width_in_blocks = get_int(request, 'width_in_blocks', 27)
    block_center = selected_block_center_y, selected_block_center_x
    block_height, block_width = to_lat_long(block_size_in_m, block_size_in_m)

    transects = pick_transects(
        block_center, block_size_in_m, num_transects,
        points_per_transect, magnetic_declination)

    bottom_left = block_center[
        0] - (block_height / 2), block_center[1] - (block_width / 2)
    block = set_up_block(bottom_left, block_height, block_width)

    if num_transects > 20:
        num_transects = 20

    if points_per_transect > 10:
        points_per_transect = 10

    can_enter_data = \
        whether_this_user_can_see_mammals_module_data_entry(request.user)

    return {
        # TODO: fix this -- incomplete refactor. These two variables refer to
        # exactly the same thing: the database ID of the square we selected.
        # END TODO
        # degrees
        # meters
        # degrees
        # TODO: remove; replace with the id of the selcted block.
        # TODO: remove
        'block_json': json.dumps(block),
        'show_save_button': can_enter_data,
        'sandbox': False,
        'selected_block_database_id': selected_block_database_id,
        'grid_square_id': selected_block_database_id,
        'magnetic_declination': magnetic_declination,
        'points_per_transect': points_per_transect,
        'num_transects': num_transects,
        'selected_block_center_y': selected_block_center_y,
        'selected_block_center_x': selected_block_center_x,
        'selected_block': selected_block,
        'transects_json': json.dumps(transects),
        'transects': transects,
        'block_size_in_m': block_size_in_m,
        'grid_center_y': grid_center_y,
        'grid_center_x': grid_center_x,
        'height_in_blocks': height_in_blocks,
        'width_in_blocks': width_in_blocks
    }


@rendered_with('mammals/index.html')
def index(request):
    return {}


@rendered_with('mammals/teaching_resources.html')
def teaching_resources(request):
    return {}


@rendered_with('mammals/help.html')
def help(request):
    return {}


def pick_transects(center, side_of_square, number_of_transects,
                   number_of_points_per_transect, magnetic_declination):
    result = []

    if number_of_transects > 20:
        number_of_transects = 20
    new_transects = pick_transect_angles(number_of_transects)
    for tr in new_transects:

        transect = {}
        transect_heading = tr
        transect_length = length_of_transect(transect_heading, side_of_square)
        transect['heading'] = radians_to_degrees(transect_heading)
        transect['heading_radians'] = transect_heading

        tmp = radians_to_degrees(transect_heading) + magnetic_declination
        if tmp < 0:
            tmp += 360
        transect['heading_wrt_magnetic_north'] = tmp
        transect['length'] = transect_length
        transect['edge'] = walk_transect(
            center, transect_length, transect_heading)
        points = []

        min_d = minimum_distance_between_points(
            transect_length, number_of_points_per_transect)

        for j in range(number_of_points_per_transect):
            new_point = {}
            distance = pick_new_distance(
                [p['distance'] for p in points], transect_length, min_d)

            point = walk_transect(center, distance, transect_heading)
            new_point['point'] = point
            new_point['heading'] = radians_to_degrees(transect_heading)
            new_point['distance'] = distance
            points.append(new_point)
        transect['points'] = sorted(points, key=lambda p: (p['distance']))
        result.append(transect)
    sorted_transects = sorted(result, key=lambda t: (t['heading']))
    transect_index, point_index = 0, 0
    for t in sorted_transects:
        transect_index += 1
        t['transect_id'] = transect_index
        t['team_letter'] = uppercase[transect_index - 1]
        point_index_2 = 0
        for p in t['points']:
            point_index += 1
            point_index_2 += 1
            p['point_id'] = point_index
            p['point_index_2'] = point_index_2
            p['transect_id'] = transect_index
    return sorted_transects


# CSV export:
def header_row():
    return [
        # , 'Bearing (true north)'
        # , 'Bearing (magnetic north)'
        # this is magnetig north only.
        # , 'Trap ID'
        'Team name', 'Trap number',
        'Bearing', 'Distance (m) from center', 'Latitude', 'Longitude'
        # , 'Location ID'
    ]


def row_to_output(point, transect):
    return [
        transect['team_letter'],
        point['point_index_2'],
        # , transect['heading']
        # , transect['heading_wrt_magnetic_north']
        # , "%s%d" % (transect['team_letter'] , point['point_index_2'] )
        transect['heading_wrt_magnetic_north'],
        point['distance'],
        point['point'][0],
        point['point'][1]
        # , point['point_id']
    ]


@csrf_protect
def grid_square_csv(request):
    transects_json = request.POST.get('transects_json')
    obj = json.loads(transects_json)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = \
        'attachment; filename=blackrock_transect_table.csv'
    writer = csv.writer(response)
    writer.writerow(header_row())
    for transect in obj:
        for point in transect['points']:
            writer.writerow(row_to_output(point, transect))
    return response


@user_passes_test(whether_this_user_can_see_mammals_module_data_entry,
                  login_url='/mammals/login/')
@rendered_with('mammals/sightings.html')
def sightings(request):
    if request.method != "GET":
        return HttpResponse('GET requests only, please.')
    pass

    sightings = Sighting.objects.all()
    return {'sightings': sightings}


@user_passes_test(whether_this_user_can_see_mammals_module_data_entry,
                  login_url='/mammals/login/')
@rendered_with('mammals/sighting.html')
def create_sighting(request):
    if request.method != "GET":
        return HttpResponse('GET requests only, please.')
    the_new_sighting = Sighting()
    the_new_sighting.save()
    return HttpResponseRedirect('/mammals/sighting/%d' % the_new_sighting.id)


@user_passes_test(whether_this_user_can_see_mammals_module_data_entry,
                  login_url='/mammals/login/')
@rendered_with('mammals/sighting.html')
@csrf_protect
def sighting(request, sighting_id):
    if request.method != "GET":
        return HttpResponse('GET requests only, please.')

    the_sighting = Sighting.objects.get(pk=sighting_id)

    return {
        'habitats': Habitat.objects.all(),
        'species': Species.objects.all(),
        'observation_types': ObservationType.objects.all(),
        'sighting': the_sighting,
    }


@user_passes_test(whether_this_user_can_see_mammals_module_data_entry,
                  login_url='/mammals/login/')
def edit_sighting(request):
    if request.method != "POST":
        return HttpResponse('POST requests only, please.')
    rp = request.POST
    the_sighting = Sighting.objects.get(pk=rp['sighting_id'])

    try:
        the_sighting.set_lat_long([float(rp['lat']), float(rp['lon'])])
    except ValueError:
        pass  # if it's empty  we don't care .

    try:
        date_list = [int(i) for i in rp['date'].split('/')]
        the_sighting.date = datetime(
            date_list[2], date_list[0], date_list[1])
    except:
        pass

    try:
        the_sighting.species = Species.objects.get(pk=rp['species_id'])
    except:
        pass

    try:
        the_sighting.habitat = Habitat.objects.get(pk=rp['habitat_id'])
    except:
        pass

    try:
        the_sighting.observation_type = ObservationType.objects.get(
            pk=rp['observation_type_id'])
    except:
        pass

    try:
        the_sighting.observers = rp['observers']
    except:
        pass

    try:
        the_sighting.notes = rp['notes']
    except:
        pass

    the_sighting.save()
    if rp['go_back'] == '':
        return HttpResponseRedirect('/mammals/sighting/%d' % the_sighting.id)
    else:
        return HttpResponseRedirect('/mammals/sightings/')


@user_passes_test(whether_this_user_can_see_mammals_module_data_entry,
                  login_url='/mammals/login/')
def new_expedition_ajax(request):
    if (request.method == "POST" and
        request.is_ajax and
        'transects_json' in request.POST and
            request.POST['transects_json'] != 'None'):
        transects_json = request.POST.get('transects_json')
        grid_square_id = request.POST.get('grid_square_id')
        obj = json.loads(transects_json)
        the_new_expedition = Expedition.create_from_obj(obj, request.user)
        the_new_expedition.grid_square = GridSquare.objects.get(
            id=grid_square_id)
        the_new_expedition.start_date_of_expedition = datetime.now()
        # TODO add timedelta (1 day) to the end.
        the_new_expedition.end_date_of_expedition = datetime.now()
        the_new_expedition.save()
    msg = '%d' % the_new_expedition.id
    return HttpResponse(msg)


@user_passes_test(whether_this_user_can_see_mammals_module_data_entry,
                  login_url='/mammals/login/')
@rendered_with('mammals/expedition.html')
def expedition(request, expedition_id):
    exp = Expedition.objects.get(id=expedition_id)
    grades = GradeLevel.objects.all()
    hours = [("%02d" % the_hour) for the_hour in range(0, 24)]
    minutes = [("%02d" % the_minute) for the_minute in range(0, 60)]
    exp.set_end_time_if_none()

    overnight_precipitations = ExpeditionOvernightPrecipitation.objects.all()
    precipitation_types = ExpeditionOvernightPrecipitationType.objects.all()

    return {
        'expedition': exp,
        'grades': grades,
        'schools': School.objects.all(),
        'moon_phases': ExpeditionMoonPhase.objects.all(),
        'overnight_temperatures': ExpeditionOvernightTemperature.objects.all(),
        'overnight_precipitations': overnight_precipitations,
        'overnight_precipitation_types': precipitation_types,
        'cloud_covers': ExpeditionCloudCover.objects.all(),
        'illuminations': Illumination.objects.all(),
        'hours': hours, 'minutes': minutes
    }


@rendered_with('mammals/expedition.html')
@user_passes_test(whether_this_user_can_see_mammals_module_data_entry,
                  login_url='/mammals/login/')
def edit_expedition(request, expedition_id):
    process_edit_expedition(request, expedition_id)
    return all_expeditions(request)


@user_passes_test(whether_this_user_can_see_mammals_module_data_entry,
                  login_url='/mammals/login/')
def edit_expedition_ajax(request):
    process_edit_expedition(request, request.POST['expedition_id'])
    msg = 'OK'
    return HttpResponse(msg)


@user_passes_test(whether_this_user_can_see_mammals_module_data_entry,
                  login_url='/mammals/login/')
def process_edit_expedition(request, expedition_id):

    exp = Expedition.objects.get(id=expedition_id)
    rp = request.POST

    if rp:
        if 'school' in rp and rp['school'] != 'None':
            exp.school_id = int(rp['school'])
        if 'school_contact_1_name' in rp:
            exp.school_contact_1_name = rp['school_contact_1_name']
        if 'school_contact_1_phone' in rp:
            exp.school_contact_1_phone = rp['school_contact_1_phone']
        if 'school_contact_1_email' in rp:
            exp.school_contact_1_email = rp['school_contact_1_email']

        if 'school_contact_1_email' in rp:
            exp.school_contact_1_email = rp['school_contact_1_email']

        if ('expedition_hour_string' in rp and
                'expedition_minute_string' in rp):
            exp.set_end_time_from_strings(
                rp['expedition_hour_string'], rp['expedition_minute_string'])

        if 'grade' in rp:
            exp.grade_level_id = int(rp['grade'])

        if 'number_of_students' in rp:
            try:
                exp.number_of_students = int(rp['number_of_students'])
            except ValueError:
                exp.number_of_students = 0

        if 'overnight_temperature_int' in rp:
            try:
                exp.overnight_temperature_int = int(
                    rp['overnight_temperature_int'])
            except ValueError:
                exp.overnight_temperature_int = 0

        exp.save()

        form_map_environment = {
            'moon_phase': 'moon_phase_id',
            'cloud_cover': 'cloud_cover_id',
            'overnight_temperature': 'overnight_temperature_id',
            'overnight_precipitation': 'overnight_precipitation_id',
            'overnight_precipitation_type': 'overnight_precipitation_type_id'
        }

        for the_key, thing_to_update in form_map_environment.iteritems():
            if the_key in rp:
                setattr(exp, thing_to_update, int(rp[the_key]))
                exp.save()


@csrf_protect
@rendered_with('mammals/expedition_animals.html')
@user_passes_test(whether_this_user_can_see_mammals_module_data_entry,
                  login_url='/mammals/login/')
def expedition_animals(request, expedition_id):
    exp = Expedition.objects.get(id=expedition_id)
    return {
        'expedition': exp,
        'sexes': AnimalSex.objects.all(),
        'species': Species.objects.all(),
        'ages': AnimalAge.objects.all(),
        'scales': AnimalScaleUsed.objects.all(),
        'schools': School.objects.all()
    }


@rendered_with('mammals/all_expeditions.html')
@user_passes_test(whether_this_user_can_see_mammals_module_data_entry,
                  login_url='/mammals/login/')
def all_expeditions(request):
    all_the_expeditions = Expedition.objects.filter(
        real=True).order_by('-start_date_of_expedition')
    results_per_page = 25
    paginator = Paginator(all_the_expeditions, results_per_page)
    page_num = request.GET.get('page', 1)
    try:
        expeditions = paginator.page(page_num)
    except PageNotAnInteger:
        # If in any doubt, deliver first page.
        expeditions = paginator.page(1)
    except InvalidPage:
        # If in any doubt, deliver first page.
        expeditions = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        expeditions = paginator.page(paginator.num_pages)
    return {
        'expeditions': expeditions,
    }


@csrf_protect
@user_passes_test(whether_this_user_can_see_mammals_module_data_entry,
                  login_url='/mammals/login/')
@rendered_with('mammals/team_form.html')
def team_form(request, expedition_id, team_letter):
    baits = Bait.objects.all()
    species = Species.objects.all()
    grades = GradeLevel.objects.all()
    habitats = Habitat.objects.all()
    trap_types = TrapType.objects.all()
    exp = Expedition.objects.get(id=expedition_id)
    team_points = exp.team_points(team_letter)
    student_names = team_points[0].student_names
    return {
        'expedition': exp,
        'baits': baits,
        'habitats': habitats,
        'grades': grades,
        'species': species,
        'trap_types': trap_types,
        'team_letter': team_letter,
        'team_points': team_points,
        'student_names': student_names
    }


def process_save_team_form(request):
    if request.method != 'POST':
        return HttpResponseRedirect('/mammals/all_expeditions/')

    rp = request.POST
    expedition_id = rp['expedition_id']
    exp = Expedition.objects.get(id=expedition_id)
    team_letter = rp['team_letter']
    the_team_points = exp.team_points(team_letter)

    form_map = {
        'habitat': 'habitat_id', 'bait': 'bait_id', 'trap_type': 'trap_type_id'
    }
    form_map_booleans = {
        'whether_a_trap_was_set_here': 'whether_a_trap_was_set_here',
        'bait_still_there': 'bait_still_there'
    }

    for point in the_team_points:
        if 'student_names' in rp:
            point.student_names = rp['student_names']
            point.save()

        for the_key, thing_to_update in form_map.iteritems():
            rp_key = '%s_%d' % (the_key, point.id)
            if rp_key in rp and rp[rp_key] != 'None':
                setattr(point, '%s' % thing_to_update, rp[rp_key])
                point.save()
        for the_key, thing_to_update in form_map_booleans.iteritems():
            rp_key = '%s_%d' % (the_key, point.id)
            if rp_key in rp and rp[rp_key] != 'None':
                setattr(point, '%s' %
                        thing_to_update, (rp[rp_key] == 'True'))
                point.save()

        rp_key = '%s_%d' % ('understory', point.id)
        if rp_key in rp and rp[rp_key] != 'None':
            point.understory = rp[rp_key]
            point.save()

        rp_key = '%s_%d' % ('notes_about_location', point.id)
        if rp_key in rp and rp[rp_key] != 'None':
            point.notes_about_location = rp[rp_key]
            point.save()

        # Deal with animals:
        animal_key = 'animal_%d' % (point.id)
        if animal_key in rp and rp[animal_key] != 'None':
            species_id = int(rp[animal_key])
            species = Species.objects.get(id=species_id)

            # TODO (icing ) here we assume that the animal has never been
            # trapped before.
            animal_never_trapped_before = True
            if animal_never_trapped_before:
                animal = Animal()
                animal.species = species
                animal.save()
            else:
                # Note, would be nice to have a foreign key to another Animal
                # denoting that this Animal is the same actual organism as the
                # other Animal, but recaptured at a later date and
                # aidentified by the same tag.
                # animal = find_already_tagged_animal_in_the_database_somehow()
                pass

            point.animal = animal
            point.save()
            animal.save()

        # Deal with actual latitude and longitude:
        # The burden of providing good data here rests on the front end.
        # If the actual lat and lon don't meet our data standards, we're simply
        # not going to use them.
        # 1) Do they both exist?
        # 2) Are they both accurate to 5 decimals?
        # 3) Are they within a certain distance of the original lat and lon (no
        # interest in points in another country.
        correcting_lat_lon = False
        match_string = '(\-)?(\d){2}\.(\d){5}'

        # if your coordinate string doesn't match the above, you have a nice
        # day.
        lat_key = 'actual_lat_%d' % point.id
        lon_key = 'actual_lon_%d' % point.id

        max_diff = 250.0  # meters
        min_diff = 1.0  # meters

        correcting_lat_lon = True

        if correcting_lat_lon and lat_key not in rp:
            correcting_lat_lon = False
        if correcting_lat_lon and lon_key not in rp:
            correcting_lat_lon = False
        if correcting_lat_lon and match(match_string, rp[lat_key]) is None:
            correcting_lat_lon = False
        if correcting_lat_lon and match(match_string, rp[lon_key]) is None:
            correcting_lat_lon = False

        if correcting_lat_lon:
            diff_lat = point.actual_lat() - float(rp[lat_key])
            diff_lon = point.actual_lon() - float(rp[lon_key])
            distance_to_corrected_point_in_meters = hypotenuse(
                *to_meters(diff_lat, diff_lon))
            if distance_to_corrected_point_in_meters > max_diff:
                correcting_lat_lon = False
                # distance_to_corrected_point_in_meters
        if (correcting_lat_lon and
                distance_to_corrected_point_in_meters < min_diff):
            correcting_lat_lon = False
            # distance_to_corrected_point_in_meters
        if correcting_lat_lon:
            point.set_actual_lat_long(
                [float(rp[lat_key]), float(rp[lon_key])])
            point.save()


@csrf_protect
@user_passes_test(whether_this_user_can_see_mammals_module_data_entry,
                  login_url='/mammals/login/')
def save_team_form(request):
    if request.method != 'POST':
        return HttpResponseRedirect('/mammals/all_expeditions/')
    rp = request.POST
    if len(rp) == 0:
        return HttpResponseRedirect('/mammals/all_expeditions/')

    expedition_id = rp['expedition_id']
    process_save_team_form(request)

    return expedition(request, expedition_id)


@user_passes_test(whether_this_user_can_see_mammals_module_data_entry,
                  login_url='/mammals/login/')
def save_team_form_ajax(request):
    process_save_team_form(request)
    msg = 'OK'
    return HttpResponse(msg)


@csrf_protect
@user_passes_test(whether_this_user_can_see_mammals_module_data_entry,
                  login_url='/mammals/login/')
def save_expedition_animals(request):
    if request.method != 'POST':
        return HttpResponseRedirect('/mammals/all_expeditions/')

    rp = request.POST
    expedition_id = rp['expedition_id']
    exp = Expedition.objects.get(id=expedition_id)

    booleans = ['scat_sample_collected', 'blood_sample_collected',
                'skin_sample_collected', 'hair_sample_collected', 'recaptured']
    menus = ['sex', 'age', 'scale_used']  # these are

    for point in exp.animal_locations():
        for b in booleans:
            rp_key = '%s_%d' % (b, point.id)
            if rp_key in rp and rp[rp_key] == 'True':
                setattr(point.animal, b, True)
            else:
                setattr(point.animal, b, False)

        for m in menus:
            rp_key = '%s_%d' % (m, point.id)
            if rp_key in rp and rp[rp_key] is not None:
                setattr(point.animal, '%s_id' % m, rp[rp_key])

        rp_key = 'health_%d' % point.id
        if rp_key in rp and rp[rp_key] != '':
            setattr(point.animal, 'health', rp[rp_key])

        rp_key = 'weight_in_grams_%d' % point.id
        if rp_key in rp and rp[rp_key] != '':
            try:
                setattr(
                    point.animal, 'weight_in_grams', int(float(rp[rp_key])))
            except ValueError:
                pass  # not throwing a 500 for this, sorry.

        rp_key = 'tag_number_%d' % point.id
        if rp_key in rp and rp[rp_key] != '':
            setattr(point.animal, 'tag_number', rp[rp_key])
        point.animal.save()

        rp_key = 'delete_%d' % point.id
        if rp_key in rp and rp[rp_key] == 'delete':
            point.animal.delete()

    return expedition(request, expedition_id)


@csrf_protect
@rendered_with('mammals/grid_square_print.html')
def grid_square_print(request):

    transects_json = request.POST.get('transects_json')
    if request.method != 'POST':
        return HttpResponseRedirect('/mammals/')

    result = {
        'transects_json': transects_json,
        'transects': json.loads(transects_json),
        'selected_block_center_y': request.POST.get('selected_block_center_y'),
        'selected_block_center_x': request.POST.get('selected_block_center_x')
    }

    # only for the research version:
    if 'selected_block_database_id' in request.POST:
        selected_block_database_id = int(
            request.POST.get('selected_block_database_id'))
        selected_block = GridSquare.objects.get(
            id=selected_block_database_id)
        result['selected_block'] = selected_block

    return result
