define([
  // These are path aliases configured in the requireJS bootstrap
  'backbone-module'
], function(Backbone){
    // Above we have passed in jQuery, Underscore and Backbone
      
    var MPAtlas = Backbone.View.extend({
        initialize: function(map) {
            var mpatlas = this;
            this.domain = '//www.mpatlas.org';
            this.cdn =  '.';
            if ($.type(map) === 'object') {
                this.mapelem = (map.length) ? map[0] : map;
            } else {
                this.mapelem = $('#' + map)[0]; // Assume it's an element id string
            }

            this.exploremodes = ['mpas', 'eezs', 'ecoregions', 'custom'];
            this.currentmode = 'mpas';

            this.layers = [
            {
                id: 'mpas',
                  name: 'Designated MPAs',
                  style: {
                      outline: '',
                      fill: ''
                  },
                  url: 'http://cdn.mpatlas.org/tilecache/mpas/{z}/{x}/{y}.png',
                  scheme: 'tms'
            },
              {
                  id: 'candidatempas',
                  name: 'Candidate MPAs',
                  style: {
                      outline: '',
                      fill: ''
                  },
                  url: 'http://cdn.mpatlas.org/tilecache/candidates/{z}/{x}/{y}.png',
                  scheme: 'tms'
              },
              {
                  id: 'eezs',
                  name: 'Exclusive Economic Zones',
                  style: {
                      outline: '',
                      fill: ''
                  },
                  url: 'http://cdn.mpatlas.org/tilecache/eezs/{z}/{x}/{y}.png',
                  scheme: 'tms'
              }
            ];

            this.activelayer = 'mpas';

            this.makeMap();
            window['leafmap'] = this.map;

            // resize body and contained map element
            _.bindAll(this, 'resizeViewport'); // make sure this refers to this when fired by event
            this.resizeViewport();
            $(window).resize(this.resizeViewport);

            this.initMapHoverEvents(250, 1); // map now fires hover event after 500ms mouse pause

            this.maptip = new MPAtlas.MapTip({el: $('#maptip')[0], mpatlas: this}); // setup maptip element and behavior

            this.registerMapHover(); // assign actions on mouse hover and click for map layer feature lookup
            this.maptip.toggleEvents(true); // activate the maptip

            this.initLayerSlider();
            
            this.initExploreButtons();
        },

          resizeViewport: function() {
              return false;
              $('#body_full').height($(window).height() - $('#header_full').height() - $('#footer_full').height());
              this.map.invalidateSize();
          },
          
          initExploreButtons: function() {
              var mpatlas = this;
              buttons = $('.explore_button');
              for (var i=0; i<buttons.length; i++) {
                  var button = buttons[i];
                  var mode = button.id.replace('explore_', '');
                  (function(button, mode) {
                      $(button).on('click', function(e) {
                            mpatlas.currentmode = mode;
                            $('.explore_button.selected').removeClass('selected');
                            $(button).addClass('selected');
                        });
                  })(button, mode);
              }
          },

          // create Leaflet map
          makeMap: function() {
              this.map = new L.Map(this.mapelem);
              var map = this.map; // use this var for closures inside event handlers

              whitepng = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAQAAAAEACAYAAABccqhmAAADGUlEQVR4nO3UMQEAAAiAMPuX1hgebAm4mAWy5jsA+GMAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEGYAEHbmUDvFpM58qAAAAABJRU5ErkJggg==';
              esriblanktile = 'http://services.arcgisonline.com/ArcGIS/rest/services/Ocean_Basemap/MapServer/tile/13/4919/7472.png';

          	var whiteTileBg = new L.TileLayer(whitepng, {maxZoom: 18});
          	//leafmap.addLayer(whiteTileBg);
              var esriOceanUrl = 'http://services.arcgisonline.com/ArcGIS/rest/services/Ocean_Basemap/MapServer/tile/{z}/{y}/{x}.png',
          		esriOceanAttribution = 'ESRI Ocean Baselayer',
          		esriOcean = new L.TileLayer(esriOceanUrl, {maxZoom: 18, opacity: 1, attribution: esriOceanAttribution});
          	map.setView(new L.LatLng(0, 0), 2).addLayer(esriOcean);

          	var mpa_tiles_url = 'http://cdn.mpatlas.org/tilecache/mpas/{z}/{x}/{y}.png',
          		mpa_tiles = new L.TileLayer(mpa_tiles_url, {maxZoom: 18, opacity: 0.7, scheme: 'tms'});
          	map.addLayer(mpa_tiles);

          	var proposed_tiles_url = 'http://cdn.mpatlas.org/tilecache/candidates/{z}/{x}/{y}.png',
          		proposed_tiles = new L.TileLayer(proposed_tiles_url, {maxZoom: 18, opacity: 0.8, scheme: 'tms'});
          	map.addLayer(proposed_tiles);

          	var eez_tiles_url = 'http://cdn.mpatlas.org/tilecache/eezs/{z}/{x}/{y}.png',
          		eez_tiles = new L.TileLayer(eez_tiles_url, {maxZoom: 18, opacity: 0.25, scheme: 'tms'});
          	map.addLayer(eez_tiles);

          	//var markerLocation = new L.LatLng(51.5, -0.09),
          	//    markerLocation2 = new L.LatLng(markerLocation.lat, markerLocation.lng + 360, true),
          	//    markerLocation3 = new L.LatLng(markerLocation.lat, markerLocation.lng - 360, true),
          	//	marker = new L.Marker(markerLocation),
          	//	marker2 = new L.Marker(markerLocation2),
          	//	marker3 = new L.Marker(markerLocation3);;
          	//map.addLayer(marker);
          	//map.addLayer(marker2);
          	//map.addLayer(marker3);
          	//marker.bindPopup("<b>Hello world!</b><br />I am a popup.");
          	//marker2.bindPopup("<b>Hello world!</b><br />I am a second popup +360.");
          	//marker3.bindPopup("<b>Hello world!</b><br />I am a third popup -360.");
          },

          registerMapHover: function() {
              var mpatlas = this;
              var maptip = this.maptip;
              var handlers = {
                  maphover: function(e, mapevent) {
                      if (!maptip.locked) {
                    var radius = mpatlas.getPixelRadius(2);
                  		var ll = mapevent.latlng;
                  		if (typeof $('#maptip-content').data('orightml') === 'undefined') {
                              $('#maptip-content').data('orightml', $('#maptip-content').html());
                          }
                          $('#maptip-content').html('Searching for MPAs...');
                        switch (mpatlas.currentmode) {
                            case 'mpas':
                                $.ajax({
                                      url: '/mpa/lookup/point/?lon=' + ll.lng + '&lat=' + ll.lat + '&radius=' + radius,
                                      success: function(data) {
                                          mpatlas.featuredata = data;
                                          var mpahtml = '';
                                          mpahtml += '<span style="font-weight:bold;">Click to explore these MPAs:</span>'
                                          for (var i=0; i < data.mpas.length; i++) {
                                              mpa = data.mpas[i];
                                              mpahtml += '<a class="maptip_mpalink" href="' + mpa.url + '"><span style="float:right; margin-left:3px; font-style:italic;">(' + mpa.country + ')</span>' + mpa.name + '</a>';
                                          }
                                          if (data.mpas.length == 0) {
                                              mpahtml = 'No MPAs at this location';
                                          }
                                          $('#maptip-content').data('latlon', {lat: ll.lat, lon: ll.lon});
                                          $('#maptip-content').html(mpahtml);
                                      }
                                  });
                                break;
                            case 'eezs':
                                radius = 0.00000001
                                $.ajax({
                                      url: '/region/eez/lookup/point/?lon=' + ll.lng + '&lat=' + ll.lat + '&radius=' + radius,
                                      success: function(data) {
                                          mpatlas.featuredata = data;
                                          var mpahtml = '';
                                          mpahtml += '<span style="font-weight:bold;">Click to explore this nation:</span>'
                                          for (var i=0; i < data.regions.length; i++) {
                                              region = data.regions[i];
                                              mpahtml += '<a class="maptip_mpalink" href="/region/eez/' + region.id + '"><span style="float:right; margin-left:3px; font-style:italic;">(' + region.country + ')</span>' + region.name + '</a>';
                                          }
                                          if (data.regions.length == 0) {
                                              mpahtml = 'No MPAs at this location';
                                          }
                                          $('#maptip-content').data('latlon', {lat: ll.lat, lon: ll.lon});
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
                      }
                  },
                  mapclick: function(mapevent) {
                        if (!maptip.locked) {
                            if (mpatlas.featuredata && mpatlas.featuredata.mpas && mpatlas.featuredata.mpas.length == 1) {
                                window.location = mpatlas.featuredata.mpas[0].url;
                            } else {
                                maptip.toggleEvents(false);
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
              var map = this.map,
                  delay = (delay) ? delay : 250,
                  pixeltolerance = (pixeltolerance) ? pixeltolerance : 1,
                  hovertimer,
                  hovered = false,
                  lastpoint = {x: -9999, y: -9999};
              this.map.on('mousemove', function(e) {
                  // this is a leaflet map MouseEvent, not a jquery event
                  if (hovered && (Math.abs(e.layerPoint.x - lastpoint.x) > pixeltolerance || Math.abs(e.layerPoint.y - lastpoint.y) > pixeltolerance)) {
                      hovered = false;
                      $(map).trigger('maphoverclear', [e]);
                  }
                  clearTimeout(hovertimer);
                  hovertimer = setTimeout(function() {
                      lastpoint = {x: e.layerPoint.x, y: e.layerPoint.y};
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

          initLayerSlider: function() {
              var layershidden = false;
              var hideLayers = function(e) {
                  layershidden = true;
                  $('#layers_overlay').animate({
                      left: 0 - $('#layers_overlay').width()
                    }, 'slow', function() {
                      // Animation complete
                      //$('#layers_overlay').css({left: null, right: '100%'});
                      $('.layershider').html('M A P &nbsp;&nbsp; L A Y E R S');
                  });
              };
              var showLayers = function(e) {
                  layershidden = false;
                  //$('#layers_overlay').css({left: 0 - $('#layers_overlay').width(), right: null, width: 'auto'});
                  $('#layers_overlay').animate({
                      left: 0
                    }, 'slow', function() {
                      // Animation complete
                  });
                  $('.layershider').html('H I D E');
              };

              $('.layershider').on('click', function(e) {
                  if (layershidden) {
                      showLayers(e);
                  } else {
                      hideLayers(e);
                  }
              });
          }
    });
    
    
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
      	this.offset = {left: 0, top: 0};
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
          	    maptip.timer = setTimeout(function () {
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
              $('#maptip').css({'top': event.pageY - maptip.offset.top, 'left': event.pageX - maptip.offset.left});
      	};

      	this.disableMapTip = function(e) {
      	    maptip.disable = true;
              maptip.hideMapTip(e, false); // true = hide immediate, false = fade out
              console.log('disablemaptip');
      	};

      	this.enableMapTip = function(e) {
              maptip.disable = false;
              if (maptip.locked) {
                  maptip.toggleEvents(true); //  break locked maptip by renabling mouse events
              }
              if (!maptip.hidden) {
                  maptip.showMapTip(e);
              }
              console.log('enablemaptip');
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
              console.log('toggleMapTipEvents');
              // enable maptip events
              // jquery custom events that prevents mouseover bubbling from child nodes
              //$(this.mapelem).on('mouseenter.maptiptrack', function(e) {
              //    maptip.hidden = false;
              //});
              //$(this.mapelem).on('mouseleave.maptiptrack', function(e) {
              //    maptip.hidden = true;
              //});
          	$(this.mpatlas.mapelem).on('mouseenter.maptip', this.showMapTip);
          	$(this.mpatlas.mapelem).on('mouseleave.maptip', this.hideMapTip);
          	$(window).on('mousemove.maptip', this.moveMapTip);

              this.locked = false;
          } else {
              console.log('toggleMapTipEvents false');
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
