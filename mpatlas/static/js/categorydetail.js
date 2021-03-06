    define([
      // These are path aliases configured in the requireJS bootstrap
      'jquery',
      'backbone',
      'cartodb',
      '/static/js/TileLayer.Bing',
      '/static/js/leaflet.label'
    ],
    function ($, Backbone) {  
        var _CategoryDetail = Backbone.View.extend({
            proxy: '',
            domain: window.location.origin + '/',
            //proxy: '/terraweave/features.ashx?url=', // handle cross-domain if necessary. used for testing
            //domain: 'https://mpatlas.org/',
            
            initialize: function(map) {
                var that = this;
                if ($.type(map) === 'object') {
                    this.mapelem = (map.length) ? map[0] : map;
                } else {
                    this.mapelem = $('#' + map)[0]; // Assume it's an element id string
                }
                this.member_data_url = 'features/';
                this.defaultzoom = 3;
                
                this.makeMap();
                window['leafmap'] = this.map;

                this.loadFeatures();
                
                // this.loadFeature();
                // this.zoomToFeature();
            },

            // create Leaflet map
            makeMap: function() {

                this.layers = [];
                this.bgLayers = {};
                this.overlayLayers = {};
                var subdomains = '12345678'; // tile1.mpatlas.org, tile2...

                // ESRI World Oceans Base Layer
                var lyr = new L.TileLayer(
                    'https://services.arcgisonline.com/ArcGIS/rest/services/Ocean/World_Ocean_Base/MapServer/tile/{z}/{y}/{x}.png',
                    {id: 10, maxZoom: 10, opacity: 0.4, attribution: 'Basemap &copy; ESRI'}
                );
                this.bgLayers['World Oceans'] = lyr;
                this.layers.push(lyr);

                // ESRI World Oceans Reference
                var lyr = new L.TileLayer(
                    'https://services.arcgisonline.com/ArcGIS/rest/services/Ocean/World_Ocean_Reference/MapServer/tile/{z}/{y}/{x}.png',
                    {id: 10, maxZoom: 10, opacity: 1, attribution: ''}
                );
                this.bgLayers['World Ocean Annotation'] = lyr;
                this.layers.push(lyr);
        
                // Bing background layer for testing
                lyr = new L.TileLayer.Bing(
                    'AnrVx0YzYa6emmkAQPBI9Ka1uY1ZFKPDC7fGYntZX2PJkJFTNgmEKfUTFC_3EI_e',
                    {type: 'Road', id: 2, maxZoom: 18, opacity: 1}
                );
                this.bgLayers['Bing Maps'] = lyr;
                //this.layers.push(lyr);
                
                // EEZs / Nations       
                lyr = new L.TileLayer(
                    'https://tile{s}.mpatlas.org/tilecache/eezs/{z}/{x}/{y}.png',
                    {id: 3, maxZoom: 10, opacity: 0.2, tms: true, subdomains: subdomains, color: '#01DF74'}
                );
                this.overlayLayers['Exclusive Economic Zones'] = lyr;
                //this.layers.push(lyr);
                
                // Marine Eco-Regions
                lyr = new L.TileLayer(
                    'https://tile{s}.mpatlas.org/tilecache/meow/{z}/{x}/{y}.png',
                    {id: 4, maxZoom: 10, opacity: 0.4, tms: true, subdomains: subdomains, color: '#CC00CC'}
                );
                this.overlayLayers['Marine Eco-Regions'] = lyr;
                
                // FAO Fishing Zones
                lyr = new L.TileLayer(
                    'https://tile{s}.mpatlas.org/tilecache/fao/{z}/{x}/{y}.png',
                    {id: 5, maxZoom: 10, opacity: 0.4, tms: true, subdomains: subdomains, color: '#FFFF00'}
                );
                this.overlayLayers['FAO Fishery Mgmt Regions'] = lyr;
                
                // Designated Marine Protected Areas
                lyr = new L.TileLayer(
                    'https://tile{s}.mpatlas.org/tilecache/mpas/{z}/{x}/{y}.png',
                    {id: 1, maxZoom: 10, opacity: 0.3, tms: false, subdomains: subdomains, color: '#0000AA'}
                );
                this.overlayLayers['Designated Marine Protected Areas'] = lyr;
                this.layers.push(lyr);
                this.mpalayer = lyr;
                
                // Candidate Marine Protected Areas
                lyr = new L.TileLayer(
                    'https://tile{s}.mpatlas.org/tilecache/candidates/{z}/{x}/{y}.png',
                    {id: 2, maxZoom: 10, opacity: 0.3, tms: false, subdomains: subdomains, color: '#FF8000'}
                );
                this.overlayLayers['Candidate Marine Protected Areas'] = lyr;
                //this.layers.push(lyr);
                
                this.map = new L.Map(this.mapelem, {
                    center: new L.LatLng(0, 0),
                    zoom: this.defaultzoom,
                    layers: this.layers,
                    worldCopyJump: true,
                    minZoom: 0,
                    maxZoom: 18,
                    attributionControl:false,
                    touchZoom: true // needed for Android tablets
                });
                
                var map = this.map; // use this var for closures inside event handlers

                // override the position of layer control           
                L.Control.Layers.prototype.getPosition = function () {
                    return 'bottomleft';
                };
                
                this.layersControl = new L.Control.Layers(
                    this.bgLayers,
                    this.overlayLayers,
                    {
                        collapsed: !L.Browser.touch
                    }
                );
                this.map.addControl(this.layersControl);
                
                this.map.on('viewreset', function (e) {
                    try {
                        //mpatlas.saveMapLocation();
                    } catch (ex) {}
                });

                this.map.on('moveend', function (e) {
                    try {
                        //mpatlas.saveMapLocation();
                    } catch (ex) {}
                });

                this.map.on('layeradd', function (e) {
                    try {
                        //mpatlas.layerAdded(e);
                    } catch (ex) {}
                });

                this.map.on('layerremove', function (e) {
                    try {
                        //mpatlas.layerRemoved(e);
                    } catch (ex) {}
                });

                // In case you need multiple markers on each of the "wrapped" worlds when zoomed out, or when
                // working near the dateline, need to make multiple markers with the 'true' 3rd parameter.
                // Also need to translate polylines, polygons, and GeoJSON layers
                //var markerLocation = new L.LatLng(51.5, -0.09),
                //    markerLocation2 = new L.LatLng(markerLocation.lat, markerLocation.lng + 360, true),
                //    markerLocation3 = new L.LatLng(markerLocation.lat, markerLocation.lng - 360, true),
            },
            
            /*
            resizeViewport: function() {
                return false;
                //$('#body_full').height($(window).height() - $('#header_full').height() - $('#footer_full').height());
                //this.map.invalidateSize();
            },
            */

            zoomToFeature: function() {
                that = this;
                if (this.is_point) {
                    var point = new L.LatLng(this.point[1], this.point[0])
                    this.map.setView(point, 6);
                } else {
                    var sw = new L.LatLng(this.bbox[0][1], this.bbox[0][0], true);
                    var ne = new L.LatLng(this.bbox[1][1], this.bbox[1][0]);
                    var bounds = new L.LatLngBounds(sw, ne);
                    var startzoom = this.map.getZoom();
                    this.map.fitBounds(bounds);
                    var zoomtimer;
                    (function forceZoom() {
                        if (startzoom == that.map.getZoom()) {
                            zoomtimer = setTimeout(function() {
                                forceZoom();
                            }, 100);
                        } else {
                            clearTimeout(zoomtimer);
                            if (that.is_point) {
                                that.map.setZoom(that.defaultzoom);
                            } else {
                                that.map.zoomOut();
                            }
                        }
                    })();
                }
            },
            
            loadFeatures: function() {
                that = this;
                var geojsonMarkerOptions = {
                    radius: 5,
                    fillColor: "#66ff78",
                    color: "#000",
                    weight: 1,
                    opacity: 1,
                    fillOpacity: 0.8
                };
                var polystyle = {
                    weight: 1,
                    // color: '#d0508c',
                    color: '#de744a',
                    opacity: 0.9,
                    // fillColor: '#d0508c',
                    fillColor: '#de744a',
                    fillOpacity: 0.7
                };
                var outlinestyle = {
                    weight: 8,
                    // color: '#d0508c',
                    color: '#de744a',
                    opacity: 0.2,
                    // fillColor: '#d0508c',
                    fillColor: '#de744a',
                    fillOpacity: 0
                };
                var highlightoutlinestyle = {
                    weight: 8,
                    // color: '#d0508c',
                    color: '#d0508c',
                    opacity: 0.2,
                    // fillColor: '#d0508c',
                    fillColor: '#de744a',
                    fillOpacity: 0
                };
                var highlightstyle = {
                    weight: 1,
                    // color: '#ffc4f9',
                    color: '#d0508c',
                    opacity: 0.9,
                    fillColor: '#d0508c',
                    fillOpacity: 0.7
                };
                var memberList = document.getElementById('member-list');
                var geojson;
                function wrapCoords(coords, west, east) {
                    var a = !isNaN(parseFloat(west)) && isFinite(west) ? west : -180;
                    var b = !isNaN(parseFloat(east)) && isFinite(east) ? east : a + 360;
                    var lng = (coords[0]) % (b - a) + (coords[0] < 0 ? (b - a) : 0); // shift to value between 0 and (b-a) (typically 0-360)
                    lng = lng + (Math.floor((a - lng)/(b-a)) + 1)*(b-a); // translate to value between a and b
                    return new L.LatLng(coords[1], lng);
                }
                function shiftLatLngs(latlngs, shift) {
                    var _latlngs = [];
                    for (var i=0; i < latlngs.length; i++) {
                        _latlngs[i] = new L.LatLng(latlngs[i].lat, latlngs[i].lng + shift);
                    }
                    return _latlngs;
                }
                function shiftFeature(feature, shift) {
                    var emptyObject = {};
                    var shifted = $.extend(true,emptyObject,feature);

                };
                // wrapCoords(coords, -360, 0);
                function highlightLayer(layer) {
                    layer.feature.properties.original.setStyle(highlightoutlinestyle);
                    layer.setStyle(highlightstyle);
                    layer.bringToFront();
                }
                function resetLayer(layer) {
                    layer.feature.properties.original.setStyle(outlinestyle);
                    geojson.resetStyle(layer);
                }
                geojson = new L.GeoJSON(null, {
                    onEachFeature: function(feature, layer) {
                        var duplicatefeature = function(feature) {
                            if (!feature.properties.duplicated) {
                                var copiedObject = {};
                                var feature2 = $.extend(true,copiedObject,feature);
                                feature2.properties.duplicated = true;
                                feature2.properties.original = layer;
                                feature2.properties.id = '9999' + feature2.properties.id
                                setTimeout(function() {
                                    geojson.addData(feature2);
                                }, 0);
                            }
                        };
                        if (feature.properties) {
                            layer.bindLabel(feature.properties.name);
                            layer.bindPopup('<h5><a href="' + feature.properties.url + '">' + feature.properties.name + '</a></h5>' + 
                                '<a href="' + feature.properties.url + '">view full description</a>' + 
                                '<p>' + feature.properties.summary + '</p>', {
                                maxHeight: '120'
                            });
                            if (!feature.properties.duplicated) {
                                var item = memberList.appendChild(document.createElement('li'));
                                item.innerHTML = '<a href="#" onclick="return false;">' + feature.properties.name + '</a>';
                                $(item).on('mouseover', function() {
                                    var _layer = (layer.feature.properties.duplicate) ? layer.feature.properties.duplicate : layer;
                                    highlightLayer(_layer);
                                });
                                $(item).on('mouseout', function() {
                                    var _layer = (layer.feature.properties.duplicate) ? layer.feature.properties.duplicate : layer;
                                    resetLayer(_layer);
                                });
                                $(item).on('click', function() {
                                    that.map.setView(layer.getBounds().getCenter(), that.defaultzoom+2);
                                    layer.openPopup();
                                });
                            }
                        }
                        
                        layer.setStyle(outlinestyle);
                        if (feature.properties.duplicated == true) {
                            var original = feature.properties.original;
                            original.feature.properties.duplicate = layer;
                            layer.setStyle(polystyle);
                        }
                        layer.on({
                            mouseover: function(e) {
                                var layer = (e.target.feature.properties.duplicate) ? e.target.feature.properties.duplicate : e.target;
                                highlightLayer(layer);
                            },
                            mouseout: function(e) {
                                var layer = (e.target.feature.properties.duplicate) ? e.target.feature.properties.duplicate : e.target;
                                resetLayer(layer);
                            }
                        });

                        duplicatefeature(feature);
                    },
                    pointToLayer: function (feature, latlng) {
                        var m1 = L.circleMarker(latlng, geojsonMarkerOptions);
                        var m2 = L.circleMarker(L.latLng(latlng.lat, latlng.lng - 360, true), geojsonMarkerOptions);
                        var m3 = L.circleMarker(L.latLng(latlng.lat, latlng.lng + 360, true), geojsonMarkerOptions);
                        return L.featureGroup([m1, m2, m3])
                    },
                    style: polystyle
                }).addTo(that.map);
                $.ajax({
                    url: that.member_data_url,
                    success: function(data) {
                        geojson.addData(data);
                    },
                    error: function(request, type, ex) {
                        console.log(request, type, ex);
                    }
                });
            },

            loadFeature: function() {
                that = this;
                $.ajax({
                    url: this.feature_url,
                    success: function(data) {
                        var geojson = new L.GeoJSON(data);
                        geojson.setStyle({
                            weight: 3,
                            color: '#d0508c',
                            opacity: 0.8,
                            fillColor: '#d0508c',
                            fillOpacity: 0.2
                        });
                        if (that.highlightlayer) {
                            that.map.removeLayer(that.highlightlayer);
                        }
                        delete that.highlightlayer;
                        geojson.on('click', function(mapevent) {
                            that.map.fireEvent('click', mapevent); // pass click from layer to map
                        });
                        that.map.addLayer(geojson);
                        that.highlightlayer = geojson;
                        if (!that.bbox[0][0]) {
                            that.map.fitBounds(that.highlightlayer.getBounds());
                        }
                    }
                });
            },

            getPixelRadius: function(pxradius) {
                // Convert pixel radius to map units (web mercator = meters) then to km.
                // pxradius can be a floating point value
                var bounds = this.map.getBounds(),
                    crs = this.map.options.crs; // undocumented access to map projection functions
                var resolution = (crs.project(bounds.getNorthEast()).y - crs.project(bounds.getSouthWest()).y) / this.map.getSize().y;
                return (resolution * pxradius) / 1000;
            }
        });

        return {
            CategoryDetail: _CategoryDetail
        };
        // What we return here will be used by other modules
    }
);
