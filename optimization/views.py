from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.template import RequestContext
from django.shortcuts import render_to_response
from blackrock.optimization.models import Tree, Plot
import csv, math, random, sets

NE_corner = 'POINT(-74.025 41.39)'
MULTIPLIER = 0.001   # to convert meters into degrees

def index(request, admin_msg=""):
  return render_to_response('optimization/index.html',
                            context_instance=RequestContext(request))
                            
def run(request):
  return render_to_response('optimization/run.html')
  
def calculate(request):
  if request.method != 'POST':
    return HttpResponseRedirect("/respiration/")

  num_plots = int(request.REQUEST['numPlots'])
  shape = request.REQUEST['shape']
  diameter = float(request.REQUEST['diameter'])

  parent = Plot.objects.get(name="Mount Misery Plot")
  results = {}

  plot_results = {}
  total_time = 0
  results['sample-area'] = 0
  species_list = sets.Set()
  results['sample-count'] = 0
  intermed_dbh = 0
  results['sample-dbh'] = 0
  density_list = []
  results['sample-density'] = 0
  basal_list = []
  results['sample-basal'] = 0
  dbh_list = []

  for plot in range(num_plots):
    sub = sample_plot(shape, diameter, parent)

    total_time += sub['time-total']
    results['sample-area'] += sub['area']
    # TODO: sample variance density
    # TODO: sample variance basal area
    species_list = species_list.union(sub['species-list'])
    results['sample-count'] += sub['count']
    intermed_dbh += sub['dbh'] * sub['count']   # weighted sum, to be used for average

    results['sample-density'] += sub['density']
    density_list.append(sub['density'])

    results['sample-basal'] += sub['basal']
    basal_list.append(sub['basal'])

    # sample variance dbh
    trees = sub['trees']
    for tree in trees:
      dbh_list.append(float(tree.dbh))
    sub['trees'] = ''

    sub['species-list'] = ""
    plot_results[plot] = sub

  results['plots'] = plot_results
  
  if total_time > 59:
    results['sample-time'] = "%dh %dm" % (total_time / 60, total_time % 60)
  else:
    results['sample-time'] = "%dm" % total_time
  results['sample-species'] = len(species_list)
  
  results['sample-area'] = round2(results['sample-area'])

  ## sample mean dbh ##
  if results['sample-count'] > 0:
    results['sample-dbh'] = round2( intermed_dbh / results['sample-count'] )
  else:
    results['sample-dbh'] = 0

  ## sample mean basal area ##
  results['sample-basal'] = round2( results['sample-basal'] / num_plots ) # average

  ## sample mean density ##
  results['sample-density'] = round2( results['sample-density'] / num_plots ) # average

  ## sample variance dbh ##
  results['sample-variance-dbh'] = round2( variance(dbh_list, results['sample-dbh'], results['sample-count']-1) )

  ## sample variance density ##
  results['sample-variance-density'] = round2( variance(density_list, results['sample-density'], num_plots-1) )

  ## sample variance basal area ##
  results['sample-variance-basal'] = round2( variance(basal_list, results['sample-basal'], num_plots-1) )

  # actual forest stats
  results['actual-area'] = round2(parent.area)
  results['actual-species'] = int(parent.num_species)
  results['actual-count'] = int(parent.tree_set.count())
  results['actual-dbh'] = round2(parent.mean_dbh)
  results['actual-density'] = round2( float(parent.density) )
  results['actual-basal'] = round2( float(parent.basal) )
  results['actual-variance-dbh'] = round2( float(parent.variance_dbh) )
  
  return HttpResponse(str(results), mimetype="application/javascript")
  
  
