if (typeof Portal == 'undefined') {
    Portal = {};
}

if (!Portal.Layer) {
    Portal.Layer = function(identifier, fileName, clickable) {
        var self = this;
    
        self.identifier = identifier;
        
        var myOptions = { preserveViewport: "true", suppressInfoWindows: false, clickable: clickable };
        self.instance = new google.maps.KmlLayer(fileName, myOptions);
        
        google.maps.event.addListener(self.instance, 'click', function (kmlEvent) {
           // @todo - custom info window... 
        });
        
        this.isVisible = function() {
            return self.instance.map != null;
        }
    }
}

/**
if (!Portal.MapMarker) {    
    Portal.MapMarker = function() {
        var self = this;
        
        Portal.Base.Observer.apply(this,arguments); //inherit events
        self.assetIdentifier = null;
        self.description = null; 
        self.featured = [];
        self.infrastructure = [];
        self.marker = null;
        self.latlng = null;
        
        this.create = function(mapInstance, assetIdentifier, name, description, lat, lng, featured, infrastructure, iconName, zIndex) {
            self.assetIdentifier = assetIdentifier;;
            self.description = description; 
            self.featured = featured;
            self.infrastructure = infrastructure;
            
            if (!lat || !lng)
                return null;
            
            var iconUrl = '';
            if (infrastructure && infrastructure.length) {
                var iconName = infrastructure[0];
                iconName = iconName.replace(/ /g, "");
                iconName = iconName.replace("-", "");
                iconUrl = 'http://' + location.hostname + ':' + location.port + "/portal/media/images/mapicon_" + iconName.toLowerCase() + '.png';
            } else if (featured && featured.length) {
                var iconName = featured[0];
                iconName = iconName.replace("Featured ", "");
                iconUrl = 'http://' + location.hostname + ':' + location.port + "/portal/media/images/mapicon_" + iconName.toLowerCase() + '.png';
            } else if (iconName) {
                if (iconName.indexOf("http:") === 0)
                    iconUrl = iconName;
                else
                    iconUrl = 'http://' + location.hostname + ':' + location.port + "/portal/media/images/" + iconName;
            } else {
                iconUrl = 'http://' + location.hostname + ':' + location.port + "/portal/media/images/mapicon_main.png";
            }

            self.latlng = new google.maps.LatLng(lat, lng);
            var shouldBeVisible = self.shouldBeVisible();
            self.marker = new google.maps.Marker({
                position: self.latlng, 
                title: name,
                icon: iconUrl,
                map: shouldBeVisible ? mapInstance : null,
                zIndex: zIndex
             });
            
            google.maps.event.addListener(self.marker, 'click', function() {
               self.events.signal(Portal, 'markerClicked', self.assetIdentifier);
            });
            
            return self.latlng;
        }
        
        this.isVisible = function() {
            return self.marker.map != null;
        }
        
        this.shouldBeVisible = function() {
            var visible = false;
            var options = null;
            var values = null;
            
            if (self.infrastructure && self.infrastructure.length ) {
                options = getElementsByTagAndClassName("input", "infrastructure_option");
                values = self.infrastructure;
            } else if (self.featured && self.featured.length) {
                options = getElementsByTagAndClassName("input", "featured_option");
                values = self.featured;
            } else {
                visible = true;
            }

            if (options) {
                forEach(options,
                        function(option) {
                            if (option.checked) {
                                for (var i=0; i < values.length; i++) {
                                    if (option.value == values[i]) {
                                        visible = true;
                                    }
                                }
                            }
                        });
            }
                
            return visible;
        }
    }
}
**/
if (!Portal.Map) {
    Portal.Map = function() {
        var self = this;
        
        self.mapInstance = null;
        self.locations = {};
        self.search_results = {};
        self.infoWindow = null;
        self.layers = {}
        self.forestCenter = null;
        self.currentPosition = null;
        
        this.hideInfoWindow = function() {
            if (self.infowindow)
                self.infowindow.close()
        }

        this.showLayerInfoWindow = function(kmlEvent) {
            if (self.infowindow)
                self.infowindow.close()
            
            var description;

            // @todo -- client-side templates?
            if (kmlEvent.featureData.name) {
                description =  '<div class="callout"><span class="callout-display-name">' + kmlEvent.featureData.name + '</span>';
                if (kmlEvent.featureData.description)
                    description += '<div class="callout-asset-types">' + kmlEvent.featureData.description + '</div>';
                description += '<a class="callout-summary-link" onclick="portalMapInstance.search(' + 
                               kmlEvent.latLng.lat() + ', ' + kmlEvent.latLng.lng() + ', \'' + escape(kmlEvent.featureData.name) + '\')">Search nearby</a></div>';
            } else if (kmlEvent.featureData.description) {
                var title = kmlEvent.featureData.description.replace("_blank", "_self");
                description =  '<div class="callout"><div>' + title + '</div><br />';
                title = title.replace(/(<([^>]+)>)/ig,"");
                description += '<a class="callout-summary-link" onclick="portalMapInstance.search(' + 
                               kmlEvent.latLng.lat() + ', ' + kmlEvent.latLng.lng() + ', \'' + escape(title) + '\')">Search nearby</a></div>';                
            } else {
                description = kmlEvent.latLng.lat() + ', ' + kmlEvent.latLng.lng();
            }
            
            var params = {content: description, position: kmlEvent.latLng, maxWidth: 400 }
            if (kmlEvent.pixelOffset.height < 0)
                params['pixelOffset'] = new google.maps.Size(-5, -20);
            self.infowindow = new google.maps.InfoWindow(params);
            self.infowindow.open(self.mapInstance);
        }
        
        this.showMarkerInfoWindow = function(asset_identifier) {
            var location = self.locations[asset_identifier];
            if (!location)
                location = self.search_results[asset_identifier]
            if (!location)
                location = self.selected[asset_identifier];
            
            if (location) {

                if (self.infowindow)
                    self.infowindow.close()
                
                var offset = new google.maps.Size(-5, 15);
    
                self.infowindow = new google.maps.InfoWindow({content: location.description, maxWidth: 400, pixelOffset: offset });
                self.infowindow.open(self.mapInstance, location.marker);
            }
        }
        
        this.toggleFacet = function() {
            for (var assetIdentifier in self.locations) {
                var location = self.locations[assetIdentifier];
                var visible = location.isVisible();
                var shouldBeVisible = location.shouldBeVisible();
                
                if (shouldBeVisible && !visible) {
                    location.marker.setMap(self.mapInstance);
                } else if (!shouldBeVisible && visible) {
                    location.marker.setMap(null);
                }
            }
        }
        
        this.toggleLayer = function() {
            for (var identifier in self.layers) {
                var layer = self.layers[identifier];
                var visible = layer.isVisible();
                var shouldBeVisible = layer.shouldBeVisible();
                
                if (shouldBeVisible && !visible) {
                    layer.instance.setMap(self.mapInstance);
                } else if (!shouldBeVisible && visible) {
                    layer.instance.setMap(null);
                }
            }
        }
        
        this.initMarkers = function(className, zIndexBoost, fitBounds) {
            // iterate over locations within the page, and add the requested markers
            var bounds = new google.maps.LatLngBounds();
            var a = {};
            var elements = getElementsByTagAndClassName("div", className);
            var zIndex = 100 + zIndexBoost;
            forEach(elements,
                    function(elem) {
                        var assetIdentifier = getFirstElementByTagAndClassName(null, "asset_identifier", elem).value;
                        var name = document.getElementById(assetIdentifier + "-name").value;
                        var description = document.getElementById(assetIdentifier + "-description").innerHTML;
                        var latitude = document.getElementById(assetIdentifier + "-latitude").value;
                        var longitude = document.getElementById(assetIdentifier + "-longitude").value;
                        
                        var iconname = null;
                        var property = document.getElementById(assetIdentifier + "-iconname");
                        if (property && property.value.length > 0)
                            iconname = property.value;
                        
                        var featured = null;
                        var infrastructure = null;
                        
                        property = document.getElementById(assetIdentifier + "-infrastructure");
                        if (property && property.value.length > 0)
                            infrastructure = property.value.split(",")
                            
                        property = document.getElementById(assetIdentifier + "-featured");
                        if (property && property.value.length > 0)
                            featured = property.value.split(",")
                        
                        var marker = new Portal.MapMarker();
                        var latlng = marker.create(self.mapInstance, assetIdentifier, name, description, latitude, longitude, featured, infrastructure, iconname, zIndex);
                        
                        a[assetIdentifier] = marker;
                        bounds.extend(latlng);
                        zIndex--;
                    });      
            
            if (!bounds.isEmpty() && fitBounds)
                self.mapInstance.fitBounds(bounds);
            
            return a;
        }
        
        this.search = function(lat, long, title) {
            for (var result in self.search_results) {
                var location = self.search_results[result];
                location.marker.setMap(null);
            }
            self.search_results = {};
            
            document.getElementById("map_filters").style.display = "none";
            
            var nearby_results = document.getElementById("nearby_results");
            
            jQuery(nearby_results).show('fast', function() {
                var url = '/portal/nearby/' + lat + '/' + long + '/';
                var request = doXHR(url);
                request.addCallback(function(response) {
                    nearby_results.innerHTML = response.responseText;
                    document.getElementById("nearby_asset").innerHTML = unescape(title);
                    self.search_results = self.initMarkers("nearby", 0, true);
                    
                    var listener = google.maps.event.addListenerOnce(self.mapInstance, "idle", function() { 
                        var center = new google.maps.LatLng(lat, long);
                        self.mapInstance.setCenter(center);
                    });
                    
                });
            });
        }
        
        this.closeSearch = function() {
            document.getElementById("map_filters").style.display = "block";
            var nearby_results = document.getElementById("nearby_results");
            nearby_results.innerHTML = "";
            nearby_results.style.display = "none";
            
            for (var result in self.search_results) {
                var location = self.search_results[result];
                location.marker.setMap(null);
            }
            self.search_results = {};
            self.center();
        }
        
        this.center = function() {
            self.mapInstance.setCenter(self.forestCenter);
            self.mapInstance.setZoom(13);
        }
        
        this.markerCount = function(myobj) {
            var count = 0;
            for (k in myobj) if (myobj.hasOwnProperty(k)) count++;
            return count;
        }
        
        this.geolocate = function() {
            var browserSupportFlag = false;
            if (navigator.geolocation) {
                // Try W3C Geolocation (Preferred)
                browserSupportFlag = true;
                navigator.geolocation.getCurrentPosition(function(position) {
                    var currentLocation = new google.maps.LatLng(position.coords.latitude,position.coords.longitude);
                    self.mapInstance.setCenter(currentLocation);
                    
                    self.currentPosition = new google.maps.Marker({
                        map: self.mapInstance,
                        draggable:true,
                        animation: google.maps.Animation.DROP,
                        position: currentLocation,
                        icon: "http://chart.googleapis.com/chart?chst=d_map_pin_letter_withshadow&chld=|FF0000|000000"
                    });
                    
                }, function() {
                    handleNoGeolocation(browserSupportFlag);
                });
            } else {
                // Browser doesn't support Geolocation
                browserSupportFlag = false;
                handleNoGeolocation(browserSupportFlag);
            }
            
            function handleNoGeolocation(errorFlag) {
                if (browserSupportFlag) {
                    alert("Geolocation service failed. Map recentering on Black Rock Forest");
                } else {
                    alert("Your browser doesn't support geolocation. Map recentering on Black Rock Forest");
                }
                self.mapInstance.setCenter(self.forestCenter);
            }
        }
        
        this.initialize = function() {
            // Center on center of Black Rock Forest
            self.forestCenter = new google.maps.LatLng(41.397459,-74.021848);
            var myOptions = {
                zoom: 13,
                center: self.forestCenter,
                mapTypeId: google.maps.MapTypeId.TERRAIN,
                disableDefaultUI: true,
            };
            
            self.mapInstance = new google.maps.Map(document.getElementById("map_canvas"), myOptions);

            var boundary = new Portal.Layer("brfboundary", "http://blackrock.ccnmtl.columbia.edu/portal/media/kml/brfboundary.kml", false);
            boundary.instance.setMap(self.mapInstance);
            
            var kmllayer = new Portal.Layer("trails", "http://blackrock.ccnmtl.columbia.edu/portal/media/kml/trails.kml", true);
            self.layers["trails"] = kmllayer;
            kmllayer.instance.setMap(self.mapInstance);
            
            /**
            var options = getElementsByTagAndClassName("input", "layer");
            forEach(options,
                    function(option) {
                        var kmllayer = new Portal.Layer(option.id, "http://blackrock.ccnmtl.columbia.edu/portal/media/kml/" + option.id + ".kml?yyyy=" + randomnumber, true);
                        self.layers[option.id] = kmllayer;
                        
                        connect(option, 'onclick', function(evt) {
                            self.events.signal(Portal, 'toggleLayer');
                         });
                    });
            
            options = getElementsByTagAndClassName("input", "facet");
            forEach(options,
                    function(option) {
                        connect(option, 'onclick', function(evt) {
                            self.events.signal(Portal, 'toggleFacet');
                         });
                    });
                
            self.locations = self.initMarkers("geocode", 0, false);
            self.locations = self.initMarkers("geocode_detail", 0, true);
            
            self.selected = self.initMarkers("geoselected", 0, true);
            if (self.markerCount(self.selected)) {
                var listener = google.maps.event.addListenerOnce(self.mapInstance, "idle", function() { 
                    self.mapInstance.setZoom(14);
                    
                    for (var s in self.selected) {
                        self.showMarkerInfoWindow(s);
                    }
                });
            }
            
            var boundary = new Portal.Layer("brfboundary", "http://blackrock.ccnmtl.columbia.edu/portal/media/kml/brfboundary.kml", false);
            boundary.instance.setMap(self.mapInstance);
            
            self.toggleLayer();
**/            
        }
    }
}

var portalMapInstance = new Portal.Map();