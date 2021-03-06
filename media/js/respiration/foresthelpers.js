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

function submitForm() {
    if (confirm('Navigating to the leaf level may cause you to lose scenario data. Do you want to continue?')) {
        $('scenario1-species').value = getSpeciesList().join();
        $('scenario1-form').submit();
        return true;
    }
    return false;
}

function initNav() {
  connect("tab-leaf", "onclick", submitForm);
  forEach(getElementsByTagAndClassName("div", "toggler"), function(elem) {
          connect(elem, "onclick", toggle);
  });
}