def sample_plot(shape, dimensions, parent):
  results = {}
  
  ## determine plot ##
  # terrible, awful, ugly hack for now
  trees = None
  x = 0
  y = 0
  if shape == 'square':
    # pick a random NE corner
    # range = 0 - 200-dimensions
    x = random.randint(0, 200-dimensions)
    y = random.randint(0, 200-dimensions)
    dimensions_deg = MULTIPLIER * dimensions
    x_deg = MULTIPLIER * x
    y_deg = MULTIPLIER * y
    sample = 'POLYGON ((%s %s, %s %s, %s %s, %s %s, %s %s))' \
              % (parent.NE_corner.x - x_deg, parent.NE_corner.y - y_deg, \
                 parent.NE_corner.x - x_deg - dimensions_deg, parent.NE_corner.y - y_deg, \
                 parent.NE_corner.x - x_deg - dimensions_deg, parent.NE_corner.y - y_deg - dimensions_deg, \
                 parent.NE_corner.x - x_deg, parent.NE_corner.y  - y_deg - dimensions_deg, \
                 parent.NE_corner.x - x_deg, parent.NE_corner.y - y_deg,                 
                 )
    trees = Tree.objects.filter(location__contained=sample)
  if shape == 'circle':
    # pick a random center point
    # range = dimensions - 200-dimensions
    x = random.randint(dimensions, 200-dimensions)
    y = random.randint(dimensions, 200-dimensions)
    x_deg = parent.NE_corner.x - x * MULTIPLIER
    y_deg = parent.NE_corner.y - y * MULTIPLIER
    center_pt = 'POINT (%s %s)' % (x_deg, y_deg)
    trees = Tree.objects.filter(location__dwithin=(center_pt, dimensions * MULTIPLIER))
 
  results['trees'] = trees
 
  ## number of trees in plot ##
  results['count'] = int(trees.count())

  ## unique species ##
  results['species-list'] = sets.Set([tree.species for tree in trees])
  results['num-species'] = len(results['species-list'])

  ## mean dbh ##
  dbhs = [float(tree.dbh) for tree in trees]
  dbh_sum = sum(dbhs)
  if trees.count() > 0:
    results['dbh'] = round2( dbh_sum / trees.count() )
  else:
    results['dbh'] = 0

  ## dbh variance ##
  results['variance-dbh'] = round2( variance(dbhs, results['dbh'], results['count']-1) )
    
  ## area ##
  if shape == 'square':
    results['area'] = round2(dimensions * dimensions)
  else:
    results['area'] = round2(math.pi * dimensions * dimensions)

  ## basal area ##
  results['basal'] = round2( (float(dbh_sum) * 0.785398) / float(results['area']) )

  ## density ##
  results['density'] = round2( (trees.count() * 10000) / results['area'] )

  ## time penalty ##

  # travel: 3 minutes per 100m (TODO: from NE corner? from previous plot?)
  travel_distance = math.sqrt(x**2 + y**2)
  results['time-travel'] = round((travel_distance / 100) * 3)

  # locating a plot - 3 minutes per plot
  results['time-locate'] = 3

  # establishing plot boundaries (shape) - square = 5min, circle = 1.5min
  if shape == "square":
    results['time-establish'] = 5
  else:
    results['time-establish'] = 1.5

  # establishing plot boundaries (size) - larger plots take longer
  # (fudging at 1 minute per meter of diameter for now)
  results['time-establish'] += dimensions
  
  # measuring trees in the plot - 30 seconds per tree
  results['time-measure'] = .5 * results['count']
  
  results['time-total'] = results['time-travel'] + results['time-locate'] \
                        + results['time-establish'] + results['time-measure']
                        

  ## species results
  species_totals = {}
  i = 0
  for species in results['species-list']:
    #print species

    tree_count = len([tree.id for tree in trees if tree.species == species])
    #print tree_count
    
    species_totals[i] = {'name':species, 'count':tree_count}
    i += 1
  #results['species-totals'] = species_totals
  #species = {}
  #for tree in trees:
  # try:
  #   species[tree.species] += 1
  #  except:
  #    species[tree.species] = 1
  #results['species'] = species
                        
  return results


def round2(value):
  return round(value * 100) / 100

def variance(values, mean, population_size):
  if population_size < 1:
    return 0

  variance_sum = 0
  for value in values:
    variance_sum += (float(value) - mean)**2
  return variance_sum / population_size
  
def loadcsv(request):
  if request.method == 'POST':
    
    fh = request.FILES['csvfile']
    if file == '':
      # TODO: error checking (correct file type, etc.)
      return HttpResponseRedirect(request.build_absolute_uri("./"))

    # delete existing
    Plot.objects.all().delete()
    Tree.objects.all().delete()
    
    p = Plot(name="Mount Misery Plot", NE_corner=NE_corner, area=40000)
    p.save()

    table = csv.reader(fh)
    header = table.next()
    
    for i in range(len(header)):
      h = header[i].lower()
      if h == 'id':
        id_idx = i
      elif h == 'species':
        species_idx = i
      elif h == 'x':
        x_idx = i
      elif h == 'y':
        y_idx = i
      elif h == 'dbh':
        dbh_idx = i
      else:
        return HttpResponse("Unsupported header %s" % h)
      
    for row in table:
       id = row[id_idx]
       species = row[species_idx]
       x = float(row[x_idx])
       y = float(row[y_idx])
       dbh = row[dbh_idx]
       xloc = p.NE_corner.x - (MULTIPLIER * x)
       yloc = p.NE_corner.y - (MULTIPLIER * y)
       loc = 'POINT(%f %f)' % (xloc, yloc)  # TODO real location data
       tree = Tree.objects.get_or_create(id=id, location=loc, species=species, dbh=dbh, plot=p)

    p.precalc()
    return HttpResponseRedirect("/optimization/")

def test(request):
  trees = Tree.objects.all()
  plot = Plot.objects.get(name="Mount Misery Plot")
  #sample = sample_plot("square", 5, plot)['sample']
  return render_to_response("optimization/test.html", {'trees':trees})#, 'sample':sample})
