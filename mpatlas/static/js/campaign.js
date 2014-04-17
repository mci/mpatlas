define(
	[
		// These are path aliases configured in the requireJS bootstrap
		//'backbone-module',
		'jquery',
		'use!backbone',
		'leaflet',
		'TileLayer.Bing',
		'leaflet_utils',
		'leaflet_maptip',
		'spin.min',
		'persist'
	].concat(!(typeof JSON !== 'undefined' && typeof JSON.stringify === 'function') ? ['json2'] : []),
	
	function ($, Backbone) {
		var spinner_opts = {
				lines: 8, // The number of lines to draw
				length: 2, // The length of each line
				width: 2, // The line thickness
				radius: 2, // The radius of the inner circle
				rotate: 0, // The rotation offset
				color: '#FFF', // #rgb or #rrggbb
				//color: '#E03E6F', // #rgb or #rrggbb
				speed: 2, // Rounds per second
				trail: 60, // Afterglow percentage
				shadow: true, // Whether to render a shadow
				hwaccel: false, // Whether to use hardware acceleration
				className: 'spinner', // The CSS class to assign to the spinner
				zIndex: 2e9, // The z-index (defaults to 2000000000)
				top: 'auto', // Top position relative to parent in px
				left: 'auto' // Left position relative to parent in px
		};
	    
		var _CampaignMap = Backbone.View.extend({
			//** TODO be sure to set the proxy and domain before sending to production!
			proxy: '',
			domain: 'http://' + document.domain + '/',
			/*
			proxy: '/proxy/?mode=native&url=',
			domain: 'http://dev.mpatlas.org/',
			*/
			
			hoverdelay: 250,
			hoverdelay_click: 3500,			
	
			initialize: function (map) {
	
				if ($.type(map) === 'object') {
					this.mapelem = (map.length) ? map[0] : map;
				} else {
					this.mapelem = $('#' + map)[0]; // Assume it's an element id string
				}
	
				this.makeMap();
	
				this.utils = new CampaignMap.Utils({
					campaignmap: this
				});
			},
	
			// create Leaflet map
			makeMap: function () {
	
				this.layers = [];
				this.bgLayers = {};
				this.overlayLayers = {};
				var subdomains = '12345678'; // tile1.mpatlas.org, tile2...
	
				// ESRI Oceans Layer
				var lyr = new L.TileLayer(
					'http://services.arcgisonline.com/ArcGIS/rest/services/Ocean_Basemap/MapServer/tile/{z}/{y}/{x}.png',
					{id: 10, maxZoom: 10, opacity: 1, attribution: 'Basemap &copy; ESRI'}
				);
				this.bgLayers['World Oceans'] = lyr;
				this.layers.push(lyr);
		
				// Bing background layer for testing
				lyr = new L.TileLayer.Bing(
					'AnrVx0YzYa6emmkAQPBI9Ka1uY1ZFKPDC7fGYntZX2PJkJFTNgmEKfUTFC_3EI_e',
					{type: 'Road', id: 2, maxZoom: 18, opacity: 1}
				);
				this.bgLayers['Bing World Map'] = lyr;
	
				// Designated Marine Protected Areas
				lyr = new L.TileLayer(
					'http://tile{s}.mpatlas.org/tilecache/mpas/{z}/{x}/{y}.png',
					{id: 1, maxZoom: 10, opacity: 0.3, tms: false, subdomains: subdomains, color: '#0000AA', attribution: 'MPA data from <a href="http://www.mpatlas.org">MPAtlas</a>, <a href="http://www.protectedplanet.net">WDPA/ProtectedPlanet</a>, <a href="http://www.mpa.gov">US MPA Center</a>'}
				);
				this.overlayLayers['Designated Marine Protected Areas'] = lyr;
				this.layers.push(lyr);
				this.mpalayer = lyr;
				
				// Candidate Marine Protected Areas
				lyr = new L.TileLayer(
					'http://tile{s}.mpatlas.org/tilecache/candidates/{z}/{x}/{y}.png',
					{id: 2, maxZoom: 10, opacity: 0.2, tms: false, subdomains: subdomains, color: '#FF8000'}
				);
				this.overlayLayers['Candidate Marine Protected Areas'] = lyr;
				this.layers.push(lyr);
	
				// EEZs / Nations		
				lyr = new L.TileLayer(
					'http://tile{s}.mpatlas.org/tilecache/eezs/{z}/{x}/{y}.png',
					{id: 3, maxZoom: 10, opacity: 0.2, tms: true, subdomains: subdomains, color: '#01DF74'}
				);
				this.overlayLayers['Exclusive Economic Zones'] = lyr;
				this.layers.push(lyr);
				
				// Marine Eco-Regions
				lyr = new L.TileLayer(
					'http://tile{s}.mpatlas.org/tilecache/meow/{z}/{x}/{y}.png',
					{id: 4, maxZoom: 10, opacity: 0.4, tms: true, subdomains: subdomains, color: '#CC00CC'}
				);
				this.overlayLayers['Marine Eco-Regions'] = lyr;
				
				// FAO Fishing Zones
				lyr = new L.TileLayer(
					'http://tile{s}.mpatlas.org/tilecache/fao/{z}/{x}/{y}.png',
					{id: 5, maxZoom: 10, opacity: 0.4, tms: true, subdomains: subdomains, color: '#FFFF00'}
				);
				this.overlayLayers['FAO Fishery Mgmt Regions'] = lyr;
				
				this.map = new L.Map(this.mapelem, {
					center: new L.LatLng(0, 0),
					zoom: 2,
					layers: this.layers,
					worldCopyJump: true,
					minZoom: 0,
					maxZoom: 14,
					attributionControl: true,
					touchZoom: true // needed for Android tablets
				});

				this.map.attributionControl.setPrefix('');
				
				var map = this.map; // use this var for closures inside event handlers

				// In case you need multiple markers on each of the "wrapped" worlds when zoomed out, or when
				// working near the dateline, need to make multiple markers with the 'true' 3rd parameter.
				// Also need to translate polylines, polygons, and GeoJSON layers
				//var markerLocation = new L.LatLng(51.5, -0.09),
				//    markerLocation2 = new L.LatLng(markerLocation.lat, markerLocation.lng + 360, true),
				//    markerLocation3 = new L.LatLng(markerLocation.lat, markerLocation.lng - 360, true),
			},

			getPixelRadius: function (pxradius) {
				// Convert pixel radius to map units (web mercator = meters) then to km.
				// pxradius can be a floating point value
				var bounds = this.map.getBounds(),
					crs = this.map.options.crs; // undocumented access to map projection functions
				var resolution = (crs.project(bounds.getNorthEast()).y - crs.project(bounds.getSouthWest()).y) / this.map.getSize().y;
				return (resolution * pxradius) / 1000;
			}
		});
		
		CampaignMap = {};

		CampaignMap.Utils = Backbone.View.extend({
			initialize: function (options) {
				this.campaignmap = options.campaignmap;
			},
			
			queryString: function (qs) {
				this.get = function (key, def) {
					if (!def) {
						def = null;
					}
					var val = this.params[key];
					if (!val || val === null) {
						val = def;
					}
					return val;
				};
				this.params = {};
		
				if (!qs) {
					qs = location.search.substring(1, location.search.length);
				}
				if (qs.length === 0) {
					return;
				}
				qs = qs.replace(/\+/g, ' ');
				var args = qs.split('&');
				var len = args.length;
				var i = 0;
				for (i = 0; i < len; i++) {
					var value, name;
					var q = args[i].split('=');
					name = unescape(q[0]).toLowerCase();
					if (name !== '') {
						if (q.length === 2) {
							value = unescape(q[1]);
						} else {
							value = '';
						}
						this.params[name] = value;
					}
				}
			}
		});
	
		CampaignMap.MapTip = Backbone.View.extend({
			// define maptip behaviors and initialize
			initialize: function (options) {
	            maptip.mouse = {x:-9999, y:-9999};
	            $(window).on('mousemove.maptipnow', function(e) {
	                maptip.mouse.y = e.pageY - maptip.offset.top;
					maptip.mouse.x = e.pageX - maptip.offset.left;
	            });
			}
		});
	
	
		return {
			CampaignMap: _CampaignMap
		};
		// What we return here will be used by other modules
	}
);
