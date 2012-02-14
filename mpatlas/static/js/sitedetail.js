define([
  // These are path aliases configured in the requireJS bootstrap
  'backbone-module',
  'json2',
  'persist',
  'leaflet',
  //'MPAlist',
  'TileLayer.Bing'
],
function (Backbone) {  
    var SiteDetail = Backbone.View.extend({
		proxy: '',
		domain: 'http://' + document.domain,
		//proxy: '/terraweave/features.ashx?url=', // handle cross-domain if necessary. used for testing
		//domain: 'http://mpatlas.org/',
        
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

            this.makeMap();
            window['leafmap'] = this.map;
            
            this.loadFeature();
            this.zoomToFeature();
        },

        // create Leaflet map
        makeMap: function() {

			this.layers = [];
			this.bgLayers = {};
			this.overlayLayers = {};

			// ESRI Oceans Layer
			lyr = new L.TileLayer(
				'http://services.arcgisonline.com/ArcGIS/rest/services/Ocean_Basemap/MapServer/tile/{z}/{y}/{x}.png',
				{id: 0, maxZoom: 9, opacity: 1}
			);
			this.bgLayers['Oceans'] = lyr;
			//this.layers.push(lyr);
	
			// Bing background layer for testing
			var lyr = new L.TileLayer.Bing(
				'http://ecn.t{subdomain}.tiles.virtualearth.net/tiles/r{quadkey}.jpeg?g=850&mkt=en-us&n=z&shading=hill',
				{id: 2, maxZoom: 18, opacity: 1}
			);
			this.bgLayers['Bing Maps'] = lyr;
			this.layers.push(lyr);

			// EEZs / Nations		
			lyr = new L.TileLayer(
				'http://cdn.mpatlas.org/tilecache/eezs/{z}/{x}/{y}.png',
				{id: 5, maxZoom: 18, opacity: 0.4, scheme: 'tms'}
			);
			this.overlayLayers['Exclusive Economic Zones'] = lyr;
			//this.layers.push(lyr);
			
			// Marine Eco-Regions
			lyr = new L.TileLayer(
				'http://cdn.mpatlas.org/tilecache/meow/{z}/{x}/{y}.png',
				{id: 6, maxZoom: 18, opacity: 0.4, scheme: 'tms'}
			);
			this.overlayLayers['Marine Eco-Regions'] = lyr;
			
			// FAO Fishing Zones
			lyr = new L.TileLayer(
				'http://cdn.mpatlas.org/tilecache/fao/{z}/{x}/{y}.png',
				{id: 7, maxZoom: 18, opacity: 0.4, scheme: 'tms'}
			);
			this.overlayLayers['FAO Fishery Mgmt Regions'] = lyr;
			
			// Designated Marine Protected Areas
			lyr = new L.TileLayer(
				//'http://cdn.mpatlas.org/tilecache/mpas/{z}/{x}/{y}.png',
				'http://mpatlas.s3.amazonaws.com/tilecache/mpas/{z}/{x}/{y}.png',
				{id: 3, maxZoom: 18, opacity: 0.5, scheme: 'tms'}
			);
			this.overlayLayers['Designated Marine Protected Areas'] = lyr;
			this.layers.push(lyr);
			
			// Candidate Marine Protected Areas
			lyr = new L.TileLayer(
				'http://cdn.mpatlas.org/tilecache/candidates/{z}/{x}/{y}.png',
				{id: 4, maxZoom: 18, opacity: 0.6, scheme: 'xyz'}
			);
			this.overlayLayers['Candidate Marine Protected Areas'] = lyr;
			this.layers.push(lyr);

            this.map = new L.Map(this.mapelem, {
				center: new L.LatLng(0, 0),
				zoom: 2,
				layers: this.layers,
				minZoom: 0,
				maxZoom: 18,
				attributionControl:false
			});
			
            var map = this.map; // use this var for closures inside event handlers

			// override the position of layer control			
			L.Control.Layers.prototype.getPosition = function () {
				return L.Control.Position.BOTTOM_LEFT;
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
		    var sw = new L.LatLng(this.bbox[0][1], this.bbox[0][0], true);
		    var ne = new L.LatLng(this.bbox[1][1], this.bbox[1][0]);
		    var bounds = new L.LatLngBounds(sw, ne);
		    var startzoom = this.map.getZoom();
		    if (this.is_point) {
		        this.map.setView(sw, 6);
		    } else {
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
        SiteDetail: SiteDetail
    };
    // What we return here will be used by other modules
});
