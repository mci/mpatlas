/* */ 
"format cjs";

L.GridLayer.Vector = L.GridLayer.extend({

	initialize: function(options) {
		this._group = L.layerGroup();
		options = L.setOptions(this, options);
	},

	onAdd: function(map) {
		L.GridLayer.prototype.onAdd.call(this, map);
		map.addLayer(this._group);
	},

	onRemove: function(map) {
		L.GridLayer.prototype.onRemove.call(this, map);
		map.removeLayer(this._group);
	},

	_getGeoJSONForTile: function(coords) {
		console.warn('Using L.GridLayer.Vector stand-alone does nothing');
	},

	_addTile: function(coords, container) {
		var tilePos = this._getTilePos(coords),
		    key = this._tileCoordsToKey(coords);

		var geojson = this._getGeoJSONForTile(coords);
		var sublayer;
		var loadSublayerFunc;

		if (window.Promise && geojson instanceof Promise) {

			loadSublayerFunc = function() {
				geojson.then(function(data){
					if (!this._tiles[key]) { return; }
					sublayer = L.geoJson(data, this.options);
					this._group.addLayer(sublayer);

					this._tiles[key].geojson  = data;
					this._tiles[key].sublayer = sublayer;

					this.fire('tileload', {
						tile: undefined,
						coords: coords
					});
				}.bind(this));
			}.bind(this);

		} else {
			loadSublayerFunc = function() {
				if (!this._tiles[key]) { return; }
				sublayer = L.geoJson(geojson, this.options);
				this._group.addLayer(sublayer);

				this._tiles[key].geojson  = geojson;
				this._tiles[key].sublayer = sublayer;

				this.fire('tileload', {
					tile: undefined,
					coords: coords
				});
			}.bind(this);
		}

// 		console.log('Should add data for ', key, geojson);

		this._tiles[key] = {
			geojson: undefined,
			sublayer: undefined,
			coords: coords,
			current: true
		};

		this.fire('tileloadstart', {
			tile: undefined,
			coords: coords
		});

		//// TODO: *Maybe* this could be an option, for non-translucent grids.
		if (this._map._animatingZoom) {
			this._map.once('zoomend', loadSublayerFunc);
		} else {
			loadSublayerFunc();
		}
	},

	_removeTile: function (key) {
// 		console.log('Should remove data for ', key);

		var tile = this._tiles[key];
		if (!tile) { return; }

		if (tile.sublayer) {
			this._group.removeLayer(tile.sublayer);
		}

		delete this._tiles[key];

		this.fire('tileunload', {
			tile: undefined,
			coords: this._keyToTileCoords(key)
		});
	},

});


// geojson-vt powered!
// NOTE: Assumes the global `geojson-vt` exists!!!
L.GridLayer.Vector.Slicer = L.GridLayer.Vector.extend({

	initialize: function(geojson, options) {
		// Inherits available options from geojson-vt!
		this._slicer = geojsonvt(geojson, options);

		if (!options) { options = {}; }
		if (!options.extent) { options.extent = 4096; }	// Default for geojson-vt
		L.GridLayer.Vector.prototype.initialize.call(this, options);
	},


	_getGeoJSONForTile: function(coords) {
		var tileSize = this.getTileSize();
		// NW pixel from map origin
		var nwPoint = coords.scaleBy(tileSize);

		// How many pixels per unit of VT extent
		var pxPerExtent = this.options.tileSize / this.options.extent;
		var zoom = coords.z;

		var vectorTile = this._slicer.getTile(coords.z, coords.x, coords.y);
		if (!vectorTile) { return; }

		var geojson = {
			type: 'FeatureCollection',
			features: []
		};

		vectorTile.features.forEach(function(vtf){	// VectorTile Feature

			var gjf = { // GeoJson Feature
				type: 'Feature',
				geometry: {
					type: undefined,
					coordinates: vtf.geometry
				},
				properties: vtf.tags
			}

			if (vtf.type === 1) {
				gjf.geometry.type = 'Point';
			} else if (vtf.type === 2) {
				gjf.geometry.type = 'LineString';
			} else if (vtf.type === 3) {
				gjf.geometry.type = 'Polygon';
			}

			gjf.geometry.coordinates = L.GeoJSON.coordsToLatLngs(vtf.geometry, vtf.type-2, function(c) {
				var p = [nwPoint.x + c[0] * pxPerExtent,
				         nwPoint.y + c[1] * pxPerExtent];
				var u = this._map.unproject(p, coords.z);
				return [u.lng, u.lat];
			}.bind(this));

			geojson.features.push(gjf);

		}.bind(this));

		return geojson;
	},

});




// Network & Protobuf powered!
// NOTE: Assumes the globals `VectorTile` and `Pbf` exist!!!
L.GridLayer.Vector.Protobuf = L.GridLayer.Vector.extend({

	options: {
		subdomains: 'abc',	// Like L.TileLayer
	},


	initialize: function(url, options) {
		// Inherits options from geojson-vt!
// 		this._slicer = geojsonvt(geojson, options);
		this._url = url;
		L.GridLayer.Vector.prototype.initialize.call(this, options);
	},


	_getSubdomain: L.TileLayer.prototype._getSubdomain,


	_getGeoJSONForTile: function(coords) {

		var tileUrl = L.Util.template(this._url, L.extend({
			s: this._getSubdomain(coords),
			x: coords.x,
			y: coords.y,
			z: coords.z
// 			z: this._getZoomForUrl()	/// TODO: Maybe replicate TileLayer's maxNativeZoom
		}, this.options));


		return fetch(tileUrl).then(function(response){

// 			console.log(response);
			if (!response.ok) {
				return {layers:[]};
			}

			return response.blob().then( function (blob) {
// 				console.log(blob);

				var reader = new FileReader();
				return new Promise(function(resolve){
					reader.addEventListener("loadend", function() {
						// reader.result contains the contents of blob as a typed array

						// blob.type === 'application/x-protobuf'
						var pbf = new Pbf( reader.result );
// 						console.log(pbf);
						return resolve(new vectorTile.VectorTile( pbf ));

					});
					reader.readAsArrayBuffer(blob);
				});
			});
		}).then(function(json){

			console.log('Vector tile:', json.layers);
// 			console.log('Vector tile water:', json.layers.water);	// Instance of VectorTileLayer


			var geojson = {
				type: 'FeatureCollection',
				features: []
			};

			for(var layerName in json.layers) {
				var layer = json.layers[layerName];

				for (var i=0; i<layer.length; i++) {
					var feat = layer.feature(i).toGeoJSON(coords.x, coords.y, coords.z);
					feat.properties.__layer = layerName;
					geojson.features.push(feat);
				}
			}

			return geojson;
		});
	},

});


L.gridLayer.vector = function (options) {
	return new L.GridLayer.Vector(options);
};

L.gridLayer.vector.slicer = function (geojson, options) {
	return new L.GridLayer.Vector.Slicer(geojson, options);
};

L.gridLayer.vector.protobuf = function (url, options) {
	return new L.GridLayer.Vector.Protobuf(url, options);
};

