    function showResources() {
  	  /* this is ugly but want to get everything
  	  on one page before doing complete cleanup
  	  and adding things like bootstrap */
  	  console.log("showresources");
  	  //get whatever tab is currently active, remove active class, make resource tab active
  	  //start by removing classes from other elements and removing html from other tabs
  	  jQuery('#tab-leaf').removeClass('active');
  	  jQuery('#tab-canopy').removeClass('active');
  	  jQuery('#tab-leaf').removeClass('tab-selected');
  	  jQuery('#tab-canopy').removeClass('tab-selected');
  	  jQuery('#resource-area').show();
  	  jQuery('#instructions').css("display","none");
  	  jQuery('#container').css("display","none");
  	  jQuery('#equation').css("display","none");
  	  jQuery('#tab-resources').addClass('active');
  	  jQuery('#tab-resources').addClass('tab-selected');
  	  //show the resources content
  	  jQuery('#resource-area').html(jQuery('#resources-template').html());   	  
  	  
    }
    
    function showLeaf() {
    	  /* this is ugly but want to get everything
    	  on one page before doing complete cleanup and adding things like bootstrap */
    	  console.log("showLeaf");
    	  //get whatever tab is currently active, remove active class, make resource tab active
    	  jQuery('#tab-resources').removeClass('active');
    	  jQuery('#tab-canopy').removeClass('active');
    	  jQuery('#tab-resources').removeClass('tab-selected');
    	  jQuery('#tab-canopy').removeClass('tab-selected');    	  
    	  
    	  jQuery('#tab-leaf').addClass('active');
    	  jQuery('#tab-leaf').addClass('tab-selected');

    	  //populate the module header
    	  jQuery('#instructions').show();
    	  jQuery('#container').show();
    	  jQuery('#equation').show();
    	  jQuery('#resource-area').hide();
    	  jQuery('#instructions').html(jQuery("#leaf-instructions-template").html());
    	  
    	  //replace the current content with the leaf content
    	  jQuery('#left-legend').html(jQuery('#leaf-left-legend-template').html());
    	  jQuery('#left-pane').html(jQuery('#leaf-left-pane-template').html());
    	  jQuery('#right-legend').html(jQuery('#leaf-right-legend-template').html());
    	  jQuery('#right-pane').html(jQuery('#leaf-right-pane-template').html());
      }
        
    function showCanopy() {
  	  /* this is ugly but want to get everything
  	  on one page before doing complete cleanup and 
  	  adding things like bootstrap */
  	  console.log("showCanopy");
  	  //get whatever tab is currently active, remove active class, make canopy tab active
  	  jQuery('#tab-resources').removeClass('active');
  	  jQuery('#tab-leaf').removeClass('active');
  	  jQuery('#tab-resources').removeClass('tab-selected');
  	  jQuery('#tab-leaf').removeClass('tab-selected');
  	  
  	  jQuery('#tab-canopy').addClass('active');
  	  jQuery('#tab-canopy').addClass('tab-selected');

  	  //make areas associated with leaf and canopy visible
  	  jQuery('#instructions').show();
  	  jQuery('#container').show();
  	  jQuery('#equation').show();
  	  jQuery('#resource-area').hide();
  	  
  	  
  	  jQuery('#instructions').html(jQuery("#canopy-instructions-template").html());
  	  
  	  //replace the current content with the leaf content
  	  jQuery('#left-legend').html(jQuery('#canopy-left-legend-template').html());
  	  jQuery('#left-pane').html(jQuery('#canopy-left-pane-template').html());
  	  jQuery('#right-legend').html(jQuery('#canopy-right-legend-template').html());
  	  jQuery('#right-pane').html(jQuery('#canopy-right-pane-template').html());
    }
    
    function initNav() {
      	  showLeaf(); //start out with leaf tab being active
      	  jQuery('#tab-resources').on('click', function() { showResources();})
      	  jQuery('#tab-leaf').on('click', function() { showLeaf();})
      	  jQuery('#tab-canopy').on('click', function() { showCanopy();})
     }