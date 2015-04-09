/* Should questions be initiated with a first/empty species/scenario? Or should that be done in the view?
 * 
 * 
 * */

var App = { 
	Models: {}, 
	Collections: {}, 
	Views:{}
};


App.Models.Species = Backbone.Model.extend({});

App.Collections.SpeciesCollection = Backbone.Collection.extend({
	model: App.Models.Species,
});

App.Models.Scenario = Backbone.Model.extend({
	
    defaults: function() {
        return {
    	    /* Should I be using 'this' or is that done automatically because it is a default? */
    		scenarioName: 'Scenario Name',
    		numSpecies: 0,
    		speciesList: new App.Collections.SpeciesCollection(),
    	}
    }
    
});


App.Collections.ScenarioCollection = Backbone.Collection.extend({
	/* Will probably have to override create or add event so that
	 * the number of scenarios is auto incremented */
	
	model: App.Models.Scenario,
	
    defaults: function() {
  	  return {
  		numScenarios: 0
	  }
    }

});


App.Views.Species = Backbone.View.extend({

	events: {
	    'click .delete': 'remove',
	    'click .scenario-species-row .name_info .dropdown-menu .species-predefined-choice': 'selectSpecies'
	  },
	
	initialize: function(options){
		_.bindAll(this, 'render', 'insert', 'remove');
		this.template = _.template(jQuery("#leaf-species-template").html());
		if (options && 'container' in options) {
			this.container = options.container;
			this.insert();
		}
		this.listenTo(this.model, 'change', this.render);
	},

	render: function () {
        this.$el.html(this.template(this.model.attributes));
        return this;
    },

    insert: function(){
		this.container.append(this.$el);
	},
	
	remove: function() {
	    this.model.destroy();
	},
	
	selectSpecies: function(event) {
		var tree_id = event.currentTarget.attributes['data-id'].value;
		/* Shouldn't be relying on a global variable here... should be passing in or something */
		var cpy_tree = App.PredefinedSpecies.get(tree_id).clone();
		this.model.set({'id': cpy_tree.get('id'), 'label' : cpy_tree.get('label'),
			            't0' : cpy_tree.get('t0'), 'k' :  cpy_tree.get('k'),
			            'r0' : cpy_tree.get('r0'), 'e0' : cpy_tree.get('e0')});
	}

});

App.Views.Scenario = Backbone.View.extend({
	
	events: {
	    'click .scenario-row .deleteScenario': 'remove',
	    /* Do we want to leave functionality as is? Where it adds a row and then user selects species or what? */
	    'click .species-table-header .dropdown-menu .species-predefined-choice': 'addSpeciesRow'
	  },
	
	initialize: function(options){
		_.bindAll(this, 'render', 'remove');
		this.template = _.template(jQuery("#scenario-template").html());
		if (options && 'container' in options) {
			this.container = options.container;
			this.insert();
		}

	},
	
	render: function() { 
		
		// why would someone put a dollar sign in front of a variable?
		var num_of_species = this.model.get('numSpecies');
		if(num_of_species > 0) {
			// remove current species rows
		    var species_container = this.$('.species-table-body .species-row-container').empty();
			this.model.speciesList.each(function(species) { 
			    new App.Views.Species(
					{ model: species, container: species_container }
					).render(); 
		    });
		}
		else {
	        this.$el.html(this.template(this.model.attributes));
	        var species_container = this.$('.species-table-body .species-row-container').empty();
	        var tree_here = new App.Models.Species({   
	            'id': "ue_id",
	            'label' : 'Tree Species',
	            't0' : 10,
	            'k' :  283.15,
	            'r0' : 0.602,
	            'e0' : 43140
	        });
	        this.$('.species-table-body').append(
	        	new App.Views.Species({ model: tree_here, container: species_container  }).render());
	        
	        return this;
		}
	},
	
    insert: function(){
		this.container.append(this.$el);
	},
	
	remove: function() {
		/* I assume I will have to do this in a custom way so it removes the inner collection */
	    this.model.destroy();
	},
	
	addSpeciesRow: function(event) {
		var tree_id = event.currentTarget.attributes['data-id'].value;
		/* Shouldn't be relying on a global variable here... should be passing in or something */
		var cpy_tree = App.PredefinedSpecies.get(tree_id).clone();
		var species_container = this.$('.species-table-body .species-row-container');
        this.$('.species-table-body').append(
        	new App.Views.Species({ model: cpy_tree, container: species_container  }).render()); 
        return this;
	}
	
});

