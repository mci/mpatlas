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
    var MPAtlas = Backbone.View.extend({
		proxy: '',
		domain: 'http://' + document.domain,
		//proxy: '/terraweave/features.ashx?url=', // handle cross-domain if necessary. used for testing
		//domain: 'http://mpatlas.org/',
		
		exploreModes: ['mpas', 'eez', 'meow', 'fao'],
		defaultMode: 'mpas',
		currentMode: null,
        
        initialize: function(map) {
            var mpatlas = this;
            if ($.type(map) === 'object') {
                this.mapelem = (map.length) ? map[0] : map;
            } else {
                this.mapelem = $('#' + map)[0]; // Assume it's an element id string
            }

            this.makeMap();
            window['leafmap'] = this.map;

			this.utils = new MPAtlas.Utils({
				mpatlas: this
			});
            this.history = new MPAtlas.History({
				mpatlas: this
			});
            this.initExploreButtons();
            this.initMapHover();
			this.getMapState();
			
			this.list = Ext.create('MPAtlas.list.Grid', {mpatlas: this});

            // resize body and contained map element
            // Depending on how the page/viewport container and the map body div are css styled,
            // this may or may not be necessary.
			//_.bindAll(this, 'resizeViewport'); // make sure this refers to this when fired by event
            //this.resizeViewport();
            //$(window).resize(this.resizeViewport);

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

			// EEZs / Nations		
			lyr = new L.TileLayer(
				'http://cdn.mpatlas.org/tilecache/eezs/{z}/{x}/{y}.png',
				{id: 3, maxZoom: 9, opacity: 0.4, scheme: 'tms'}
			);
			this.overlayLayers['Exclusive Economic Zones'] = lyr;
			this.layers.push(lyr);
			
			// Marine Eco-Regions
			lyr = new L.TileLayer(
				'http://cdn.mpatlas.org/tilecache/meow/{z}/{x}/{y}.png',
				{id: 4, maxZoom: 9, opacity: 0.4, scheme: 'tms'}
			);
			this.overlayLayers['Marine Eco-Regions'] = lyr;
			
			// FAO Fishing Zones
			lyr = new L.TileLayer(
				'http://cdn.mpatlas.org/tilecache/fao/{z}/{x}/{y}.png',
				{id: 5, maxZoom: 9, opacity: 0.4, scheme: 'tms'}
			);
			this.overlayLayers['FAO Fishing Zones'] = lyr;
			
			// Designated Marine Protected Areas
			lyr = new L.TileLayer(
				//'http://cdn.mpatlas.org/tilecache/mpas/{z}/{x}/{y}.png',
				'http://mpatlas.s3.amazonaws.com/tilecache/mpas/{z}/{x}/{y}.png',
				{id: 6, maxZoom: 9, opacity: 0.5, scheme: 'tms'}
			);
			this.overlayLayers['Designated Marine Protected Areas'] = lyr;
			this.layers.push(lyr);
			
			// Candidate Marine Protected Areas
			lyr = new L.TileLayer(
				'http://cdn.mpatlas.org/tilecache/candidates/{z}/{x}/{y}.png',
				{id: 7, maxZoom: 9, opacity: 0.6, scheme: 'xyz'}
			);
			this.overlayLayers['Candidate Marine Protected Areas'] = lyr;
			this.layers.push(lyr);

            this.map = new L.Map(this.mapelem, {
				center: new L.LatLng(0, 0),
				zoom: 2,
				layers: this.layers,
				minZoom: 0,
				maxZoom: 12,
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
			var sel = $('#body_list_full');
			sel.fadeOut(600);
			// The code below is really hacky, clean up maptip api when we can
			//mpatlas.maptip.enableMapTip(); // Not needed, maphover events will bring it back automatically
			if (mpatlas.maptip.locked) {
			    mpatlas.maptip.disable = false;
			    mpatlas.maptip.showMapTip();
			}
		},
		
		switchToListView: function () {
			mpatlas.maptip.disableMapTip();
			$('#btnMapMode').removeClass('selected');
			$('#btnListMode').addClass('selected');

			var sel = $('#body_list_full');
			sel.fadeIn(600);

			$('.leaflet-control-container').hide();
			
			if (mpatlas.list) {
				var sz = {
					height: sel.height() - 44,
					width:  sel.width() - 200
				};
				mpatlas.list.setSize(sz);
				mpatlas.list.doLayout();
			}
			//$('#mpa-list-container').css('opacity', 0.8);
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
				var location = this.history.get('location', true);
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

			var explMode = this.history.get('exploreMode');
			this.setExploreMode((explMode) ? explMode : this.defaultMode);
		},
		
		layerAdded: function (e) {
			var lyr = e.layer;
		},
		
		layerRemoved: function (e) {
			var lyr = e.layer;
		},

        initExploreButtons: function() {
            var mpatlas = this;
            buttons = $('.explore_button');
            for (var i = 0; i < buttons.length; i++) {
                var button = buttons[i];
                var mode = button.id.replace('explore_', '');
                (function(button, mode) {
                    $(button).on('click', function(e) {
                        mpatlas.setExploreMode(mode);
                    });
                })(button, mode);
            }
        },
        
        setExploreMode: function(mode) {
            var mpatlas = this;
            if (mpatlas.currentMode !== mode) {
                mpatlas.currentMode = mode;
				mpatlas.history.set('exploreMode', mode);
                $('.explore_button.selected').removeClass('selected');
                $('#explore_' + mode).addClass('selected');
                mpatlas.maptip.disableMapTip();
                mpatlas.maptip.toggleEvents(true);
            }
        },

		initMapHover: function () {
            // Make map fire hover event after 500ms mouse pause, used by feature layer lookups
            this.initMapHoverEvents(500, 1);

            this.maptip = new MPAtlas.MapTip({
                el: $('#maptip')[0],
                mpatlas: this
            }); // setup maptip element and behavior

            this.registerMapHover(); // assign actions on mouse hover/pause and click for map layer feature lookup
            //this.maptip.toggleEvents(true); // activate the maptip event registration
            //this.maptip.hideMapTip();
            //this.maptip.disableMapTip();

            // give them an initial map tip with a hint
			//$('#maptip-content').html('Pause your mouse over the map<br/>to discover nearby MPAs');

		},
		
		saveMapLocation: function () {
			var loc = {
				center: mpatlas.map.getCenter(),
				zoom: mpatlas.map.getZoom()
			};
			mpatlas.history.set('location', loc, true);			
		},
		
		zoomToMPA: function (id) {
			
		},

        registerMapHover: function() {
            var mpatlas = this;
            var maptip = this.maptip;
            var handlers = {
                maphover: function(e, mapevent) {
					
					// stop if layer list is expanded because that means we are over the top of it
					var lyrContainer = $('.leaflet-control-layers-expanded');
					if (lyrContainer.length > 0) {
						return;
					}
					
					var url = null;
                    if (!maptip.locked) {

						var radius = mpatlas.getPixelRadius(2);
                        var ll = mapevent.latlng;
                        if (typeof $('#maptip-content').data('orightml') === 'undefined') {
                            $('#maptip-content').data('orightml', $('#maptip-content').html());
                        }
						//maptip.enableMapTip();
						$('html').addClass('busy'); // Add progress cursor when searching

                        switch (mpatlas.currentMode) {

                        case 'mpas':
	                        //$('#maptip-content').html('Searching for MPAs...');
							
							url = mpatlas.domain + '/mpa/lookup/point/?lon=' + ll.lng + '&lat=' + ll.lat + '&radius=' + radius;
							if (mpatlas.proxy && mpatlas.proxy !== '') {
								url = mpatlas.proxy + escape(url);
							}
                            $.ajax({
                                url: url,
                                success: function(data) {
                                    mpatlas.featuredata = data;
                                    var mpahtml = '';
                                    mpahtml += '<span style="font-weight:bold;">Click to explore these MPAs:</span>';
                                    for (var i = 0; i < data.mpas.length; i++) {
                                        mpa = data.mpas[i];
                                        mpahtml += '<a class="maptip_mpalink" href="' + mpa.url + '"><span style="float:right; margin-left:3px; font-style:italic;">(' + mpa.country + ')</span>' + mpa.name + '</a>';
                                    }
                                    if (data.mpas.length === 0) {
                                        //mpahtml = 'No MPAs at this location';
                                        mpahtml = '';
                                        $('html').removeClass('busy'); // Remove progress cursor when done searching
                                        maptip.disableMapTip();
										return;
                                    }
                                    $('#maptip-content').data('latlon', {
                                        lat: ll.lat,
                                        lon: ll.lon
                                    });
                                    $('html').removeClass('busy'); // Remove progress cursor when done searching
                                    $('#maptip-content').html(mpahtml);
                                    maptip.enableMapTip();
									maptip.offset = $('#leafletmap').offset();
                                },
                                error: function() {
                                    $('html').removeClass('busy'); // Add progress cursor when searching
                                }
                            });
                            break;

                        case 'eez':
                        case 'meow':
						case 'fao':
	                        //$('#maptip-content').html('Searching for Region...');

                            radius = 0.00000001;

							url = mpatlas.domain + '/region/' + mpatlas.currentMode + '/lookup/point/?lon=' + ll.lng + '&lat=' + ll.lat + '&radius=' + radius;
							if (mpatlas.proxy && mpatlas.proxy !== '') {
								url = mpatlas.proxy + escape(url);
							}
                                
							$.ajax({
								url: url,
                                success: function(data) {
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
                                            success: function(data) {
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
                                                geojson.on('click', function(mapevent) {
                                                    mpatlas.map.fireEvent('click', mapevent); // pass click from layer to map
                                                });
                                                mpatlas.map.addLayer(geojson);
                                                mpatlas.highlightlayer = geojson;
                                            }
                                        });
                                    } else {
                                        //mpahtml = 'No Region at this location';
                                        mpahtml = '';
                                        $('html').removeClass('busy'); // Remove progress cursor when done searching
                                        maptip.disableMapTip();
										return;
                                    }
                                    $('#maptip-content').data('latlon', {
                                        lat: ll.lat,
                                        lon: ll.lon
                                    });
                                    $('#maptip-content').html(mpahtml);
                                    $('html').removeClass('busy'); // Remove progress cursor when done searching
                                    maptip.enableMapTip();
                                }
                            });
                            break;
                        }
                    }
                },
                maphoverclear: function(e, mapevent) {
                    if (!maptip.locked) {
                        mpatlas.featuredata = {};
                        $('#maptip-content').html($('#maptip-content').data('orightml'));
                        if (mpatlas.highlightlayer) {
                            mpatlas.map.removeLayer(mpatlas.highlightlayer);
                        }
                        maptip.disableMapTip();
                    }
                },
                mapclick: function(mapevent) {
                    if (!maptip.locked) {
                        switch (mpatlas.currentMode) {
                        case 'mpas':
                            if (mpatlas.featuredata && mpatlas.featuredata.mpas && mpatlas.featuredata.mpas.length === 1) {
                                window.location = mpatlas.featuredata.mpas[0].url;
                            } else {
                                maptip.toggleEvents(false);
                            }
                            break;
                        case 'eez':
                        case 'meow':
						case 'fao':
                            if (mpatlas.featuredata && mpatlas.featuredata.regions && mpatlas.featuredata.regions.length >= 1) {
                                window.location = '/region/' + mpatlas.currentMode + '/' + mpatlas.featuredata.regions[0].id;
                            } else {
                                maptip.toggleEvents(false);
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

        initMapHoverEvents: function(delay, pixeltolerance) {
            var map = this.map,hovertimer, hovered = false, lastpoint = {
                x: -9999,
                y: -9999
            };
            delay = (delay) ? delay : 250;
			pixeltolerance = (pixeltolerance) ? pixeltolerance : 1;
			
            this.map.on('mousemove', function(e) {
                // this is a leaflet map MouseEvent, not a jquery event
                if (hovered && (Math.abs(e.layerPoint.x - lastpoint.x) > pixeltolerance || Math.abs(e.layerPoint.y - lastpoint.y) > pixeltolerance)) {
                    hovered = false;
                    $(map).trigger('maphoverclear', [e]);
                }
                clearTimeout(hovertimer);
                hovertimer = setTimeout(function() {
                    lastpoint = {
                        x: e.layerPoint.x,
                        y: e.layerPoint.y
                    };
                    hovered = true;
                    $(map).trigger('maphover', [e]);
                }, delay);
            });
            this.map.on('mouseout', function(e) {
                clearTimeout(hovertimer);
                hovered = false;
                $(map).trigger('maphoverclear', [e]);
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
			for (var i = 0; i < len; i++) {
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
				expires: 0.5 // 1/2 day or 12 hours
			});
			
		},
		
		set: function (key, value, encode) {
			if (encode) {
				value = JSON.stringify(value);
			}
			this.localStorage.set(key, value);			
		},
		
		get: function (key, decode) {
			var value = this.localStorage.get(key);
			if (decode) {
				value = JSON.parse(value);
			}
			return value;
		}
	});

    //MPAtlas.prototype.MapTip = Backbone.View.extend({
    MPAtlas.MapTip = Backbone.View.extend({
        // define maptip behaviors and initialize
        initialize: function(options) {
            var elem = options.el;
            var mpatlas = options.mpatlas;
            var maptip = this;
            this.elem = elem;
            this.mpatlas = mpatlas;
            //var popuppane = mpatlas.map.getPanes().popupPane;
            //$('#maptip').appendTo(popuppane);
            $(elem).appendTo(mpatlas.mapelem);
            this.timer = null;
            this.disable = true;
            this.offset = {
                left: 9000,
                top: 0
            };
            maptip.locked = true; // initial value needs to be true

            //var offsetX = event.pageX - offset.left;
            //var offsetY = event.pageY - offset.top;
            this.showMapTip = function(event) {
                maptip.hidden = false;
                if (!maptip.disable) {
                    $('#maptip').removeClass('nodisplay').removeClass('hidden').removeClass('transparent');
                    clearTimeout(maptip.timer);
                    maptip.offset = $('#leafletmap').offset();
                }
            };

            this.hideMapTip = function(event, immediate) {
                if (immediate) {
                    $('#maptip').addClass('nodisplay').addClass('hidden');
                } else {
                    maptip.timer = setTimeout(function() {
                        $('#maptip').addClass('hidden');
                    }, 500);
                }
                $('#maptip').addClass('transparent');
            };

            this.moveMapTip = function(event) {
                //var offset = $(event.delegateTarget).offset();
                //var offsetX = event.pageX - offset.left;
                //var offsetY = event.pageY - offset.top;
                //$('#maptip').css({'top': offsetY, 'left': offsetX});
                $('#maptip').css({
                    'top': event.pageY - maptip.offset.top,
                    'left': event.pageX - maptip.offset.left
                });
            };

            this.disableMapTip = function(e, immediatehide) {
                maptip.disable = true;
                maptip.hideMapTip(e, immediatehide); // true = hide immediate, false = fade out
            };

            this.enableMapTip = function(e) {
                maptip.disable = false;
                if (maptip.locked) {
                    maptip.toggleEvents(true); //  break locked maptip by renabling mouse events
                }
                //if (!maptip.hidden) {
                //}
                maptip.showMapTip(e);
            };

            mpatlas.map.on('movestart', maptip.disableMapTip);
            //mpatlas.map.on('moveend', maptip.enableMapTip);
            mpatlas.map.on('moveend', function() {
                maptip.toggleEvents(true);
            });
        },

        // make maptip responsive (or not responsive) to mouse and map events
        // effectively locks maptip on page
        toggleEvents: function(respond_to_events) {
            var maptip = this;
            if ($.type(respond_to_events) === 'undefined' || respond_to_events) {
                if (this.locked) {
                    console.log('toggleMapTipEvents');
				
                    // enable maptip events
                    // jquery custom events that prevents mouseover bubbling from child nodes
                    $(this.mpatlas.mapelem).on('mouseenter.maptip', this.showMapTip);
                    $(this.mpatlas.mapelem).on('mouseleave.maptip', this.hideMapTip);
                    $(window).on('mousemove.maptip', this.moveMapTip);

                    this.locked = false;
                }
            } else {
                //console.log('toggleMapTipEvents false');
				
                // disable maptip event tracking
                // jquery custom events that prevents mouseover bubbling from child nodes
                $(this.mpatlas.mapelem).off('mouseenter.maptip', this.showMapTip);
                $(this.mpatlas.mapelem).off('mouseleave.maptip', this.hideMapTip);
                $(window).off('mousemove.maptip', this.moveMapTip);

                //this.map.off('movestart', maptip.disableMapTip);
                //this.map.off('moveend', maptip.enableMapTip);

                this.locked = true;
            }
        }
    });


    return {
        MPAtlas: MPAtlas
    };
    // What we return here will be used by other modules
});