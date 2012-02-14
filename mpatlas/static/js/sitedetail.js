define([
  // These are path aliases configured in the requireJS bootstrap
  'backbone-module',
  'json2',
  'persist',
  'leaflet',
  'TileLayer.Bing',
  'MPAtlas.list'
],
function (Backbone) {  
    var SiteDetail = Backbone.View.extend({
		proxy: '',
		domain: 'http://' + document.domain,
		//proxy: '/terraweave/features.ashx?url=', // handle cross-domain if necessary. used for testing
		//domain: 'http://mpatlas.org/',
        
        initialize: function(map) {
            var that = this;
            if ($.type(map) === 'object') {
                this.mapelem = (map.length) ? map[0] : map;
            } else {
                this.mapelem = $('#' + map)[0]; // Assume it's an element id string
            }

            this.makeMap();
            window['leafmap'] = this.map;
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
			this.layers.push(lyr);
	
			// Bing background layer for testing
			var lyr = new L.TileLayer.Bing(
				'http://ecn.t{subdomain}.tiles.virtualearth.net/tiles/r{quadkey}.jpeg?g=850&mkt=en-us&n=z&shading=hill',
				{id: 2, maxZoom: 18, opacity: 0.6}
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

		zoomToMPA: function(id) {
			
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
