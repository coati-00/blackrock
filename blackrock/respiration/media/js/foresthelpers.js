var blackrockRespiration.helperFunctions = function(){
    var stations = Array();
    var years = Array();

    addYears: function (stationName, yearlist) {
        stations.push(stationName);
        years.push(yearlist);
    },


    getStationIndex: function (stationName) {
        for(var idx = 0; idx < stations.length; idx++)
        if (stations[idx] == stationName)
            return idx;
        return -1;
    },

    updateYears: function (e) {
      var baseID = e.src().id.split('-')[0];
      var sel = $(baseID + "-year");
      var stationName = e.src().value;

      var selectedYear = sel.value;
      replaceChildNodes(sel, null);
      var yrs = years[getStationIndex(stationName)];
      for(var i=0; i<yrs.length; i++) {
            var year = yrs[i];
        var options = {'value':year};
        if(year == selectedYear) {
          options['selected'] = '';
       }
        appendChildNodes(sel, OPTION(options, year));
      }
    },

    initYearHelper: function () {
      forEach(getElementsByTagAndClassName("select", "fieldstation-select"), function(elem) {
        connect(elem, "onchange", updateYears);
        var scid = elem.id.split('-')[0];
        signal(elem, 'onchange', {'source':elem, 'type':'change'});
      });
    },

    toggle: function (e) {
      var elem = e.src();
      var parent = getFirstParentByTagAndClassName(elem, "div", "togglecontainer");
      var sibs = getElementsByTagAndClassName("*", "togglechild", parent);
      if(hasElementClass(elem, "toggle-open")) {
        removeElementClass(elem, "toggle-open");
        addElementClass(elem, "toggle-closed");
        forEach(sibs, function(sib) {
            hideElement(sib);
        });
      }
      else {
        removeElementClass(elem, "toggle-closed");
        addElementClass(elem, "toggle-open");
        forEach(sibs, function(sib) {
          showElement(sib);
        });
      }
    }

}


var stations = Array();
var years = Array();

function addYears(stationName, yearlist) {
  stations.push(stationName);
  years.push(yearlist);
}

function getStationIndex(stationName) {
    for(var idx = 0; idx < stations.length; idx++)
        if (stations[idx] == stationName)
            return idx;
    return -1;
}

function updateYears(e) {
  var baseID = e.src().id.split('-')[0];
  var sel = $(baseID + "-year");
  var stationName = e.src().value;

  var selectedYear = sel.value;
  replaceChildNodes(sel, null);
  var yrs = years[getStationIndex(stationName)];
  for(var i=0; i<yrs.length; i++) {
    var year = yrs[i];
    var options = {'value':year};
    if(year == selectedYear) {
      options['selected'] = '';
   }
    appendChildNodes(sel, OPTION(options, year));
  }
}

function initYearHelper() {
  forEach(getElementsByTagAndClassName("select", "fieldstation-select"), function(elem) {
    connect(elem, "onchange", updateYears);
    var scid = elem.id.split('-')[0];
    signal(elem, 'onchange', {'source':elem, 'type':'change'});
  });
}

function toggle(e) {
  var elem = e.src();
  var parent = getFirstParentByTagAndClassName(elem, "div", "togglecontainer");
  var sibs = getElementsByTagAndClassName("*", "togglechild", parent);
  if(hasElementClass(elem, "toggle-open")) {
    removeElementClass(elem, "toggle-open");
    addElementClass(elem, "toggle-closed");
    forEach(sibs, function(sib) {
            hideElement(sib);
    });
  }
  else {
    removeElementClass(elem, "toggle-closed");
    addElementClass(elem, "toggle-open");
    forEach(sibs, function(sib) {
      showElement(sib);
    });
  }
}