//App.Views.SpeciesCollection = Backbone.Views.extend({});
App.Views.ScenarioManagementView = Backbone.View.extend({
	

});

/* Need some kind of management view to co-ordinate collections and graphs */
/* In old code scenario module has     
 * initYearHelper();
    updateColors();
    all other functionality is here
    */
App.Views.RespirationGraphManagementView = Backbone.View.extend({
	

});


jQuery(function(){
	
	App.PredefinedSpecies = new App.Collections.SpeciesCollection();

	/* Add some predefined species */
	App.PredefinedSpecies.add([
	    new App.Models.Species({   
	        'id': "quercus_rubra",
	        'label' : 'Quercus rubra',
	        't0' : 10,
	        'k' :  283.15,
	        'r0' : 0.602,
	        'e0' : 43140
	    }),
	    new App.Models.Species({   
	        'id': "quercus_prinus",
	        'label' : 'Quercus prinus',
	        't0' : 10,
	        'k' :  283.15,
	        'r0' : 0.670,
	        'e0' : 37005
	    }),
	    new App.Models.Species({   
	        'id': "acer_rubrum",
	        'label' : 'Acer rubrum',
	        't0' : 10,
	        'k' :  283.15,
	        'r0' : 0.680,
	        'e0' : 27210
	   }),
	   new App.Models.Species({   
	        'id': "vaccinium_corymbosum",
	        'label' : 'Vaccinium corymbosum',
	        't0' : 10,
	        'k' :  283.15,
	        'r0' : 0.091,
	        'e0' : 62967
	   }),
	   new App.Models.Species({   
	        'id': "berberis_thumbergii",
	        'label' : 'Berberis thumbergii',
	        't0' : 10,
	        'k' :  283.15,
	        'r0' : 0.203,
	        'e0' : 81950
	   }),
	   new App.Models.Species({   
	        'id': "kalmia_latifolia",
	        'label' : 'Kalmia latifolia',
	        't0' : 10,
	        'k' :  283.15,
	        'r0' : 0.308,
	        'e0' : 54940
        }),
        new App.Models.Species({   
        	'id': "carya_glabra",
            'label' : 'Carya glabra',
            't0' : 10,
            'k' :  283.15,
            'r0' : 0.134,
            'e0' : 70547.5
        }),
        new App.Models.Species({   
        	'id': "liriodendron_tulipifera",
            'label' : 'Liriodendron tulipifera',
            't0' : 10,
            'k' :  283.15,
            'r0' : 0.187,
            'e0' : 60620.0
        }),
        new App.Models.Species({   
        	'id': "platanus_occidentalis",
            'label' : 'Platanus occidentalis',
            't0' : 10,
            'k' :  283.15,
            'r0' : 0.320,
            'e0' : 56336.7
        }),
        new App.Models.Species({   
        	'id': "betula_papyrifera",
            'label' : 'Betula papyrifera',
            't0' : 10,
            'k' :  283.15,
            'r0' : 0.357,
            'e0' : 45322.0
        }),
        new App.Models.Species({   
        	'id': "populus_tremuloides",
            'label' : 'Populus tremuloides',
            't0' : 10,
            'k' :  283.15,
            'r0' : 0.424,
            'e0' : 52261.3
        }),
        new App.Models.Species({   
        	'id': "populus_grandidentata",
            'label' : 'Populus grandidentata',
            't0' : 10,
            'k' :  283.15,
            'r0' : 0.294,
            'e0' : 59425.5
        }),
        new App.Models.Species({   
        	'id': "betula_lenta",
            'label' : 'Betula lenta',
            't0' : 10,
            'k' :  283.15,
            'r0' : 0.162,
            'e0' : 54267.7
        })
    ]);
	
	
	App.TestSpecies = new App.Models.Species({   
        'id': "unique_id",
        'label' : 'Quercus rubra',
        't0' : 10,
        'k' :  283.15,
        'r0' : 0.602,
        'e0' : 43140
    });

//	App.TestSpeciesView = new App.Views.Species({ model: App.TestSpecies, el: jQuery('.species-view-test')}).render();
//	//App.TestScenarioView = new App.Views.Scenario();
//	
//	App.TestScenario = new App.Models.Scenario({});
//
	App.TestScenarioView = new App.Views.Scenario({ model: App.TestScenario, el: jQuery('.scenario-view-test')}).render();
	
	
});
