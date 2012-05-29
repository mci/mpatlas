define([
  // These are path aliases configured in the requireJS bootstrap
  'leaflet'
], function(){
    L.Maptip = L.Popup.extend({
    	options: {
    		minWidth: 50,
    		maxWidth: 300,
    		maxHeight: null,
    		autoPan: true,
    		closeButton: true,
    		offset: new L.Point(0, 2),
    		autoPanPadding: new L.Point(5, 5),
    		className: '',
    		closePopupOnClick: false
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

    		this._update();

    		this._container.style.opacity = '1'; //TODO fix ugly opacity hack
    	}
    });
    
    return L.Maptip;
    // What we return here will be used by other modules
});
