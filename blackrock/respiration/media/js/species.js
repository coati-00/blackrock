var Blackrock = { 
    Models: {}, 
    Collections: {}, 
    Views:{}
}

Blackrock.Models.Species = Backbone.Model.extend({});

Blackrock.Collections.SpeciesCollection = Backbone.Collection.extend({
    model: Blackrock.Models.Species,
});

Blackrock.Views.Species = Backbone.View.extend({

    events: {
        'click .delete': 'remove',
        'click .species-select-predefined': 'showSpecies',
        'click .species-predefined-choice': 'selectSpecies'
        //'click .scenario-species-row .name_info .dropdown-menu .species-predefined-choice': 'selectSpecies'
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

    showSpecies: function(event) {
        var this_list = jQuery(this.el).find('.species-predefined-list').show();
        //event.currentTarget.attributes['data-id'].value;
        /* Shouldn't be relying on a global variable here... should be passing in or something */
    },
    
    selectSpecies: function(event) {
        var tree_id = event.currentTarget.attributes['data-id'].value;
        /* Shouldn't be relying on a global variable here... should be passing in or something */
        var cpy_tree = Blackrock.PredefinedSpecies.get(tree_id).clone();
        this.model.set({'id': cpy_tree.get('id'), 'label' : cpy_tree.get('label'),
                        't0' : cpy_tree.get('t0'), 'k' :  cpy_tree.get('k'),
                        'r0' : cpy_tree.get('r0'), 'e0' : cpy_tree.get('e0')});
        //var this_values = jQuery(this.el).find('.species-predefined-list').show();
    }

});

Blackrock.Views.LeafGraphManagementView = Backbone.View.extend({
      events: {
        //'click .scenario-row .deleteScenario': 'remove',
        /* Do we want to leave functionality as is? Where it adds a row and then user selects species or what? */
        'click .addLeafSpecies' : 'addSpeciesRow'
      },

        initialize: function(options){
            _.bindAll(this, 'renderCollection');
        //_.bindAll(this, 'render', 'insert', 'remove');
        this.template = _.template(jQuery("#leaf-left-bb-pane-template").html());
        this.collection_container = $el.jQuery(".leafspeciescontainer");
        this.item_view = Blackrock.Views.Species;
        this.collection = new Blackrock.Collections.SpeciesCollection();
        // if (options && 'container' in options) {
        //     this.container = options.container;
        //     this.insert();
        // }
        //this.listenTo(this.model, 'change', this.render);
    },
    // global.addSpecies = addSpecies;
    // global.delSpecies = delSpecies;
    // global.getNumSpecies = getNumSpecies;
    // global.incNumSpecies = incNumSpecies;
    // global.getSpeciesList = getSpeciesList;
    // global.setSpeciesList = setSpeciesList;
    renderCollection: function() {
        this.collection.each(function(model)
        {
            this.$el.append(new this.item_view({
                model: model
            }).render().el);
        }, this);
        return this;
    }//,
    
    // addItem: function(model, collection, options)
    // {
    //     this.$el.append(new this.item_view({
    //         model: model
    //     }).render().el);
    // }
});


jQuery(function(){
    
    Blackrock.PredefinedSpecies = new Blackrock.Collections.SpeciesCollection();

    /* Add some predefined species */
    Blackrock.PredefinedSpecies.add([
        new Blackrock.Models.Species({   
            'id': "quercus_rubra",
            'label' : 'Quercus rubra',
            't0' : 10,
            'k' :  283.15,
            'r0' : 0.602,
            'e0' : 43140
        }),
        new Blackrock.Models.Species({   
            'id': "quercus_prinus",
            'label' : 'Quercus prinus',
            't0' : 10,
            'k' :  283.15,
            'r0' : 0.670,
            'e0' : 37005
        }),
        new Blackrock.Models.Species({   
            'id': "acer_rubrum",
            'label' : 'Acer rubrum',
            't0' : 10,
            'k' :  283.15,
            'r0' : 0.680,
            'e0' : 27210
       }),
       new Blackrock.Models.Species({   
            'id': "vaccinium_corymbosum",
            'label' : 'Vaccinium corymbosum',
            't0' : 10,
            'k' :  283.15,
            'r0' : 0.091,
            'e0' : 62967
       }),
       new Blackrock.Models.Species({   
            'id': "berberis_thumbergii",
            'label' : 'Berberis thumbergii',
            't0' : 10,
            'k' :  283.15,
            'r0' : 0.203,
            'e0' : 81950
       }),
       new Blackrock.Models.Species({   
            'id': "kalmia_latifolia",
            'label' : 'Kalmia latifolia',
            't0' : 10,
            'k' :  283.15,
            'r0' : 0.308,
            'e0' : 54940
        }),
        new Blackrock.Models.Species({   
            'id': "carya_glabra",
            'label' : 'Carya glabra',
            't0' : 10,
            'k' :  283.15,
            'r0' : 0.134,
            'e0' : 70547.5
        }),
        new Blackrock.Models.Species({   
            'id': "liriodendron_tulipifera",
            'label' : 'Liriodendron tulipifera',
            't0' : 10,
            'k' :  283.15,
            'r0' : 0.187,
            'e0' : 60620.0
        }),
        new Blackrock.Models.Species({   
            'id': "platanus_occidentalis",
            'label' : 'Platanus occidentalis',
            't0' : 10,
            'k' :  283.15,
            'r0' : 0.320,
            'e0' : 56336.7
        }),
        new Blackrock.Models.Species({   
            'id': "betula_papyrifera",
            'label' : 'Betula papyrifera',
            't0' : 10,
            'k' :  283.15,
            'r0' : 0.357,
            'e0' : 45322.0
        }),
        new Blackrock.Models.Species({   
            'id': "populus_tremuloides",
            'label' : 'Populus tremuloides',
            't0' : 10,
            'k' :  283.15,
            'r0' : 0.424,
            'e0' : 52261.3
        }),
        new Blackrock.Models.Species({   
            'id': "populus_grandidentata",
            'label' : 'Populus grandidentata',
            't0' : 10,
            'k' :  283.15,
            'r0' : 0.294,
            'e0' : 59425.5
        }),
        new Blackrock.Models.Species({   
            'id': "betula_lenta",
            'label' : 'Betula lenta',
            't0' : 10,
            'k' :  283.15,
            'r0' : 0.162,
            'e0' : 54267.7
        })
    ]);
    
    
    Blackrock.TestSpecies = new Blackrock.Models.Species({   
        'id': "unique_id",
        'label' : 'Quercus rubra',
        't0' : 10,
        'k' :  283.15,
        'r0' : 0.602,
        'e0' : 43140
    });

    Blackrock.TestSpeciesView = new Blackrock.Views.Species({ model: Blackrock.TestSpecies, el: jQuery('#left-pane')}).render();
    console.log(Blackrock.TestSpeciesView);
//  //App.TestScenarioView = new App.Views.Scenario();
//  
//  App.TestScenario = new App.Models.Scenario({});
//
//    App.TestScenarioView = new App.Views.Scenario({ model: App.TestScenario, el: jQuery('.scenario-view-test')}).render();
    
    
});



/* module wrapper pattern*/
(function() {

    //Currently Removes Duplicate Trees of Same Species - need to change that

    var global = this;
    var numSpecies = 1;
    var speciesList = [];
    var html = "";

    function initSpeciesCloner() {
        html = $('species1').innerHTML;
    }
    
    function initPredefinedSpecies() {        
        forEach(getElementsByTagAndClassName("input", "species-select-predefined"), function(elem) {
            disconnectAll(elem);
            connect(elem, "onclick", this, togglePredefinedSpeciesList);
        });
        
        forEach(getElementsByTagAndClassName("div", "species-predefined-choice"), function(elem) {
            disconnectAll(elem);
            connect(elem, "onclick", this, populateSpeciesChoice);
        });
    }
    
    function addSpecies(elem) {
      numSpecies++;
      var scenario;
      
      if(!elem) {
        scenario = document; //how does this associate the species with a scenario
        speciesList.push("species" + numSpecies);
      }
      else {
        // get scenario, if there is one
        scenario = getFirstParentByTagAndClassName(elem, "div", "scenario");
        if(! scenario) {
          scenario = document;
          speciesList.push("species" + numSpecies);
        }
        else if(scenario.id == "scenario1") {
          speciesList.push("species" + numSpecies);
        }
      }
      var parent = getFirstElementByTagAndClassName("div", "speciescontainer", scenario) ||
          getFirstElementByTagAndClassName("div", "leafspeciescontainer", scenario);
      var newDiv = DIV();
      addElementClass(newDiv, "species");
      appendChildNodes(parent, newDiv);
      newDiv.innerHTML = html.replace(/species1/g, "species" + numSpecies);
      newDiv.id = "species" + numSpecies;
      var namediv = getFirstElementByTagAndClassName("input", "species-name", newDiv);
      namediv.value = "Your Tree #" + numSpecies;
      global.EquationHighlighter.initSpecies(newDiv);
      updateColors();
      
      initPredefinedSpecies();
    }


    function initSpecies() {
      var leafSpecies = $("leaf-numspecies").value;
      speciesList = [];
      // change to see if jenkins will build
      for(var i=1; i<=leafSpecies; i++) {
        if(i > 1) {
          addSpecies();
        }
        else {
          speciesList.push("species"+i);
        }
        $('species'+i+'-name').value = $('leaf-species'+i+'-name').value;
        $('species'+i+'-base-temp').value = $('leaf-species'+i+'-base-temp').value;
        $('species'+i+'-R0').value = $('leaf-species'+i+'-R0').value;
        $('species'+i+'-E0').value = $('leaf-species'+i+'-E0').value;
      }
        if(leafSpecies == 0) {setDefaults(); }
    }

    function setDefaults() {
      $('species1-name').value = "Your Tree #1";
      $('species1-base-temp').value = 0;
      $('species1-R0').value = ""; /*0.84*/
      $('species1-E0').value = ""; /*27210*/

      speciesList = ["species1"];
    }
    

    function delSpecies(id) {
      removeElement(id);
      if(speciesList.indexOf(id) != -1) { 
        speciesList.splice(speciesList.indexOf(id), 1);
        leafGraph();
      }
    }

    function EquationHighlighter() {

    connect(window,'onload',this,'onLoad');
    this.vars = {
             "e-zero":[],
             "r-g":[],
             "t-zero":[],
             "t-a":[],
             "r-zero":[],
             "r-result":[]
            };
    this.current = [];
    }


    EquationHighlighter.prototype.onLoad = function() {

    var self = this;

    this.arrhenius_vars = getElementsByTagAndClassName(null,'arr-variable','equation');

    for (var a in self.vars) { //accessing the this.vars from function EquationHighlighter
        connect('arr-'+a,'onmouseenter',bind(self.hiliteFields,self,a));
        connect('arr-'+a,'onmouseleave',bind(self.unHiliteFields,self,a));
        forEach(getElementsByTagAndClassName(null,a),function(elt) {
        connect(elt,'onfocus',bind(self.hiliteVar,self,a,addElementClass));
        connect(elt,'onblur',bind(self.hiliteVar,self,a,removeElementClass));
        if($("plotGraph") !== null) {
          connect(elt,'onchange',self.needsUpdate);
        }
        });
    }
    };
    
    EquationHighlighter.prototype.needsUpdate = function() {
        // accessing outer TemperatureSliders
        if (leafGraph()) {
            global.TemperatureSliders.updateGraphDimensions();
        }
    };

    EquationHighlighter.prototype.initSpecies = function(elt) {
        var self = this;
        var e_zero = getFirstElementByTagAndClassName(null,"e-zero",elt);
        var r_zero = getFirstElementByTagAndClassName(null,"r-zero",elt);
        connect(e_zero,'onfocus',function(){self.hiliteVar("e-zero");});
        connect(r_zero,'onfocus',function(){self.hiliteVar("r-zero");});
        if($("plotGraph") !== null) {
          connect(e_zero,'onchange',self.needsUpdate);
          connect(r_zero,'onchange',self.needsUpdate);
        }
        
        var input_predefined = getFirstElementByTagAndClassName("input", "species-select-predefined", parent=elt);
        connect(input_predefined, "onclick", togglePredefinedSpeciesList);
        
        
        forEach(getElementsByTagAndClassName("div", "species-predefined-choice", parent=elt), function(elem) {
            disconnectAll(elem);
            connect(elem, "onclick", this, populateSpeciesChoice);
        });
    };
    
    EquationHighlighter.prototype.hiliteVar = function(arr_var,select_func) {
        var self = this;
        forEach(self.arrhenius_vars,function(elt) {
            removeElementClass(elt,'selected');
        });
        select_func = (select_func)?select_func:addElementClass;
        select_func('arr-'+arr_var,'selected');
    };
    
    EquationHighlighter.prototype.hiliteFields = function(arr_var) {
        var self = this;
        self.curr = getElementsByTagAndClassName(null,arr_var);
        forEach(self.curr,function(elt) {
            addElementClass(elt,'selected');
        });
        self.hiliteVar(arr_var);
    };
    
    EquationHighlighter.prototype.unHiliteFields = function(arr_var) {
        var self = this;
        forEach(self.curr,function(elt) {
            removeElementClass(elt,'selected');
        });
    };


    function TemperatureSliders() {
        connect(window,'onload',this,'onLoad');
        this.low=null;
        this.high=null;
        this.MAX_TEMP = 45;
        this.MIN_TEMP_WIDTH = 10;
        this.length=null;
        this.margin = 25;
        this.freeze = false;
    }


    TemperatureSliders.prototype.onLoad = function() {
        var self = this;
        if(!$('temp-slider')) {
            return; 
        }
        
        var sliders = null;
        try {
            sliders = getElementsByTagAndClassName(null,'slider','temp-slider');
        }
        catch(err) {
            return;  // no sliders; don't initialize this part
        }
        this.input_low = $('temp_low');
        this.input_high = $('temp_high');
        this.low = Number(this.input_low.value);
        this.high = Number(this.input_high.value);
    
        this.length = getElementDimensions(sliders[0].parentNode).w - this.margin;
        //length2temp:divide ; temp2length:multiply
        this.conv = this.length/this.MAX_TEMP;
        this.MIN_WIDTH = this.MIN_TEMP_WIDTH * this.conv;

        this.canvas = getElement('graph');
        this.graph_cursor = getElement('graph-cursor');
        
        /// Temperature Sliders
        connect(this.input_low,'onchange',function(){self.low = self.input_low.value;
                                 self.update('input_low');});
        connect(this.input_high,'onchange',function(){self.high = self.input_high.value;
                                  self.update('input_high');});
        this.drag_low = Draggable(sliders[0],{snap:bind(this.lowSnap,this),
                              onchange:bind(this.update,this,'drag_low'),
                              revert:global.EquationHighlighter.needsUpdate
                             });
        this.drag_high = Draggable(sliders[1],{snap:bind(this.highSnap,this),
                               onchange:bind(this.update,this,'drag_high'),
                               revert:global.EquationHighlighter.needsUpdate
                              });
    
        this.drag_range = Draggable(sliders[2],{snap:bind(this.rangeSnap,this),
                            onchange:bind(this.update,this,'drag_range'),
                            revert:global.EquationHighlighter.needsUpdate
                               });

        /// Graph Mouse Cursor
        connect(this.canvas,'onmousemove',this,'graphCursor');
        connect(this.canvas,'onclick',this,'setCursorFreeze');
        connect('unfreeze','onclick',this,'setCursorFreeze');
    
    
        this.update('do all of them');
        global.EquationHighlighter.needsUpdate();
    };

    TemperatureSliders.prototype.lowSnap = function(x,y) {
        x = Math.min(x,this.length-this.MIN_WIDTH);
        x = Math.max(x,0);
        this.low = x/this.conv;
        this.high = Math.max(this.high,(x+this.MIN_WIDTH)/this.conv);
        return [x,0];
    };
    
    TemperatureSliders.prototype.highSnap = function(x,y) {
        x = Math.min(x,this.length);
        x = Math.max(x,this.MIN_WIDTH);
        this.low = Math.min(this.low,(x-this.MIN_WIDTH)/this.conv);
        this.high = x/this.conv;
        return [x,0];
    };
    
    TemperatureSliders.prototype.rangeSnap = function(x,y) {
        var range = this.high - this.low;
        x = Math.min(x,this.length - range*this.conv);
        var low_coords = this.lowSnap(x,y);
        this.high = this.low + range;
        low_coords[1] = 8; //match #temp-slider .range in CSS
        return low_coords;
    };

    TemperatureSliders.prototype.update = function(not_me) {
        var self = this;
        var plans = {
            'input_low':function(){self.input_low.value = String(self.low).substr(0,4);},//2 decimals
            'input_high':function(){self.input_high.value = String(self.high).substr(0,4);},
            'drag_low':function(){
            self.drag_low.element.style.left = self.low*self.conv +'px'; //math
            },
            'drag_high':function(){
            self.drag_high.element.style.left = self.high*self.conv +'px'; //math
            },
            'drag_range':function(){
            self.drag_range.element.style.left = self.low*self.conv +'px'; //math
            self.drag_range.element.style.width = (self.high-self.low)*self.conv +'px'; //math
            }
        };
        delete plans[not_me];
        for (var a in plans) {
            plans[a]();
        }
    };

    TemperatureSliders.prototype.updateGraphDimensions = function() {
        this.graph_left_margin = this.calcGraphLeftMargin(); // variable based on the legend
        this.canvas_length = this.calcCanvasLength(); // depends on the graph_left_margin
        this.updateCursorVals();
    };
    
    TemperatureSliders.prototype.calcGraphLeftMargin = function() {
        var canvas_position = getElementPosition(this.canvas);
        
        // graph_left_margin is really the width of the y-axis legend.
        // left_margin can thus vary width depending on the value, 
        // throwing the whole graph off. Sadly, it's not easy to get this width
        // so, I'm trying a bit of a hack here.
        var margin = 0;
        var parent = getElement("rightfield");
        forEach(getElementsByTagAndClassName(null, "y-axis-label", parent),
                function(elem) {
                    var coords = getElementPosition(elem);
                    var dims = getElementDimensions(elem);
                       
                    // This constant represents the left & right draw margins in the canvas
                    // Yes, ugly, but no way else to figure out the exact positions of the y-axis labels
                    // 10.0999755859375;
                    var right = (coords.x - canvas_position.x) + dims.w + 10.0999755859375;
                    if (right > margin)
                        margin = right;
                });

        return margin;
    };
    
    TemperatureSliders.prototype.calcCanvasLength = function() {
        var graph_right_margin = 1.75;
        var canvas_length = getElementDimensions(this.canvas).w - this.graph_left_margin - graph_right_margin;
        return canvas_length;
    };

    TemperatureSliders.prototype.graphCursor = function(evt,do_anyway) {
        if (this.freeze && !do_anyway) return;
    
        var mouse = evt.mouse();
        var coords = getElementPosition(this.canvas);
        var pos_x = mouse.page.x - coords.x;
        this.temp = pos_x - this.graph_left_margin;
        if (this.temp >= this.canvas_length) { this.temp = this.canvas_length; }
        if (this.temp >= 0) {
            this.graph_cursor.style.left = (pos_x)+'px';
            var self = this;
            setTimeout(function(){self.updateCursorVals();},10);
            setTimeout(function(){showElement(self.graph_cursor);},10);
        }
    };
    
    TemperatureSliders.prototype.setCursorFreeze = function(evt) {
        var src = evt.src();
        if (src.id == 'unfreeze') {
            this.freeze = false;
            hideElement(src);
        }
        else {
            this.graphCursor(evt,true);
            this.freeze = true;
            showElement('unfreeze');
        }
    };

    TemperatureSliders.prototype.updateCursorVals = function(evt) {
        var lf = global.LeafData;
        var real_temp = lf.t_a_min + (lf.t_a_max-lf.t_a_min)*this.temp/this.canvas_length;

        if (!isNaN(real_temp)) {
            $('temp_mouse').value = Math.round(real_temp * 10) / 10;
            for (var a in lf.species) {
                $(a+'-R').value = lf.arrhenius(a,real_temp);
            }
        }
    };
    
    function getNumSpecies() {
      return numSpecies;
    }
    function incNumSpecies() {
      numSpecies++;
    }
    function getSpeciesList() {
      return speciesList;
    }
    function setSpeciesList(list) {
      speciesList = list;
    }


    function togglePredefinedSpeciesList(evt) {
        evt.stopPropagation();
        
        var elt = evt.src();
        var parent = getFirstParentByTagAndClassName(elt,
                tagName='div', className='species');     
        var list = getFirstElementByTagAndClassName(tagName="div",
                className="species-predefined-list", parent=parent);
        if (getStyle(list, 'display') == 'none') {
            // close other lists first
            closePredefinedSpecies();
            setStyle(list, {'display': 'block'});
        } else {
            setStyle(list, {'display': 'none'});
        }
    }

    var predefinedSpecies = {
        "quercus_rubra" : {
            'label' : 'Quercus rubra',
            't0' : 10,
            'k' :  283.15,
            'r0' : 0.602,
            'e0' : 43140
        },
        "quercus_prinus" : {
            'label' : 'Quercus prinus',
            't0' : 10,
            'k' :  283.15,
            'r0' : 0.670,
            'e0' : 37005
        },
        "acer_rubrum" : {
            'label' : 'Acer rubrum',
            't0' : 10,
            'k' :  283.15,
            'r0' : 0.680,
            'e0' : 27210
        },
        "vaccinium_corymbosum" : {
            'label' : 'Vaccinium corymbosum',
            't0' : 10,
            'k' :  283.15,
            'r0' : 0.091,
            'e0' : 62967
        },
        "berberis_thumbergii" : {
            'label' : 'Berberis thumbergii',
            't0' : 10,
            'k' :  283.15,
            'r0' : 0.203,
            'e0' : 81950
        },
        "kalmia_latifolia" : {
            'label' : 'Kalmia latifolia',
            't0' : 10,
            'k' :  283.15,
            'r0' : 0.308,
            'e0' : 54940
        },
        "carya_glabra": {
            'label' : 'Carya glabra',
            't0' : 10,
            'k' :  283.15,
            'r0' : 0.134,
            'e0' : 70547.5
        },
        "liriodendron_tulipifera": {
            'label' : 'Liriodendron tulipifera',
            't0' : 10,
            'k' :  283.15,
            'r0' : 0.187,
            'e0' : 60620.0
        },
        "platanus_occidentalis": {
            'label' : 'Platanus occidentalis',
            't0' : 10,
            'k' :  283.15,
            'r0' : 0.320,
            'e0' : 56336.7
        },
        "betula_papyrifera": {
            'label' : 'Betula papyrifera',
            't0' : 10,
            'k' :  283.15,
            'r0' : 0.357,
            'e0' : 45322.0
        },
        "populus_tremuloides": {
            'label' : 'Populus tremuloides',
            't0' : 10,
            'k' :  283.15,
            'r0' : 0.424,
            'e0' : 52261.3
        },
        "populus_grandidentata": {
            'label' : 'Populus grandidentata',
            't0' : 10,
            'k' :  283.15,
            'r0' : 0.294,
            'e0' : 59425.5
        },
        "betula_lenta": {
            'label' : 'Betula lenta',
            't0' : 10,
            'k' :  283.15,
            'r0' : 0.162,
            'e0' : 54267.7
        }
    };

    function populateSpeciesChoice(evt) {
        var elt = evt.src();
        if (elt.id in predefinedSpecies) {
            var parent = getFirstParentByTagAndClassName(elt, tagName='div', className='species');
            
            var eltLabel = getFirstElementByTagAndClassName('input', 'species-name', parent=parent);
            eltLabel.value = predefinedSpecies[elt.id].label;

            var eltTemp = getFirstElementByTagAndClassName('input', 't-zero', parent=parent);
            eltTemp.value = predefinedSpecies[elt.id].t0;//using t0 because it is the var in the json funct above

            var eltKelvin = getFirstElementByTagAndClassName('span', 'k-zero', parent=parent);
            eltKelvin.innerHTML = predefinedSpecies[elt.id].k;

            var eltRZero = getFirstElementByTagAndClassName('input', 'r-zero', parent=parent);
            eltRZero.value = predefinedSpecies[elt.id].r0;
            
            var eltEZero = getFirstElementByTagAndClassName('input', 'e-zero', parent=parent);
            eltEZero.value = predefinedSpecies[elt.id].e0;

            var lst = getFirstElementByTagAndClassName('div', 'species-predefined-list', parent=parent);
            setStyle(lst, {'display': 'none'});
            
            global.EquationHighlighter.needsUpdate();
        } else {
            alert('Cannot find that species. Please select another one.');
        }
    }
    
    function initSpeciesModule() {
        initSpeciesCloner();
        initSpecies();
        initPredefinedSpecies();
    }


    global.addSpecies = addSpecies;
    global.delSpecies = delSpecies;
    global.getNumSpecies = getNumSpecies;
    global.incNumSpecies = incNumSpecies;
    global.getSpeciesList = getSpeciesList;
    global.setSpeciesList = setSpeciesList;
    global.EquationHighlighter = new EquationHighlighter();
    global.TemperatureSliders = new TemperatureSliders();
    global.initSpeciesModule = initSpeciesModule;


})();