define([
  // These are path aliases configured in the requireJS bootstrap
  'backbone-module',
  'json2',
  'persist',
  'leaflet',
  'TileLayer.Bing'
],
function (Backbone) {  
    var MPAtlas = Backbone.View.extend({
		proxy: '',
		domain: 'http://' + document.domain + '/',
		//proxy: '/terraweave/features.ashx?url=', // handle cross-domain if necessary. used for testing
		//domain: 'http://mpatlas.org/',
		
		exploremodes: ['mpas', 'eez', 'meow', 'fao'],
		currentmode: 'mpas',			

        initialize: function(map) {

            if ($.type(map) === 'object') {
                this.mapelem = (map.length) ? map[0] : map;
            } else {
                this.mapelem = $('#' + map)[0]; // Assume it's an element id string
            }

            this.makeMap();
            window['leafmap'] = this.map;

            // resize body and contained map element
            // Depending on how the page/viewport container and the map body div are css styled,
            // this may or may not be necessary.
			//_.bindAll(this, 'resizeViewport'); // make sure this refers to this when fired by event
            //this.resizeViewport();
            //$(window).resize(this.resizeViewport);

            this.history = new MPAtlas.History();

            this.initExploreButtons();
			
			var location = this.history.get('location', true);
			if (location) {
				this.map.panTo(location);
			} else {
				this.map.locate();
			}
			
			var currMode = this.history.get('currentMode', true);
			if (currMode) {
				this.currentmode = currMode;
			}
			
			this.initMapHover(); // do the hover initialization last
			
        },

        // create Leaflet map
        makeMap: function() {

			var layers = [];
			this.bgMaps = {};
			this.overlayMaps = {};

			// Bing background layer for testing
			var lyr = new L.TileLayer.Bing(
				'ApQd0ymqxAh08w4k8U5VnEicyUqlQbcylqZcuI6hi8fV3nsW0MqwepRj-yBF2MeY', // this is my key - need one for Waitt
				'road',
				{maxZoom: 18, opacity: 1}
			)
			this.bgMaps['Bing Maps'] = lyr;

			// ESRI Oceans Layer
			var lyr = new L.TileLayer(
				'http://services.arcgisonline.com/ArcGIS/rest/services/Ocean_Basemap/MapServer/tile/{z}/{y}/{x}.png',
				{maxZoom: 9, opacity: 1}
			);
			this.bgMaps['Oceans'] = lyr;
			layers.push(lyr);
	
			// EEZs / Nations		
			lyr = new L.TileLayer(
				'http://cdn.mpatlas.org/tilecache/eezs/{z}/{x}/{y}.png',
				{maxZoom: 9, opacity: 0.4, scheme: 'tms'}
			);
			this.overlayMaps['Exclusive Economic Zones'] = lyr;
			layers.push(lyr);
			
			// Marine Eco-Regions
			lyr = new L.TileLayer(
				'http://cdn.mpatlas.org/tilecache/meow/{z}/{x}/{y}.png',
				{maxZoom: 9, opacity: 0.4, scheme: 'tms'}
			);
			this.overlayMaps['Marine Eco-Regions'] = lyr;
			
			// FAO Fishing Zones
			lyr = new L.TileLayer(
				'http://cdn.mpatlas.org/tilecache/fao/{z}/{x}/{y}.png',
				{maxZoom: 9, opacity: 0.4, scheme: 'tms'}
			);
			this.overlayMaps['FAO Fishing Zones'] = lyr;
			
			
			var group = new L.LayerGroup();
			
			// Designated Marine Protected Areas
			lyr = new L.TileLayer(
				'http://cdn.mpatlas.org/tilecache/mpas/{z}/{x}/{y}.png',
				{maxZoom: 9, opacity: 0.7, scheme: 'xyz'}
			);
			this.overlayMaps['Designated Marine Protected Areas'] = lyr;
			group.addLayer(lyr);
			
			// Candidate Marine Protected Areas
			lyr = new L.TileLayer(
				'http://cdn.mpatlas.org/tilecache/candidates/{z}/{x}/{y}.png',
				{maxZoom: 9, opacity: 0.7, scheme: 'xyz'}
			);
			this.overlayMaps['Candidate Marine Protected Areas'] = lyr;
			group.addLayer(lyr);

			layers.push(group);

            this.map = new L.Map(this.mapelem, {
				center: new L.LatLng(0, 0),
				zoom: 2,
				layers: layers,
				minZoom: 0,
				maxZoom: 12,
				attributionControl:false
			});
			
            var map = this.map; // use this var for closures inside event handlers

			// override the position of layer control			
			L.Control.Layers.prototype.getPosition = function () {
				return L.Control.Position.BOTTOM_LEFT;
			}
			
			this.layersControl = new L.Control.Layers(
				this.bgMaps,
				this.overlayMaps,
				{
					collapsed: !L.Browser.touch
				}
			);
			this.map.addControl(this.layersControl);
			
			this.map.on('locationfound', function(location) {
				mpatlas.map.panTo(location.latlng);
			});

			this.map.on('viewreset', function(location) {
				mpatlas.saveLocation(location);
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

        initExploreButtons: function() {
            var mpatlas = this;
            buttons = $('.explore_button');
            for (var i = 0; i < buttons.length; i++) {
                var button = buttons[i];
                var mode = button.id.replace('explore_', '');
                (function(button, mode) {
                    $(button).on('click', function(e) {
                        if (mpatlas.currentmode != mode) {
                            mpatlas.currentmode = mode;
                            $('.explore_button.selected').removeClass('selected');
                            $(button).addClass('selected');
                            mpatlas.maptip.toggleEvents(true);
                            mpatlas.maptip.hideMapTip();
                        }
                    });
                })(button, mode);
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
            this.maptip.toggleEvents(true); // activate the maptip event registration

            // give them an initial map tip with a hint
			$('#maptip-content').html('Pause your mouse over the map<br/>to discover MPAs in that area.');

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
						maptip.enableMapTip();

                        switch (mpatlas.currentmode) {

                        case 'mpas':
	                        $('#maptip-content').html('Searching for MPAs...');
							
							url = mpatlas.domain + 'mpa/lookup/point/?lon=' + ll.lng + '&lat=' + ll.lat + '&radius=' + radius;
							if (mpatlas.proxy && mpatlas.proxy !== '') {
								url = mpatlas.proxy + escape(url);
							}
                            $.ajax({
                                url: url,
                                success: function(data) {
                                    mpatlas.featuredata = data;
                                    var mpahtml = '';
                                    mpahtml += '<span style="font-weight:bold;">Click to explore these MPAs:</span>'
                                    for (var i = 0; i < data.mpas.length; i++) {
                                        mpa = data.mpas[i];
                                        mpahtml += '<a class="maptip_mpalink" href="' + mpa.url + '"><span style="float:right; margin-left:3px; font-style:italic;">(' + mpa.country + ')</span>' + mpa.name + '</a>';
                                    }
                                    if (data.mpas.length == 0) {
                                        mpahtml = 'No MPAs at this location';
                                        //mpahtml = '';
                                        //maptip.disableMapTip();
										//return;
                                    }
                                    $('#maptip-content').data('latlon', {
                                        lat: ll.lat,
                                        lon: ll.lon
                                    });
                                    $('#maptip-content').html(mpahtml);
									maptip.offset = $('#leafletmap').offset();
                                }
                            });
                            break;

                        case 'eez':
                        case 'meow':
						case 'fao':
	                        $('#maptip-content').html('Searching for Region...');

                            radius = 0.00000001;

							url = mpatlas.domain + 'region/' + mpatlas.currentmode + '/lookup/point/?lon=' + ll.lng + '&lat=' + ll.lat + '&radius=' + radius;
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
                                        mpahtml += '<a class="maptip_mpalink" href="/region/' + mpatlas.currentmode + '/' + region.id + '"><span style="float:right; margin-left:3px; font-style:italic;">(' + region.country + ')</span>' + region.name + '</a>';
                                        mpahtml += '<span style="font-size:11px;">Total Marine Area: <strong>' + region.area_km2 + ' km2</strong>';
                                        mpahtml += '<br /># of MPAs: <strong>' + region.mpas + '</strong>';
                                        mpahtml += '<br />Total Marine Area in MPAs: <strong>' + region.percent_in_mpas + '%</strong>';
                                        mpahtml += '<br />Total Marine Area No Take: <strong>' + region.percent_no_take + '%</strong></span>';

                                        // Load feature from GeoJSON
										url = mpatlas.domain + 'region/' + mpatlas.currentmode + '/' + region.id + '/features/';
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
                                        mpahtml = 'No Region at this location';
                                        //mpahtml = '';
                                        //maptip.disableMapTip();
										//return;
                                    }
                                    $('#maptip-content').data('latlon', {
                                        lat: ll.lat,
                                        lon: ll.lon
                                    });
                                    $('#maptip-content').html(mpahtml);
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
                        switch (mpatlas.currentmode) {
                        case 'mpas':
                            if (mpatlas.featuredata && mpatlas.featuredata.mpas && mpatlas.featuredata.mpas.length == 1) {
                                window.location = mpatlas.featuredata.mpas[0].url;
                            } else {
                                maptip.toggleEvents(false);
                            }
                            break;
                        case 'eez':
                        case 'meow':
						case 'fao':
                            if (mpatlas.featuredata && mpatlas.featuredata.regions && mpatlas.featuredata.regions.length >= 1) {
                                window.location = '/region/' + mpatlas.currentmode + '/' + mpatlas.featuredata.regions[0].id;
                            } else {
                                maptip.toggleEvents(false);
                            }
                            break;
                        }
                    } else {
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
		},
		
		saveLocation: function (location) {
			this.history.set('location', location, true)
		}
    });

	MPAtlas.History = Backbone.View.extend({
		initialize: function (options) {
			this.localStorage = new Persist.Store('MPAtlas', {
				about: 'Local Store for MPAtlas',
				expires: 30
			});
			
		},
		
		set: function (key, value, encode) {
			return;
			if (encode) {
				value = JSON.stringify(value);
			}
			this.localStorage.set(key, value);			
		},
		
		get: function (key, decode) {
			return '';
			var value = this.localStorage.get(key);
			if (decode) {
				value = JSON.parse(value);
			}
			return value;
		}
	})

    //MPAtlas.prototype.MapTip2 = Backbone.View.extend({
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
                left: 0,
                top: 0
            };
            maptip.locked = false;

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

            this.hideMapTip = function(event, fake, immediate) {
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

            this.disableMapTip = function(e) {
                maptip.disable = true;
                maptip.hideMapTip(e, false); // true = hide immediate, false = fade out
            };

            this.enableMapTip = function(e) {
                maptip.disable = false;
                if (maptip.locked) {
                    maptip.toggleEvents(true); //  break locked maptip by renabling mouse events
                }
                //if (!maptip.hidden) {
                    maptip.showMapTip(e);
                //}
            };

            mpatlas.map.on('movestart', maptip.disableMapTip);
            mpatlas.map.on('moveend', maptip.enableMapTip);

            //mpatlas.toggleEvents(true);
        },

        // make maptip responsive (or not responsive) to mouse and map events
        // effectively locks maptip on page
        toggleEvents: function(respond_to_events) {
            var maptip = this;
            if ($.type(respond_to_events) === 'undefined' || respond_to_events) {
                //console.log('toggleMapTipEvents');
				
                // enable maptip events
                // jquery custom events that prevents mouseover bubbling from child nodes
                $(this.mpatlas.mapelem).on('mouseenter.maptip', this.showMapTip);
                $(this.mpatlas.mapelem).on('mouseleave.maptip', this.hideMapTip);
                $(window).on('mousemove.maptip', this.moveMapTip);

                this.locked = false;
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