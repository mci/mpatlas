define([
  // These are path aliases configured in the requireJS bootstrap
  'jquery',
  'backbone',
  'cartodb',
  '/static/js/TileLayer.Bing'
  // 'leaflet.vectorgrid'
  //'persist',
  //'MPAList'
],
function ($, Backbone) {  
    var SiteDetail = Backbone.View.extend({
		proxy: '',
		domain: window.location.origin + '/',
		//proxy: '/terraweave/features.ashx?url=', // handle cross-domain if necessary. used for testing
		//domain: 'https://mpatlas.org/',
        
        initialize: function(map, siteid, feature_url, is_point, point, bbox) {
            var that = this;
            if ($.type(map) === 'object') {
                this.mapelem = (map.length) ? map[0] : map;
            } else {
                this.mapelem = $('#' + map)[0]; // Assume it's an element id string
            }
            this.siteid = siteid;
            this.feature_url = feature_url;
            this.is_point = is_point;
            this.point = point;
            this.bbox = bbox;
            
            this.initInfoExpander();
            
            this.makeMap();
            window['leafmap'] = this.map;
            
            this.loadFeature();
            this.zoomToFeature();
            console.log('postzoom');
        },
        
        initInfoExpander: function() {
            var that = this;
            $('#infoexpander, #siteinfotitle').on('click', function(e) {
                $('#siteinfo').toggleClass('collapsed');
            });
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
				{id: 10, maxZoom: 10, opacity: 1, attribution: 'Basemap &copy; ESRI'}
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
			
			/*
			// Designated Marine Protected Areas
			lyr = new L.TileLayer(
				'https://tile{s}.mpatlas.org/tilecache/mpas/{z}/{x}/{y}.png',
				{id: 1, maxZoom: 10, opacity: 0.9, tms: false, subdomains: subdomains, color: '#0000AA'}
			);
			this.overlayLayers['Designated Marine Protected Areas'] = lyr;
			this.layers.push(lyr);
			this.mpalayer = lyr;
			
			// Candidate Marine Protected Areas
			lyr = new L.TileLayer(
				'https://tile{s}.mpatlas.org/tilecache/candidates/{z}/{x}/{y}.png',
				{id: 2, maxZoom: 10, opacity: 0.6, tms: false, subdomains: subdomains, color: '#FF8000'}
			);
			this.overlayLayers['Candidate Marine Protected Areas'] = lyr;
			//this.layers.push(lyr);
			*/
			
            this.map = new L.Map(this.mapelem, {
				center: new L.LatLng(0, 0),
				zoom: 2,
				layers: this.layers,
				worldCopyJump: true,
				minZoom: 0,
				maxZoom: 18,
				attributionControl:false,
				touchZoom: true // needed for Android tablets
			});

			//this.map.attributionControl.setPrefix('');
			
            var map = this.map; // use this var for closures inside event handlers

            var that = this;

            // Designated Marine Protected Areas
            lyr = cartodb.createLayer(this.map, 'https://mpatlas.cartodb.com/api/v2/viz/15af8902-c9dc-11e4-a3d3-0e0c41326911/viz.json',
            	{
            		cartodb_logo: false,
            		legends: false
            	})
                .on('done', function(layer) {
                  layer.options.attribution = 'MPA data from <a href="https://www.mpatlas.org">MPAtlas</a>, <a href="http://www.protectedplanet.net">WDPA/ProtectedPlanet</a>, <a href="http://www.mpa.gov">US MPA Center</a>';
                  that.overlayLayers['Designated Marine Protected Areas'] = layer;
                  that.layers.unshift(layer);
                  that.mpalayer = layer;
                })
                .on('error', function(err) {
                  alert("some error occurred: " + err);
                })
                .addTo(this.map);

            /*
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
			*/
			
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
    		                that.map.setZoom(6);
    		            } else {
    		                that.map.zoomOut();
    	                }
    		        }
    		    })();
	        }
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
                        fillOpacity: 0.4
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
                // success: function(data) {
                // 	geojson_tiles = L.vectorGrid.slicer(data, {
                // 		vectorTileLayerStyles: {
                // 			sliced: {
                // 				weight: 3,
                // 				color: '#d0508c',
                // 				opacity: 0.8,
                // 				fillColor: '#d0508c',
                // 				fillOpacity: 0.4
                // 			}
                // 		}
                // 	})
                //     if (that.highlightlayer) {
                //         that.map.removeLayer(that.highlightlayer);
                //     }
                //     delete that.highlightlayer;
                //     geojson_tiles.on('click', function(mapevent) {
                //         that.map.fireEvent('click', mapevent); // pass click from layer to map
                //     });
                //     that.map.addLayer(geojson_tiles);
                //     // console.log('added geojson tiles', geojson_tiles);
                //     that.highlightlayer = geojson_tiles;
                //     if (!that.bbox[0][0]) {
                //         that.map.fitBounds(that.highlightlayer.getBounds());
                //     }
                // }
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
        SiteDetail: SiteDetail
    };
    // What we return here will be used by other modules
});
