MPAtlas = function(map) {
    this.initialize(map);
};

$.extend(MPAtlas.prototype, {
    
    // constructor
    initialize: function(map) {
        var mpatlas = this;
        this.domain = '//www.mpatlas.org';
        this.cdn =  '.';
        if ($.type(map) === 'object') {
            this.mapelem = (map.length) ? map[0] : map;
        } else {
            this.mapelem = $('#' + map)[0]; // Assume it's an element id string
        }

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
        this.resizeViewport();
        $(window).resize(this.resizeViewport);

        this.initMapHover(250, 1); // map now fires hover event after 500ms mouse pause
        this.initMapTip(); // setup maptip element and behavior

        this.registerMapHover();

        this.initLayerSlider();
    },
    
    resizeViewport: function() {
        $('#body_full').height($(window).height() - $('#header_full').height() - $('#footer_full').height());
        this.map.invalidateSize();
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
    
    // define maptip behaviors and initialize
    initMapTip: function() {
        //var popuppane = this.map.getPanes().popupPane;
    	//$('#maptip').appendTo(popuppane);
    	var mpatlas = this;
    	this.maptip = $('#maptip')[0];
    	var maptip = this.maptip
    	$('#maptip').appendTo(this.mapelem);
    	var maptiptimer = maptip.maptiptimer;
    	var maptipdisable = maptip.maptipdisable = true;
    	var maptipoffset = maptip.maptipoffset = {left: 0, top: 0};
    	maptip.locked = false;
        //var offsetX = event.pageX - offset.left;
        //var offsetY = event.pageY - offset.top;
    	maptip.showMapTip = function(event) {
                maptip.hidden = false;
    	    if (!maptipdisable) {
    	        $('#maptip').removeClass('nodisplay').removeClass('hidden').removeClass('transparent');
    	        clearTimeout(maptiptimer);
    	        maptipoffset = $('#leafletmap').offset();
            }
    	};
    	maptip.hideMapTip = function(event, fake, immediate) {
            if (immediate) {
                $('#maptip').addClass('nodisplay').addClass('hidden');
            } else {
        	    maptiptimer = setTimeout(function () {
                    $('#maptip').addClass('hidden');
                }, 500);
            }
            $('#maptip').addClass('transparent');
    	};
    	maptip.moveMapTip = function(event) {
            //var offset = $(event.delegateTarget).offset();
            //var offsetX = event.pageX - offset.left;
            //var offsetY = event.pageY - offset.top;
            //$('#maptip').css({'top': offsetY, 'left': offsetX});
            $('#maptip').css({'top': event.pageY - maptipoffset.top, 'left': event.pageX - maptipoffset.left});
    	};
    	var disableMapTip = this.maptip.disableMapTip = function(e) {
    	    maptipdisable = true;
            maptip.hideMapTip(e, false); // true = hide immediate, false = fade out
            console.log('disablemaptip');
    	};
    	var enableMapTip = this.maptip.enableMapTip = function(e) {
            maptipdisable = false;
            if (maptip.locked) {
                mpatlas.toggleMapTipEvents(true); //  break locked maptip by renabling mouse events
            }
            if (!maptip.hidden) {
                maptip.showMapTip(e);
            }
            console.log('enablemaptip');
        };

        this.map.on('movestart', maptip.disableMapTip);
        this.map.on('moveend', maptip.enableMapTip);

    	this.toggleMapTipEvents(true);
    },
    
    toggleMapTipEvents: function(respond_to_events) {
        var maptip = this.maptip;
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
        	$(this.mapelem).on('mouseenter.maptip', maptip.showMapTip);
        	$(this.mapelem).on('mouseleave.maptip', maptip.hideMapTip);
        	$(window).on('mousemove.maptip', maptip.moveMapTip);
    	
            maptip.locked = false;
        } else {
            console.log('toggleMapTipEvents false');
            // disable maptip event tracking
            // jquery custom events that prevents mouseover bubbling from child nodes
        	$(this.mapelem).off('mouseenter.maptip', maptip.showMapTip);
        	$(this.mapelem).off('mouseleave.maptip', maptip.hideMapTip);
        	$(window).off('mousemove.maptip', maptip.moveMapTip);

        	//this.map.off('movestart', maptip.disableMapTip);
            //this.map.off('moveend', maptip.enableMapTip);
        
            maptip.locked = true;
        }
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
            		$.ajax({
                        url: '/mpa/lookup/point/?lon=' + ll.lng + '&lat=' + ll.lat + '&radius=' + radius,
                        success: function(data) {
                            var mpahtml = '';
                            for (var i=0; i < data.mpas.length; i++) {
                                mpa = data.mpas[i];
                                mpahtml += mpa.name + ' (' + mpa.country + ')<br />';
                            }
                            if (data.mpas.length == 0) {
                                mpahtml = 'No MPAs at this location';
                            }
                            $('#maptip-content').data('latlon', {lat: ll.lat, lon: ll.lon});
                            $('#maptip-content').html(mpahtml);
                        }
                    });
                }
            },
            maphoverclear: function(e, mapevent) {
                if (!maptip.locked) {
                    $('#maptip-content').html($('#maptip-content').data('orightml'));
                }
            }
        };
        $(this.map).on('maphover', handlers.maphover);
        $(this.map).on('maphoverclear', handlers.maphoverclear);
        this.map.on('click', function(e) {
            mpatlas.toggleMapTipEvents(false);
        });
    },
    
    initMapHover: function(delay, pixeltolerance) {
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

