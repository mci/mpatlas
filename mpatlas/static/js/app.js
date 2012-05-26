define(
	[
		// These are path aliases configured in the requireJS bootstrap
		//'backbone-module',
		'jquery',
		'use!backbone',
		'leaflet',
		'TileLayer.Bing',
		'persist'
	],
	
	function ($, Backbone) {  
		var _MPAtlas = Backbone.View.extend({
			//** TODO be sure to set the proxy and domain before sending to production!
			proxy: '',
			domain: 'http://' + document.domain + '/',
			/*
			proxy: '/terraweave/features.ashx?url=',
			domain: 'http://mpatlas.org/',
			*/
			
			exploreModes: ['mpas', 'nation', 'meow', 'fao'],
			currentMode: 'mpas',			
	
			initialize: function (map) {
	
				if ($.type(map) === 'object') {
					this.mapelem = (map.length) ? map[0] : map;
				} else {
					this.mapelem = $('#' + map)[0]; // Assume it's an element id string
				}
	
				this.makeMap();
	
				this.utils = new MPAtlas.Utils({
					mpatlas: this
				});
				this.history = new MPAtlas.History({
					mpatlas: this
				});
				this.getMapState();										
				this.initMapHover(); // do the hover initialization last
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
					{id: 0, maxZoom: 9, opacity: 1}
				);
				this.bgLayers['World Oceans'] = lyr;
				this.layers.push(lyr);
		
				// Bing background layer for testing
				lyr = new L.TileLayer.Bing(
					'http://ecn.t{subdomain}.tiles.virtualearth.net/tiles/r{quadkey}.jpeg?g=850&mkt=en-us&n=z&shading=hill',
					{id: 2, maxZoom: 18, opacity: 0.6}
				);
				this.bgLayers['Bing World Map'] = lyr;
	
				// EEZs / Nations		
				lyr = new L.TileLayer(
					'http://tile{s}.mpatlas.org/tilecache/eezs/{z}/{x}/{y}.png',
					{id: 3, maxZoom: 9, opacity: 0.2, scheme: 'tms', subdomains: subdomains}
				);
				this.overlayLayers['Exclusive Economic Zones'] = lyr;
				this.layers.push(lyr);
				
				// Marine Eco-Regions
				lyr = new L.TileLayer(
					'http://tile{s}.mpatlas.org/tilecache/meow/{z}/{x}/{y}.png',
					{id: 4, maxZoom: 9, opacity: 0.4, scheme: 'tms', subdomains: subdomains}
				);
				this.overlayLayers['Marine Eco-Regions'] = lyr;
				
				// FAO Fishing Zones
				lyr = new L.TileLayer(
					'http://tile{s}.mpatlas.org/tilecache/fao/{z}/{x}/{y}.png',
					{id: 5, maxZoom: 9, opacity: 0.4, scheme: 'tms', subdomains: subdomains}
				);
				this.overlayLayers['FAO Fishery Mgmt Regions'] = lyr;
				
				// Designated Marine Protected Areas
				lyr = new L.TileLayer(
					'http://tile{s}.mpatlas.org/tilecache/mpas/{z}/{x}/{y}.png',
					{id: 6, maxZoom: 9, opacity: 0.5, scheme: 'tms', subdomains: subdomains}
				);
				this.overlayLayers['Designated Marine Protected Areas'] = lyr;
				this.layers.push(lyr);
				
				// Candidate Marine Protected Areas
				lyr = new L.TileLayer(
					'http://tile{s}.mpatlas.org/tilecache/candidates/{z}/{x}/{y}.png',
					{id: 7, maxZoom: 9, opacity: 0.6, scheme: 'xyz', subdomains: subdomains}
				);
				this.overlayLayers['Candidate Marine Protected Areas'] = lyr;
				this.layers.push(lyr);
	
				this.map = new L.Map(this.mapelem, {
					center: new L.LatLng(0, 0),
					zoom: 2,
					layers: this.layers,
					minZoom: 0,
					maxZoom: 9,
					attributionControl: false
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
						mpatlas.saveMapLocation();
					} catch (ex) {}
				});
	
				this.map.on('moveend', function (e) {
					try {
						mpatlas.saveMapLocation();
					} catch (ex) {}
				});
	
				this.map.on('layeradd', function (e) {
					try {
						mpatlas.layerAdded(e);
					} catch (ex) {}
				});
	
				this.map.on('layerremove', function (e) {
					try {
						mpatlas.layerRemoved(e);
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
	
			switchToMapView: function () {
				$('#btnListMode').removeClass('selected');
				$('#btnMapMode').addClass('selected');
				$('.leaflet-control-container').show();
				
				$('#body_list_full').fadeOut(600);
				
				// TODO The code below is really hacky, clean up maptip api when we can
				//mpatlas.maptip.enableMapTip(); // Not needed, maphover events will bring it back automatically
				if (mpatlas.maptip.locked) {
					mpatlas.maptip.disable = false;
					mpatlas.maptip.showMapTip();
				}
			},
			
			switchToListView: function () {
				if (!MPAList.List) {
					document.location.href = this.domain + 'mpa/sites/';
					return;
				}

				mpatlas.maptip.disableMapTip();
				$('#btnMapMode').removeClass('selected');
				$('#btnListMode').addClass('selected');
				$('.leaflet-control-container').hide();

				$('#body_list_full').fadeIn(600);
				
				if (MPAList.List) {
					// wait slightly for the fade in
					new Ext.util.DelayedTask(function () {
						MPAList.List.resizeGrid();
					}).delay(100);
				}
	
			},
			
			getMapState: function () {
				var qs = new this.utils.queryString();
				var y = qs.get('lat');
				var x = qs.get('lng');
				if (y && !x) {
					x = qs.get('lon');
				} else if (!y) {
					x = qs.get('x');
					y = qs.get('y');
				}
				var z = qs.get('zoom');
				if (!z) {
					z = qs.get('z');
				}
				
				if (x && y && z) {
					if (z === this.map.getZoom()) {
						this.map.panTo(new L.LatLng(y, x));					
					} else {
						this.map.setView(new L.LatLng(y, x), z);
					}
				} else {
					var location = null;
					try {
						location = this.history.get('location', true);
					} catch (e) {}
					if (location && location.center) {
						if (location.zoom === this.map.getZoom()) {
							this.map.panTo(location.center);					
						} else {
							this.map.setView(location.center, location.zoom);
						}
					} else {
						
						// get the users location
						this.map.on('locationfound', function (location) {
							mpatlas.map.panTo(location.latlng);
						});
						this.map.locate();
					}				
				}
	
				var explMode = null;
				try {
					explMode = this.history.get('exploreMode');
				} catch (e2) {}
				this.setExploreMode(explMode || this.currentMode);				
			},
			
			layerAdded: function (e) {
				var lyr = e.layer;
			},
			
			layerRemoved: function (e) {
				var lyr = e.layer;
			},

			setExploreMode: function (mode) {
				this.currentMode = mode;
				try {
					this.history.set('exploreMode', mode);						
				} catch (e) {}
				$('.explore_button.selected').removeClass('selected');
				$('#explore_' + mode).addClass('selected');
				if (this.maptip) {
					this.maptip.disableMapTip();
					this.maptip.toggleEvents(true);
				}
			},
			
			saveMapLocation: function () {
				var loc = {
					center: mpatlas.map.getCenter(),
					zoom: mpatlas.map.getZoom()
				};
				mpatlas.history.set('location', loc, true);			
			},
			
			zoomToMPA: function (options) {
				
				// add a marker
				if (this.marker) {
					this.map.removeLayer(this.marker);	
				}
				var ptLL = new L.LatLng(options.pt[1], options.pt[0]);
				this.marker = new L.Marker(ptLL);
				this.marker.on('click', function () {
					document.location = mpatlas.domain + 'mpa/sites/' + options.id + '/';
				});
				this.map.addLayer(this.marker);

				// zoom to the bbox
				var bb = options.bbox;
				var sw = new L.LatLng(bb[1], bb[0]);
				var ne = new L.LatLng(bb[3], bb[2]);
				var bnds = new L.LatLngBounds(sw, ne);
				this.map.fitBounds(bnds);
				this.switchToMapView();
			},
	
			initMapHover: function () {
				// Make map fire hover event after 500ms mouse pause, used by feature layer lookups
				this.initMapHoverEvents(500, 1);
	
				this.maptip = new MPAtlas.MapTip({
					el: $('#maptip')[0],
					mpatlas: this
				}); // setup maptip element and behavior
				
				this.maptip.enableMapTip();
				this.maptip.disableMapTip();
				
				this.registerMapHover(); // assign actions on mouse hover/pause and click for map layer feature lookup
				//this.maptip.toggleEvents(true); // activate the maptip event registration
	
				//$('#maptip-content').html('');
				//this.maptip.disableMapTip();
			},
			
			registerMapHover: function () {
				var mpatlas = this;
				var maptip = this.maptip;
				var check_point_distance = function(mapevent) {
				    maptip.pointstillgood = true;
				    var pixeltolerance = 4;
				    if (maptip.lastPoint) {
				        if (Math.abs(mapevent.layerPoint.x - maptip.lastPoint.x) > pixeltolerance || Math.abs(mapevent.layerPoint.y - maptip.lastPoint.y) > pixeltolerance) {
				            maptip.pointstillgood = false;
				        }
				    }
				    maptip.lastPoint = mapevent.layerPoint;
				    return maptip.pointstillgood;
				};
				var load_mpa_maptip = function(mapevent) {
				    var radius = mpatlas.getPixelRadius(2);
				    var latlng = mapevent.latlng;
				    url = mpatlas.domain + 'mpa/lookup/point/?lon=' + latlng.lng + '&lat=' + latlng.lat + '&radius=' + radius;
					if (mpatlas.proxy && mpatlas.proxy !== '') {
						url = mpatlas.proxy + escape(url);
					}
					$.ajax({
						url: url,
						success: function (data) {
							mpatlas.featuredata = data;
							var mpahtml = '';
							mpahtml += '<span style="font-weight:bold;">Click to explore these MPAs:</span>';
							var len = data.mpas.length;
							var i = 0;
							for (i = 0; i < len; i++) {
								mpa = data.mpas[i];
								//mpahtml += '<a class="maptip_mpalink" href="' + mpatlas.domain + 'mpa/sites/' + mpa.id + '/' + '"><span style="float:right; margin-left:3px; font-style:italic;">(' + mpa.country + ')</span>' + mpa.name + '</a>';
								mpahtml += '<a class="maptip_mpalink" href="' + mpa.url + '"><span style="float:right; margin-left:3px; font-style:italic;">(' + mpa.country + ')</span>' + mpa.name + '</a>';
							}
							if (data.mpas.length === 0) {
								//mpahtml = 'No MPAs at this location';
                                mpahtml = '';
                                $(mpatlas.mapelem).removeClass('busy'); // Remove progress cursor when done searching
                                maptip.disableMapTip();
								return;											
							}
							$('#maptip-content').data('latlon', {
								lat: latlng.lat,
								lon: latlng.lon
							});
							$(mpatlas.mapelem).removeClass('busy'); // Remove progress cursor when done searching
							$('#maptip-content').html(mpahtml);
							maptip.enableMapTip();
						    maptip.toggleEvents(false);
							//maptip.showMapTip();
							maptip.offset = $('#leafletmap').offset();
						},
						error: function () {
							$(mpatlas.mapelem).removeClass('busy'); // Add progress cursor when searching
						}
					});
				};
				var load_region_maptip = function(mapevent) {
				    var radius = mpatlas.getPixelRadius(2);
				    //var radius = 0.00000001;
				    var latlng = mapevent.latlng;
					url = mpatlas.domain + 'region/' + mpatlas.currentMode + '/lookup/point/?lon=' + latlng.lng + '&lat=' + latlng.lat + '&radius=' + radius;
					if (mpatlas.proxy && mpatlas.proxy !== '') {
						url = mpatlas.proxy + escape(url);
					}
					$.ajax({
						url: url,
						success: function (data) {
							mpatlas.featuredata = data;
							var mpahtml = '';
							mpahtml += '<span style="font-weight:bold;">Click to explore this region:</span>';
							if (data.regions.length > 0) {
								var region = data.regions[0]; // Just report one region at a time
								mpahtml += '<a class="maptip_mpalink" href="/region/' + mpatlas.currentMode + '/' + region.id + '">';
								mpahtml += '<span style="float:right; margin-left:3px; font-style:italic;">(' + region.country + ')</span>' + region.name + '</a>';
								mpahtml += '<span style="font-size:11px;">Total Marine Area: <strong>' + region.area_km2 + ' km2</strong>';
								mpahtml += '<br /># of MPAs: <strong>' + region.mpas + '</strong>';
								mpahtml += '<br />Total Marine Area in MPAs: <strong>' + region.percent_in_mpas + '%</strong>';
								mpahtml += '<br />Total Marine Area No Take: <strong>' + region.percent_no_take + '%</strong></span>';

								// Load feature from GeoJSON
								url = mpatlas.domain + 'region/' + mpatlas.currentMode + '/' + region.id + '/features/';
								if (mpatlas.proxy && mpatlas.proxy !== '') {
									url = mpatlas.proxy + escape(url);
								}

								$.ajax({
									url: url,
									success: function (data) {
										var geojson = new L.GeoJSON(data);
										geojson.setStyle({
											weight: 3,
											color: '#1FF',
											opacity: 0.5,
											fillColor: '#1FF',
											fillOpacity: 0.3
										});
										if (mpatlas.highlightlayer) {
											mpatlas.map.removeLayer(mpatlas.highlightlayer);
										}
										delete mpatlas.highlightlayer;
										geojson.on('click', function (mapevent) {
											mpatlas.map.fireEvent('click', mapevent); // pass click from layer to map
										});
										mpatlas.map.addLayer(geojson);
										mpatlas.highlightlayer = geojson;
									}
								});
								
							} else {
								//mpahtml = 'No Region at this location';
								mpahtml = '';
								$(mpatlas.mapelem).removeClass('busy'); // Remove progress cursor when done searching
								maptip.disableMapTip();
								return;
							}
							$('#maptip-content').data('latlon', {
								lat: latlng.lat,
								lon: latlng.lon
							});
							$('#maptip-content').html(mpahtml);
							$(mpatlas.mapelem).removeClass('busy'); // Remove progress cursor when done searching
							maptip.enableMapTip();
						    maptip.toggleEvents(false);
							//maptip.showMapTip();
							maptip.offset = $('#leafletmap').offset();
						},
						error: function (xhr, ajaxOptions, thrownError) {
                            $(mpatlas.mapelem).removeClass('busy'); // Add progress cursor when searching
                        }
					});
				};
				var clearMapTip = function(nothing, hideimmediately) {
				    mpatlas.featuredata = {};
					$('#maptip-content').html($('#maptip-content').data('orightml'));
					if (mpatlas.highlightlayer) {
						mpatlas.map.removeLayer(mpatlas.highlightlayer);
					}
					//maptip.disableMapTip();
					//maptip.toggleEvents(true);
					maptip.locked = false;
					maptip.hideMapTip(null, hideimmediately);
				};
				maptip.clearMapTip = clearMapTip;
				var handlers = {
					
					maphover: function (e, mapevent) {
						// stop if layer list is expanded because that means we are over the top of it
						var lyrContainer = $('.leaflet-control-layers-expanded');
						if (lyrContainer.length > 0) {
							return;
						}
						
						var url = null;
						if (!maptip.locked) {
						    check_point_distance(mapevent);
							var ll = mapevent.latlng;
							if (typeof $('#maptip-content').data('orightml') === 'undefined') {
								$('#maptip-content').data('orightml', $('#maptip-content').html());
							}
							//maptip.enableMapTip();
							$(mpatlas.mapelem).addClass('busy'); // Add progress cursor when searching

							switch (mpatlas.currentMode) {
	
							case 'mpas':
							    if (!maptip.pointstillgood) {
							        hideimmediately = true;
							        maptip.hideMapTip(null, hideimmediately);
							    }
							    clearTimeout(maptip.hovercleartimer);
								maptip.moveMapTip();
								load_mpa_maptip(mapevent);
								break;
	
							case 'nation':
							case 'meow':
							case 'fao':
								//$('#maptip-content').html('Searching for Region...');
								if (!maptip.pointstillgood) {
							        hideimmediately = true;
							        maptip.hideMapTip(null, hideimmediately);
							    }
							    clearTimeout(maptip.hovercleartimer);
								maptip.moveMapTip();
								load_region_maptip(mapevent);
								break;
							}
						}
					},
					
					maphoverclear: function (e, mapevent) {
						if (!maptip.locked) {
							clearMapTip(null, false);
						} else {
						    if (!maptip.mouseover) {
						        maptip.hovercleartimer = setTimeout(maptip.clearMapTip, 3000);
					        }
						}
					},
					
					mapclick: function (mapevent) {
						//if (!maptip.locked) {
						if (true) {
						    check_point_distance(mapevent);
						    $(mpatlas.mapelem).addClass('busy'); // Add progress cursor when searching
							switch (mpatlas.currentMode) {
							case 'mpas':
							    clearTimeout(maptip.hovercleartimer);
								if (maptip.pointstillgood && mpatlas.featuredata && mpatlas.featuredata.mpas && mpatlas.featuredata.mpas.length === 1) {
									//window.location = mpatlas.domain + 'mpa/sites/' + mpatlas.featuredata.mpas[0].id + '/';
									window.location = mpatlas.featuredata.mpas[0].url;
								} else if (maptip.pointstillgood && mpatlas.featuredata && mpatlas.featuredata.mpas) {
								    maptip.enableMapTip();
								    maptip.toggleEvents(false);
								    //maptip.hideMapTip();
								    maptip.moveMapTip();
									load_mpa_maptip(mapevent);
								} else {
								    maptip.enableMapTip();
								    maptip.toggleEvents(false);
    							    hideimmediately = true;
    							    maptip.hideMapTip(null, hideimmediately);
								    maptip.hideMapTip();
								    maptip.moveMapTip();
									load_mpa_maptip(mapevent);
								}
								break;
							case 'nation':
							case 'meow':
							case 'fao':
							    clearTimeout(maptip.hovercleartimer);
								if (maptip.pointstillgood && mpatlas.featuredata && mpatlas.featuredata.regions && mpatlas.featuredata.regions.length === 1) {
									window.location = mpatlas.domain + 'region/' + mpatlas.currentMode + '/' + mpatlas.featuredata.regions[0].id + '/';
								} else if (maptip.pointstillgood && mpatlas.featuredata && mpatlas.featuredata.regions) {
								    maptip.enableMapTip();
								    maptip.toggleEvents(false);
								    //maptip.hideMapTip();
								    maptip.moveMapTip();
									load_region_maptip(mapevent);
								} else {
								    maptip.enableMapTip();
								    maptip.toggleEvents(false);
    							    hideimmediately = true;
    							    maptip.hideMapTip(null, hideimmediately);
								    maptip.hideMapTip();
								    maptip.moveMapTip();
									load_region_maptip(mapevent);
								}
								break;
							}
						} else {
							mpatlas.featuredata = {};
							$('#maptip-content').html($('#maptip-content').data('orightml'));
							if (mpatlas.highlightlayer) {
								mpatlas.map.removeLayer(mpatlas.highlightlayer);
							}
							maptip.disableMapTip(null, true); // immediate hide
							maptip.toggleEvents(true);
						}
					}
				};
				$(this.map).on('maphover', handlers.maphover);
				$(this.map).on('maphoverclear', handlers.maphoverclear);
				this.map.on('click', handlers.mapclick);
			},
	
			initMapHoverEvents: function (delay, pixeltolerance) {
				var map = this.map, hovertimer, hovered = false, lastpoint = {
					x: -9999,
					y: -9999
				};
				delay = (delay) ? delay : 250;
				pixeltolerance = (pixeltolerance) ? pixeltolerance : 1;
				
				this.map.on('mousemove', function (e) {
					clearTimeout(hovertimer);
					// this is a leaflet map MouseEvent, not a jquery event
					if (hovered && (Math.abs(e.layerPoint.x - lastpoint.x) > pixeltolerance || Math.abs(e.layerPoint.y - lastpoint.y) > pixeltolerance)) {
						hovered = false;
						$(map).trigger('maphoverclear', [e]);
					} else if (!hovered) {
						hovertimer = setTimeout(function () {
							lastpoint = {
								x: e.layerPoint.x,
								y: e.layerPoint.y
							};
							hovered = true;
							$(map).trigger('maphover', [e]);
						}, delay);
					}
				});
				this.map.on('mouseout', function (e) {
					clearTimeout(hovertimer);
					hovered = false;
					$(map).trigger('maphoverclear', [e]);
				});
	
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
		
		MPAtlas = {};

		MPAtlas.Utils = Backbone.View.extend({
			initialize: function (options) {
				this.mpatlas = options.mpatlas;
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
	
		MPAtlas.History = Backbone.View.extend({
			initialize: function (options) {
				this.mpatlas = options.mpatlas;
				this.localStorage = new Persist.Store('MPAtlas', {
					about: 'Local Store for MPAtlas',
					expires: 0.125 // 1/8 day or 3 hours
				});
				
			},
			
			set: function (key, value, encode) {
				try {
					if (encode) {
						value = JSON.stringify(value);
					}
					this.localStorage.set(key, value);			
				} catch (e) {}
			},
			
			get: function (key, decode) {
				var val = null;
				try {
					var value = this.localStorage.get(key);
					if (decode) {
						val = JSON.parse(value);
					}
				} catch (e) {}
				return val;
			}
		});
	
		MPAtlas.MapTip = Backbone.View.extend({
			// define maptip behaviors and initialize
			initialize: function (options) {
				var elem = options.el;
				var mpatlas = options.mpatlas;
				var maptip = this;
				this.elem = elem;
				this.elem.maptip = this;
				this.mpatlas = mpatlas;
				//var popuppane = mpatlas.map.getPanes().popupPane;
				//$('#maptip').appendTo(popuppane);
				$(elem).appendTo(mpatlas.mapelem);
				this.timer = null;
				this.disable = true;
				this.offset = {
					left: -9999,
					top: -9999
				};
	            maptip.locked = true; // initial value needs to be true
	            
	            maptip.mouse = {x:-9999, y:-9999};
	            $(window).on('mousemove.maptipnow', function(e) {
	                maptip.mouse.y = e.pageY - maptip.offset.top;
					maptip.mouse.x = e.pageX - maptip.offset.left;
	            });
	            
	            // Prevent mouse events from hitting map when we're over maptip
	            // $(this.elem).on('mousedown mouseup mousemove click dblclick scroll', function(e) {
	            $(this.elem).on('mousedown mouseup mousemove click dblclick scroll', function(e) {
	                e.stopPropagation();
	                // return false; // This will prevent links from working, so don't do it.
	            });
	            
				//var offsetX = event.pageX - offset.left;
				//var offsetY = event.pageY - offset.top;
				this.showMapTip = function (event) {
					maptip.hidden = false;
					if (!maptip.disable) {
						$('#maptip').removeClass('nodisplay').removeClass('hidden').removeClass('transparent');
						clearTimeout(maptip.timer);
						maptip.offset = $('#leafletmap').offset();
					}
				};
	
				this.hideMapTip = function (event, immediate) {
					if (immediate) {
						$('#maptip').addClass('nodisplay').addClass('hidden');
					} else {
						maptip.timer = setTimeout(function () {
							$('#maptip').addClass('hidden');
						}, 500);
					}
					$('#maptip').addClass('transparent');
				};
	
				this.moveMapTip = function (event) {
					//var offset = $(event.delegateTarget).offset();
					//var offsetX = event.pageX - offset.left;
					//var offsetY = event.pageY - offset.top;
					//$('#maptip').css({'top': offsetY, 'left': offsetX});
					var x = maptip.mouse.x;
					var y = maptip.mouse.y;
					if (event) {
					    x = event.pageX - maptip.offset.left;
					    y = event.pageY - maptip.offset.top;
					}
					$('#maptip').css({
						'top': y,
						'left': x
					});
				};
	
				this.disableMapTip = function (e, immediatehide) {
					maptip.disable = true;
					maptip.hideMapTip(e, immediatehide); // true = hide immediate, false = fade out
				};
	
				this.enableMapTip = function (e) {
					maptip.disable = false;
					if (maptip.locked) {
						maptip.toggleEvents(true); //  break locked maptip by renabling mouse events
					}
					maptip.showMapTip(e);
				};
	
				//mpatlas.map.on('movestart', maptip.disableMapTip);
				mpatlas.map.on('movestart', function() {
				    maptip.clearMapTip();
				    maptip.disableMapTip();
				});
				//mpatlas.map.on('moveend', maptip.enableMapTip);
				mpatlas.map.on('moveend', function () {
					maptip.toggleEvents(true);
				});
			},
	        
	        clearMapTip: function (nothing, hideimmediately) {
	            // stub function, gets filled out by mpatlas
	        },
	        
	        cancelHoverClear: function () {
	            var maptip = this.maptip;
	            maptip.mouseover = true;
	            if (maptip.hovercleartimer) {
				    clearTimeout(maptip.hovercleartimer);
				}
				// Disable map zooming while over maptip
				var map = maptip.mpatlas.map;
				map.doubleClickZoom.disable();
	            map.scrollWheelZoom.disable();
	            map.touchZoom.disable();
	            map.boxZoom.disable();
	            map.dragging.disable();
	        },
	        
	        setHoverClear: function () {
	            var maptip = this.maptip;
	            maptip.mouseover = false;
	            maptip.hovercleartimer = setTimeout(maptip.clearMapTip, 3000);
	            // Reenable map zooming when leaving maptip
	            var map = maptip.mpatlas.map;
	            map.doubleClickZoom.enable();
	            map.scrollWheelZoom.enable();
	            map.touchZoom.enable();
	            map.boxZoom.enable();
	            map.dragging.enable();
	        },
	        
			// make maptip responsive (or not responsive) to mouse and map events
			// effectively locks maptip on page
			toggleEvents: function (respond_to_events) {
				var maptip = this;
				if ($.type(respond_to_events) === 'undefined' || respond_to_events) {
	                if (this.locked) {
						// enable maptip events
						// jquery custom events that prevents mouseover bubbling from child nodes
						//$(this.mpatlas.mapelem).on('mouseenter.maptipwindow', this.showMapTip);
						$(this.mpatlas.mapelem).on('mouseleave.maptipwindow', this.hideMapTip);
						$(window).on('mousemove.maptip', this.moveMapTip);

						this.locked = false;
					}
				} else {
					// disable maptip event tracking
					// jquery custom events that prevents mouseover bubbling from child nodes
					//$(this.mpatlas.mapelem).off('mouseenter.maptipwindow', this.showMapTip);
					$(this.mpatlas.mapelem).off('mouseleave.maptipwindow', this.hideMapTip);
					$(window).off('mousemove.maptip', this.moveMapTip);
	
					//this.map.off('movestart', maptip.disableMapTip);
					//this.map.off('moveend', maptip.enableMapTip);
	
					this.locked = true;
				}
				$(maptip.elem).off('mouseenter.maptip', this.cancelHoverClear);
				$(maptip.elem).off('mouseleave.maptip', this.setHoverClear);
				$(maptip.elem).on('mouseenter.maptip', this.cancelHoverClear);
				$(maptip.elem).on('mouseleave.maptip', this.setHoverClear);
			}
		});
	
	
		return {
			MPAtlas: _MPAtlas
		};
		// What we return here will be used by other modules
	}
);