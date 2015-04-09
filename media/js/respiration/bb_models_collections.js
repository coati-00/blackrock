	var Species = BaseModel.extend({
	    urlRoot: '/'
	});

	var SpeciesCollection = BaseCollection.extend({
		model: Species,
	});
	
	var Scenario = BaseModel.extend({
	    urlRoot: '/',
	    
	    defaults: function() {
	    	  return {
	    	    species_list: []
	    	  }
	    }

	});

	var ScenarioCollection = BaseCollection.extend({	
		model: Scenario,
	});
	
