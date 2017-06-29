/* */ 
(function(process) {
  'use strict';
  module.exports = geojsonvt;
  var convert = require('./convert'),
      transform = require('./transform'),
      clip = require('./clip'),
      wrap = require('./wrap'),
      createTile = require('./tile');
  function geojsonvt(data, options) {
    return new GeoJSONVT(data, options);
  }
  function GeoJSONVT(data, options) {
    options = this.options = extend(Object.create(this.options), options);
    var debug = options.debug;
    if (debug)
      console.time('preprocess data');
    var z2 = 1 << options.maxZoom,
        features = convert(data, options.tolerance / (z2 * options.extent));
    this.tiles = {};
    this.tileCoords = [];
    if (debug) {
      console.timeEnd('preprocess data');
      console.log('index: maxZoom: %d, maxPoints: %d', options.indexMaxZoom, options.indexMaxPoints);
      console.time('generate tiles');
      this.stats = {};
      this.total = 0;
    }
    features = wrap(features, options.buffer / options.extent, intersectX);
    if (features.length)
      this.splitTile(features, 0, 0, 0);
    if (debug) {
      if (features.length)
        console.log('features: %d, points: %d', this.tiles[0].numFeatures, this.tiles[0].numPoints);
      console.timeEnd('generate tiles');
      console.log('tiles generated:', this.total, JSON.stringify(this.stats));
    }
  }
  GeoJSONVT.prototype.options = {
    maxZoom: 14,
    indexMaxZoom: 5,
    indexMaxPoints: 100000,
    solidChildren: false,
    tolerance: 3,
    extent: 4096,
    buffer: 64,
    debug: 0
  };
  GeoJSONVT.prototype.splitTile = function(features, z, x, y, cz, cx, cy) {
    var stack = [features, z, x, y],
        options = this.options,
        debug = options.debug,
        solid = null;
    while (stack.length) {
      y = stack.pop();
      x = stack.pop();
      z = stack.pop();
      features = stack.pop();
      var z2 = 1 << z,
          id = toID(z, x, y),
          tile = this.tiles[id],
          tileTolerance = z === options.maxZoom ? 0 : options.tolerance / (z2 * options.extent);
      if (!tile) {
        if (debug > 1)
          console.time('creation');
        tile = this.tiles[id] = createTile(features, z2, x, y, tileTolerance, z === options.maxZoom);
        this.tileCoords.push({
          z: z,
          x: x,
          y: y
        });
        if (debug) {
          if (debug > 1) {
            console.log('tile z%d-%d-%d (features: %d, points: %d, simplified: %d)', z, x, y, tile.numFeatures, tile.numPoints, tile.numSimplified);
            console.timeEnd('creation');
          }
          var key = 'z' + z;
          this.stats[key] = (this.stats[key] || 0) + 1;
          this.total++;
        }
      }
      tile.source = features;
      if (!cz) {
        if (z === options.indexMaxZoom || tile.numPoints <= options.indexMaxPoints)
          continue;
      } else {
        if (z === options.maxZoom || z === cz)
          continue;
        var m = 1 << (cz - z);
        if (x !== Math.floor(cx / m) || y !== Math.floor(cy / m))
          continue;
      }
      if (!options.solidChildren && isClippedSquare(tile, options.extent, options.buffer)) {
        if (cz)
          solid = z;
        continue;
      }
      tile.source = null;
      if (debug > 1)
        console.time('clipping');
      var k1 = 0.5 * options.buffer / options.extent,
          k2 = 0.5 - k1,
          k3 = 0.5 + k1,
          k4 = 1 + k1,
          tl,
          bl,
          tr,
          br,
          left,
          right;
      tl = bl = tr = br = null;
      left = clip(features, z2, x - k1, x + k3, 0, intersectX, tile.min[0], tile.max[0]);
      right = clip(features, z2, x + k2, x + k4, 0, intersectX, tile.min[0], tile.max[0]);
      if (left) {
        tl = clip(left, z2, y - k1, y + k3, 1, intersectY, tile.min[1], tile.max[1]);
        bl = clip(left, z2, y + k2, y + k4, 1, intersectY, tile.min[1], tile.max[1]);
      }
      if (right) {
        tr = clip(right, z2, y - k1, y + k3, 1, intersectY, tile.min[1], tile.max[1]);
        br = clip(right, z2, y + k2, y + k4, 1, intersectY, tile.min[1], tile.max[1]);
      }
      if (debug > 1)
        console.timeEnd('clipping');
      if (features.length) {
        stack.push(tl || [], z + 1, x * 2, y * 2);
        stack.push(bl || [], z + 1, x * 2, y * 2 + 1);
        stack.push(tr || [], z + 1, x * 2 + 1, y * 2);
        stack.push(br || [], z + 1, x * 2 + 1, y * 2 + 1);
      }
    }
    return solid;
  };
  GeoJSONVT.prototype.getTile = function(z, x, y) {
    var options = this.options,
        extent = options.extent,
        debug = options.debug;
    var z2 = 1 << z;
    x = ((x % z2) + z2) % z2;
    var id = toID(z, x, y);
    if (this.tiles[id])
      return transform.tile(this.tiles[id], extent);
    if (debug > 1)
      console.log('drilling down to z%d-%d-%d', z, x, y);
    var z0 = z,
        x0 = x,
        y0 = y,
        parent;
    while (!parent && z0 > 0) {
      z0--;
      x0 = Math.floor(x0 / 2);
      y0 = Math.floor(y0 / 2);
      parent = this.tiles[toID(z0, x0, y0)];
    }
    if (!parent || !parent.source)
      return null;
    if (debug > 1)
      console.log('found parent tile z%d-%d-%d', z0, x0, y0);
    if (isClippedSquare(parent, extent, options.buffer))
      return transform.tile(parent, extent);
    if (debug > 1)
      console.time('drilling down');
    var solid = this.splitTile(parent.source, z0, x0, y0, z, x, y);
    if (debug > 1)
      console.timeEnd('drilling down');
    if (solid !== null) {
      var m = 1 << (z - solid);
      id = toID(solid, Math.floor(x / m), Math.floor(y / m));
    }
    return this.tiles[id] ? transform.tile(this.tiles[id], extent) : null;
  };
  function toID(z, x, y) {
    return (((1 << z) * y + x) * 32) + z;
  }
  function intersectX(a, b, x) {
    return [x, (x - a[0]) * (b[1] - a[1]) / (b[0] - a[0]) + a[1], 1];
  }
  function intersectY(a, b, y) {
    return [(y - a[1]) * (b[0] - a[0]) / (b[1] - a[1]) + a[0], y, 1];
  }
  function extend(dest, src) {
    for (var i in src)
      dest[i] = src[i];
    return dest;
  }
  function isClippedSquare(tile, extent, buffer) {
    var features = tile.source;
    if (features.length !== 1)
      return false;
    var feature = features[0];
    if (feature.type !== 3 || feature.geometry.length > 1)
      return false;
    var len = feature.geometry[0].length;
    if (len !== 5)
      return false;
    for (var i = 0; i < len; i++) {
      var p = transform.point(feature.geometry[0][i], extent, tile.z2, tile.x, tile.y);
      if ((p[0] !== -buffer && p[0] !== extent + buffer) || (p[1] !== -buffer && p[1] !== extent + buffer))
        return false;
    }
    return true;
  }
})(require('process'));
