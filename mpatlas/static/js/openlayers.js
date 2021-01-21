$(function() {
    OpenLayers.Util.onImageLoadErrorColor = "transparent";

    map = new OpenLayers.Map('mainmap', { 
        //maxExtent: baseLayer.maxExtent,
        //units: baseLayer.units,
        //resolutions: baseLayer.resolutions,
        //numZoomLevels: baseLayer.numZoomLevels,
        //tileSize: baseLayer.tileSize,
        //displayProjection: baseLayer.displayProjection

        maxExtent: new OpenLayers.Bounds(-20037508.342787,-20037508.342787,20037508.342787,20037508.342787),
        numZoomLevels: 18,
        maxResolution: 156543.0339,
        units: 'm',
        projection: new OpenLayers.Projection("EPSG:3857"),
        displayProjection: new OpenLayers.Projection("EPSG:4326"),
        controls: [
    		new OpenLayers.Control.ArgParser(),
    		new OpenLayers.Control.Navigation(),
    		new OpenLayers.Control.TouchNavigation(),
    		new OpenLayers.Control.PinchZoom(),
    		new OpenLayers.Control.ZoomPanel()
        ],
    });

    function getEsriOceanURL(bounds) {
        var res = this.map.getResolution();
        var x = Math.round ((bounds.left - this.maxExtent.left) / (res * this.tileSize.w));
        var y = Math.round ((this.maxExtent.top - bounds.top) / (res * this.tileSize.h));
        //var y = Math.round ((bounds.bottom - this.maxExtent.bottom) / (res * this.tileSize.h));
        var z = this.map.getZoom();

        // wrap the dateline
        var limit = Math.pow(2, z);
        if (this.wrapDateLine) {
           x = ((x % limit) + limit) % limit;
        }

        // stop at upper and lower tile to prevent missing tile images
        if (y < 0 || y >= (this.maxExtent.top - this.maxExtent.bottom) / (res * this.tileSize.h) ) {
            return null;
        }

        var path = z + "/" + y + "/" + x + "." + this.type; 
        var url = this.url;
        if (url instanceof Array) {
            url = this.selectUrl(path, url);
        }
        return url + '/tile/' + path;
    }

    var esriocean = new OpenLayers.Layer.XYZ(
        "ESRI Ocean Layer",
        "https://services.arcgisonline.com/ArcGIS/rest/services/Ocean_Basemap/MapServer",
        {
            type: 'png',
            getURL: getEsriOceanURL,
            wrapDateLine: true,
            isBaseLayer: true,
            transparent: true,
            opacity: 1,
            transitionEffect: 'resize',
            wrapDateLine: true,
            sphericalMercator: true,
            displayOutsideMaxExtent: false
        }
    );
    map.addLayers([esriocean]);

    function get_mpa_url(bounds) {
        var res = this.map.getResolution();
        var x = Math.round ((bounds.left - this.maxExtent.left) / (res * this.tileSize.w));
        //var y = Math.round ((this.maxExtent.top - bounds.top) / (res * this.tileSize.h));
        var y = Math.round ((bounds.bottom - this.maxExtent.bottom) / (res * this.tileSize.h));
        var z = this.map.getZoom();

        var limit = Math.pow(2, z);
        if (this.wrapDateLine) {
           x = ((x % limit) + limit) % limit;
        }

        var path = z + "/" + x + "/" + y + "." + this.type; 
        var url = this.url;
        if (url instanceof Array) {
            url = this.selectUrl(path, url);
        }
        return url + path;
    }

    var mpas = new OpenLayers.Layer.XYZ(
        "Existing MPAs",
        "https://cdn.mpatlas.org/tilecache/mpas/",
        {
            type: 'png',
            getURL: get_mpa_url,
            wrapDateLine: true,
            isBaseLayer: false,
            transparent: true,
            opacity: 0.8,
            transitionEffect: 'resize',
            wrapDateLine: true,
            sphericalMercator: true,
        }
    );
    var proposed = new OpenLayers.Layer.XYZ(
        "Proposed MPAs",
        "https://cdn.mpatlas.org/tilecache/candidates/",
        {
            type: 'png',
            getURL: get_mpa_url,
            isBaseLayer: false,
            transparent: true,
            opacity: 0.8,
            transitionEffect: 'resize',
            wrapDateLine: true,
            sphericalMercator: true,
        }
    );
    var eezs = new OpenLayers.Layer.XYZ(
        'Exclusive Economic Zones (EEZs)',
    	"https://cdn.mpatlas.org/tilecache/eezs/",
		{
			type: 'png',
			getURL: get_mpa_url,
			isBaseLayer: false,
			transparent: true,
			opacity: 0.3,
			transitionEffect: 'resize',
			wrapDateLine: true,
			//visibility: false,
			displayInLayerSwitcher: true,
			displayOutsideMaxExtent: true,
			options: {
				color:  '#00CC99'
			}
		}
	);

    var osm = new OpenLayers.Layer.OSM();
    osm.isBaseLayer = true;
    map.addLayers([osm]);

    /*var gphy = new OpenLayers.Layer.Google(
        "Google Physical",
        {
            type: google.maps.MapTypeId.TERRAIN,
            opacity: 0.9,
            transitionEffect: 'resize'
        }
    );
    map.addLayers([gphy]);*/

    map.addLayers([proposed, mpas, eezs]);

    //map.addControl(new OpenLayers.Control.ZoomPanel());
    //map.addControl(new OpenLayers.Control.LayerSwitcher());
    //map.addControl(new OpenLayers.Control.MousePosition() );            
    //map.zoomToExtent(new OpenLayers.Bounds(-8341644, 4711236, -8339198, 4712459));
    //map.zoomToExtent(new OpenLayers.Bounds(-8725663.6225564, 4683718.6735907, -8099491.4868444, 4996804.7414467));

    map.setCenter(new OpenLayers.LonLat(0, 0).transform(
        new OpenLayers.Projection("EPSG:4326"),
        map.getProjectionObject()
    ), 1);


    var highlight = new OpenLayers.Layer.Vector("Highlight Layer");
    map.addLayers([highlight]);
    var eez_url = "/region/eez/2/features/?webmercator=true";
    var eez_geojson = 'xxx';
    //var geojson = new OpenLayers.Format.GeoJSON({
    //    'internalProjection': map.baseLayer.projection,
    //    'externalProjection': map.baseLayer.projection
    //});
    OpenLayers.loadURL(eez_url, {}, null, function (response) {
        var gformat = new OpenLayers.Format.GeoJSON({
            'internalProjection': map.baseLayer.projection,
            'externalProjection': map.baseLayer.projection
        });
        var features = gformat.read(response.responseText);
        var bounds;
        if(features) {
            if(features.constructor != Array) {
                features = [features];
            }
            for(var i=0; i < features.length; ++i) {
                //if (!bounds) {
                //    bounds = features[i].geometry.getBounds();
                //} else {
                //    bounds.extend(features[i].geometry.getBounds());
                //}
            }
            highlight.addFeatures(features);
            //map.zoomToExtent(bounds);
        }
    });
    //var eezfeature = geojson.read(eez_geojson);
    //highlight.addFeatures(eezfeatures);


    var getPixelRadius = function(pxradius) {
        // Convert pixel radius to map units (web mercator, meters) then to km.
        // pxradius can be a floating point value
		return (map.resolution * pxradius) / 1000;
    };

    OpenLayers.Control.Hover = OpenLayers.Class(OpenLayers.Control, {                
    	defaultHandlerOptions: {
    		'delay': 250,
    		'pixelTolerance': 3,
    		'stopMove': false
    	},

    	initialize: function(options) {
    		this.handlerOptions = OpenLayers.Util.extend(
    			{}, this.defaultHandlerOptions
    		);
    		OpenLayers.Control.prototype.initialize.apply(
    			this, arguments
    		); 
    		this.handler = new OpenLayers.Handler.Hover(
    			this,
    			{'pause': this.onPause, 'move': this.onMove},
    			this.handlerOptions
    		);
    	}, 

    	onPause: function(e) {
    	    /*
    		var m = MPAtlas;
    		if (m.request) {
    			Ext.Ajax.abort(m.request);
    			m.request = null;
    		}
    		if (m.ui.popUp) {
    			if (m.ui.popUp.closeOnMove) {
    				m.ui.popUp.hide();
    			} else {
    				return;
    			}
    		}		

    		var pt = m.map.getLonLatFromViewPortPx(e.xy);
    		switch (m.activeLayer) {
    			default:
    				m.eezs.getDetails({point: pt, isClick: false});
    				//m.mpas.getDetails({point: pt, isClick: false});
    		}
    		*/
    		console.log('hover');
    		var radius = getPixelRadius(1.5);
    		var pt = map.getLonLatFromViewPortPx(e.xy);
    		var ll = pt.clone();
            ll.transform(map.projection, map.displayProjection);
    		$.ajax({
                url: '/mpa/lookup/point/?lon=' + ll.lon + '&lat=' + ll.lat,
                success: function(data) {
                    var mpahtml = '';
                    for (var i=0; i < data.mpas.length; i++) {
                        mpa = data.mpas[i];
                        mpahtml += mpa.name + ' (' + mpa.country + ')<br />';
                    }
                    if (data.mpas.length == 0) {
                        mpahtml = 'No MPAs at this location';
                    }
                    if (typeof $('#maptip-content').data('orightml') === 'undefined') {
                        $('#maptip-content').data('orightml', $('#maptip-content').html());
                    }
                    $('#maptip-content').data('latlon', {lat: ll.lat, lon: ll.lon});
                    $('#maptip-content').html(mpahtml);
                }
            });
    	},

    	onMove: function(e) {
    	    /*
    		var m = MPAtlas;
    		m.vectors.removeAllFeatures();
    		if (m.request) {
    			Ext.Ajax.abort(m.request);
    			m.request = null;
    		}
    		if (m.ui.popUp && m.ui.popUp.closeOnMove) {
    			m.ui.popUp.hide();
    		}		

    		switch (m.activeLayer) {
    			default:  // mpas
    				m.mpas.selected = null;
    				m.mpas.selectedCount = 0;
    		}
    		*/
    		$('#maptip-content').html($('#maptip-content').data('orightml'));
    	}
    });

    OpenLayers.Control.Click = OpenLayers.Class(OpenLayers.Control, {                
    	defaultHandlerOptions: {
    		'single': true,
    		'double': false,
    		'pixelTolerance': 3,
    		'stopSingle': false,
    		'stopDouble': false
    	},

    	initialize: function(options) {
    		this.handlerOptions = OpenLayers.Util.extend(
    			{}, this.defaultHandlerOptions
    		);
    		OpenLayers.Control.prototype.initialize.apply(
    			this, arguments
    		); 
    		this.handler = new OpenLayers.Handler.Click(
    			this, {
    				'click': this.onClick
    			}, this.handlerOptions
    		);
    	}, 

    	onClick: function(e) {
    		/*
    		var m = MPAtlas;
    		if (m.request) {
    			Ext.Ajax.abort(m.request);
    			m.request = null;
    		}
    		if (m.ui.popUp) {
    			m.ui.popUp.hide();
    		}		

    		var lyr = null, url = null;
    		var pt = m.map.getLonLatFromViewPortPx(e.xy);		
    		switch (m.activeLayer) {
    			default:  // mpas
    				lyr = m.mpas;
    				var selected = lyr.selected;
    				if (selected) {
    					if (selected.id) {
    						url = lyr.baseUrl + 'sites/' + selected.id;
    					} else if (selected.url) {
    						url = m.domain + selected.url;
    					}
    					if (url) {
    						document.location.href = url;
    					}
    				} else if (lyr.response) {
    					lyr.formatResponse({point: pt, isClick: true});
    				}
    		}
    		*/
    		var pt = map.getLonLatFromViewPortPx(e.xy);
    		var ll = pt.clone();
            ll.transform(map.projection, map.displayProjection);
            lastlatlon = $('#maptip-content').data('latlon');
    		if (lastlatlon && lastlatlon.lat == ll.lat && lastlatlon.lon == ll.lon) {
    		    //maptipdisable = true;
    		}
    	}	
    });

    maphover = new OpenLayers.Control.Hover();
    mapclick = new OpenLayers.Control.Click();
    map.addControl(maphover);
    maphover.activate();
    map.addControl(mapclick);
    mapclick.activate();

    leafmap.on('locationfound', function(location) {
        leafmap.panTo(new L.LatLng(0, location.latlng.lng));
    });
    leafmap.locate();
});