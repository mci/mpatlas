define([
  // These are path aliases configured in the requireJS bootstrap
  'leaflet',
  'leaflet_utils'
], function(){
    L.Maptip = L.Popup.extend({
    	options: {
    		minWidth: 50,
    		maxWidth: 300,
    		maxHeight: null,
    		autoPan: true,
    		closeButton: true,
    		offset: new L.Point(0, 0),
    		autoPanPadding: new L.Point(5, 5),
    		className: '',
    		closePopupOnClick: false
    		//closePopupOnClick: true
    	},

    	onAdd: function (map) {
    		this._map = map;

    		if (!this._container) {
    			this._initLayout();
    		}
    		this._updateContent();

    		this._container.style.opacity = '0';
    		map._panes.popupPane.appendChild(this._container);

    		map.on('viewreset', this._updatePosition, this);

    		if (this.options.closePopupOnClick && map.options.closePopupOnClick) {
    			map.on('preclick', this._close, this);
    		}

    		this.update();

    		this._container.style.opacity = '1'; //TODO fix ugly opacity hack
    	},
     	
     	_initLayout: function () {
    		var prefix = 'maptip',
    		    leafletprefix = 'leaflet-popup', // need this to make sure 3dtransform css from leaflet get applied properly in webkit, otherwise it will be unclickable
    			container = this._container = L.DomUtil.create('div', leafletprefix + ' ' + prefix + ' ' + this.options.className),
    			closeButton;

    		if (this.options.closeButton) {
     			closeButton = this._closeButton = L.DomUtil.create('a', 'leaflet-popup-close-button ' + prefix + '-close-button', container);
     			closeButton.href = '#close';
     			closeButton.innerHTML = 'x';

    			L.DomEvent.addListener(closeButton, 'click', this._onCloseButtonClick, this);
    		}

    		var wrapper = this._wrapper = L.DomUtil.create('div', prefix + '-content-wrapper', container);
    		L.DomEvent.disableClickPropagation(wrapper);

    		this._contentNode = L.DomUtil.create('div', prefix + '-content', wrapper);
    		L.DomEvent.addListener(this._contentNode, 'mousewheel', L.DomEvent.stopPropagation);

    		this._tipContainer = L.DomUtil.create('div', prefix + '-arrow-container', container);
    		this._tip = L.DomUtil.create('div', prefix + '-arrow', this._tipContainer);
    	},
    	
    	setLatLng: function (latlng) {
    		this._latlng = latlng;
    		this.update();
    		return this;
    	},
    	
    	setLayerPoint: function(point) {
    	    if (!this._map) { return this; }
    	    latlng_unbounded = this._map.layerPointToLatLngUnbounded(point);
    	    return this.setLatLng(latlng_unbounded);
    	},
    	
    	_updatePosition: function () {
    		var pos = this._map.latLngToLayerPoint(this._latlng);

            // this._containerBottom = -pos.y - this.options.offset.y;
            // this._containerLeft = pos.x - Math.round(this._containerWidth / 2) + this.options.offset.x;
            
            // this._container.style.bottom = this._containerBottom + 'px';
            // this._container.style.left = this._containerLeft + 'px';
    		
    		this._containerTop = pos.y + this.options.offset.y;
    		this._containerLeft = pos.x + this.options.offset.x;

    		this._container.style.top = this._containerTop + 'px';
    		this._container.style.left = this._containerLeft + 'px';
    	},
    	
    	_adjustPan: function () {
    		if (!this.options.autoPan) { return; }

    		var map = this._map,
    			containerHeight = this._container.offsetHeight,
    			containerWidth = this._containerWidth,
    			statsContainer = L.DomUtil.get('stats_overlay'),
    			statsWidth = (statsContainer.offsetWidth ? statsContainer.offsetWidth : 0)
    			
    			layerPos = new L.Point(
    				this._containerLeft + 14 + statsWidth,
    				this._containerTop - 29),
    			
    			containerPos = map.layerPointToContainerPoint(layerPos),
    			adjustOffset = new L.Point(0, 0),
    			padding      = this.options.autoPanPadding,
    			size         = map.getSize();
    		
    		if (containerPos.x < 0) {
    			adjustOffset.x = containerPos.x - padding.x;
    		}
    		if (containerPos.x + containerWidth > size.x) {
    			adjustOffset.x = containerPos.x + containerWidth - size.x + padding.x;
    		}
    		if (containerPos.y < 0) {
    			adjustOffset.y = containerPos.y - padding.y;
    		}
    		if (containerPos.y + containerHeight > size.y) {
    			adjustOffset.y = containerPos.y + containerHeight - size.y + padding.y;
    		}
    		
    		if (adjustOffset.x || adjustOffset.y) {
    			map.panBy(adjustOffset);
    		}
    	}
    });
    
    return L.Maptip;
    // What we return here will be used by other modules
});
