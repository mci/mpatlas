/* */ 
"format cjs";


L.Renderer.GL.Tile = L.Canvas.extend({

// 	initialize: function (tileSize, options) {
// 		L.Canvas.prototype.initialize.call(this, options);
// 		this._size = tileSize;
//
// 		this._initContainer();
// 		this._container.setAttribute('width', this._size.x);
// 		this._container.setAttribute('height', this._size.y);
// 		this._layers = {};
// 		this._drawnLayers = {};
// 	},

	getContainer: function() {
		return this._map ? this._map._glCanvas : undefined;
	},

	onAdd: L.Util.FalseFn,

	_initContainer: function () {
// 		var container = this._container = document.createElement('canvas');

// 		L.DomEvent
// 			.on(container, 'mousemove', L.Util.throttle(this._onMouseMove, 32, this), this)
// 			.on(container, 'click dblclick mousedown mouseup contextmenu', this._onClick, this)
// 			.on(container, 'mouseout', this._handleMouseOut, this);

// 		this._ctx = container.getContext('2d');
	},


	/// TODO: Modify _initPath to include an extra parameter, a group name
	/// to order symbolizers by z-index

});


L.renderer.gl.tile = function(tileSize, opts){
	return new L.Renderer.GL.Tile(tileSize, opts);
}

