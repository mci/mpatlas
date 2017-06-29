/* */ 
"format cjs";
(function(process) {
  (function(f) {
    if (typeof exports === "object" && typeof module !== "undefined") {
      module.exports = f();
    } else if (typeof define === "function" && define.amd) {
      define([], f);
    } else {
      var g;
      if (typeof window !== "undefined") {
        g = window;
      } else if (typeof global !== "undefined") {
        g = global;
      } else if (typeof self !== "undefined") {
        g = self;
      } else {
        g = this;
      }
      g.geojsonvt = f();
    }
  })(function() {
    var define,
        module,
        exports;
    return (function e(t, n, r) {
      function s(o, u) {
        if (!n[o]) {
          if (!t[o]) {
            var a = typeof require == "function" && require;
            if (!u && a)
              return a(o, !0);
            if (i)
              return i(o, !0);
            var f = new Error("Cannot find module '" + o + "'");
            throw f.code = "MODULE_NOT_FOUND", f;
          }
          var l = n[o] = {exports: {}};
          t[o][0].call(l.exports, function(e) {
            var n = t[o][1][e];
            return s(n ? n : e);
          }, l, l.exports, e, t, n, r);
        }
        return n[o].exports;
      }
      var i = typeof require == "function" && require;
      for (var o = 0; o < r.length; o++)
        s(r[o]);
      return s;
    })({
      1: [function(require, module, exports) {
        'use strict';
        module.exports = clip;
        var createFeature = require('./feature');
        function clip(features, scale, k1, k2, axis, intersect, minAll, maxAll) {
          k1 /= scale;
          k2 /= scale;
          if (minAll >= k1 && maxAll <= k2)
            return features;
          else if (minAll > k2 || maxAll < k1)
            return null;
          var clipped = [];
          for (var i = 0; i < features.length; i++) {
            var feature = features[i],
                geometry = feature.geometry,
                type = feature.type,
                min,
                max;
            min = feature.min[axis];
            max = feature.max[axis];
            if (min >= k1 && max <= k2) {
              clipped.push(feature);
              continue;
            } else if (min > k2 || max < k1)
              continue;
            var slices = type === 1 ? clipPoints(geometry, k1, k2, axis) : clipGeometry(geometry, k1, k2, axis, intersect, type === 3);
            if (slices.length) {
              clipped.push(createFeature(feature.tags, type, slices, feature.id));
            }
          }
          return clipped.length ? clipped : null;
        }
        function clipPoints(geometry, k1, k2, axis) {
          var slice = [];
          for (var i = 0; i < geometry.length; i++) {
            var a = geometry[i],
                ak = a[axis];
            if (ak >= k1 && ak <= k2)
              slice.push(a);
          }
          return slice;
        }
        function clipGeometry(geometry, k1, k2, axis, intersect, closed) {
          var slices = [];
          for (var i = 0; i < geometry.length; i++) {
            var ak = 0,
                bk = 0,
                b = null,
                points = geometry[i],
                area = points.area,
                dist = points.dist,
                outer = points.outer,
                len = points.length,
                a,
                j,
                last;
            var slice = [];
            for (j = 0; j < len - 1; j++) {
              a = b || points[j];
              b = points[j + 1];
              ak = bk || a[axis];
              bk = b[axis];
              if (ak < k1) {
                if ((bk > k2)) {
                  slice.push(intersect(a, b, k1), intersect(a, b, k2));
                  if (!closed)
                    slice = newSlice(slices, slice, area, dist, outer);
                } else if (bk >= k1)
                  slice.push(intersect(a, b, k1));
              } else if (ak > k2) {
                if ((bk < k1)) {
                  slice.push(intersect(a, b, k2), intersect(a, b, k1));
                  if (!closed)
                    slice = newSlice(slices, slice, area, dist, outer);
                } else if (bk <= k2)
                  slice.push(intersect(a, b, k2));
              } else {
                slice.push(a);
                if (bk < k1) {
                  slice.push(intersect(a, b, k1));
                  if (!closed)
                    slice = newSlice(slices, slice, area, dist, outer);
                } else if (bk > k2) {
                  slice.push(intersect(a, b, k2));
                  if (!closed)
                    slice = newSlice(slices, slice, area, dist, outer);
                }
              }
            }
            a = points[len - 1];
            ak = a[axis];
            if (ak >= k1 && ak <= k2)
              slice.push(a);
            last = slice[slice.length - 1];
            if (closed && last && (slice[0][0] !== last[0] || slice[0][1] !== last[1]))
              slice.push(slice[0]);
            newSlice(slices, slice, area, dist, outer);
          }
          return slices;
        }
        function newSlice(slices, slice, area, dist, outer) {
          if (slice.length) {
            slice.area = area;
            slice.dist = dist;
            if (outer !== undefined)
              slice.outer = outer;
            slices.push(slice);
          }
          return [];
        }
      }, {"./feature": 3}],
      2: [function(require, module, exports) {
        'use strict';
        module.exports = convert;
        var simplify = require('./simplify');
        var createFeature = require('./feature');
        function convert(data, tolerance) {
          var features = [];
          if (data.type === 'FeatureCollection') {
            for (var i = 0; i < data.features.length; i++) {
              convertFeature(features, data.features[i], tolerance);
            }
          } else if (data.type === 'Feature') {
            convertFeature(features, data, tolerance);
          } else {
            convertFeature(features, {geometry: data}, tolerance);
          }
          return features;
        }
        function convertFeature(features, feature, tolerance) {
          if (feature.geometry === null) {
            return;
          }
          var geom = feature.geometry,
              type = geom.type,
              coords = geom.coordinates,
              tags = feature.properties,
              id = feature.id,
              i,
              j,
              rings,
              projectedRing;
          if (type === 'Point') {
            features.push(createFeature(tags, 1, [projectPoint(coords)], id));
          } else if (type === 'MultiPoint') {
            features.push(createFeature(tags, 1, project(coords), id));
          } else if (type === 'LineString') {
            features.push(createFeature(tags, 2, [project(coords, tolerance)], id));
          } else if (type === 'MultiLineString' || type === 'Polygon') {
            rings = [];
            for (i = 0; i < coords.length; i++) {
              projectedRing = project(coords[i], tolerance);
              if (type === 'Polygon')
                projectedRing.outer = (i === 0);
              rings.push(projectedRing);
            }
            features.push(createFeature(tags, type === 'Polygon' ? 3 : 2, rings, id));
          } else if (type === 'MultiPolygon') {
            rings = [];
            for (i = 0; i < coords.length; i++) {
              for (j = 0; j < coords[i].length; j++) {
                projectedRing = project(coords[i][j], tolerance);
                projectedRing.outer = (j === 0);
                rings.push(projectedRing);
              }
            }
            features.push(createFeature(tags, 3, rings, id));
          } else if (type === 'GeometryCollection') {
            for (i = 0; i < geom.geometries.length; i++) {
              convertFeature(features, {
                geometry: geom.geometries[i],
                properties: tags
              }, tolerance);
            }
          } else {
            throw new Error('Input data is not a valid GeoJSON object.');
          }
        }
        function project(lonlats, tolerance) {
          var projected = [];
          for (var i = 0; i < lonlats.length; i++) {
            projected.push(projectPoint(lonlats[i]));
          }
          if (tolerance) {
            simplify(projected, tolerance);
            calcSize(projected);
          }
          return projected;
        }
        function projectPoint(p) {
          var sin = Math.sin(p[1] * Math.PI / 180),
              x = (p[0] / 360 + 0.5),
              y = (0.5 - 0.25 * Math.log((1 + sin) / (1 - sin)) / Math.PI);
          y = y < 0 ? 0 : y > 1 ? 1 : y;
          return [x, y, 0];
        }
        function calcSize(points) {
          var area = 0,
              dist = 0;
          for (var i = 0,
              a,
              b; i < points.length - 1; i++) {
            a = b || points[i];
            b = points[i + 1];
            area += a[0] * b[1] - b[0] * a[1];
            dist += Math.abs(b[0] - a[0]) + Math.abs(b[1] - a[1]);
          }
          points.area = Math.abs(area / 2);
          points.dist = dist;
        }
      }, {
        "./feature": 3,
        "./simplify": 5
      }],
      3: [function(require, module, exports) {
        'use strict';
        module.exports = createFeature;
        function createFeature(tags, type, geom, id) {
          var feature = {
            id: id || null,
            type: type,
            geometry: geom,
            tags: tags || null,
            min: [Infinity, Infinity],
            max: [-Infinity, -Infinity]
          };
          calcBBox(feature);
          return feature;
        }
        function calcBBox(feature) {
          var geometry = feature.geometry,
              min = feature.min,
              max = feature.max;
          if (feature.type === 1) {
            calcRingBBox(min, max, geometry);
          } else {
            for (var i = 0; i < geometry.length; i++) {
              calcRingBBox(min, max, geometry[i]);
            }
          }
          return feature;
        }
        function calcRingBBox(min, max, points) {
          for (var i = 0,
              p; i < points.length; i++) {
            p = points[i];
            min[0] = Math.min(p[0], min[0]);
            max[0] = Math.max(p[0], max[0]);
            min[1] = Math.min(p[1], min[1]);
            max[1] = Math.max(p[1], max[1]);
          }
        }
      }, {}],
      4: [function(require, module, exports) {
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
      }, {
        "./clip": 1,
        "./convert": 2,
        "./tile": 6,
        "./transform": 7,
        "./wrap": 8
      }],
      5: [function(require, module, exports) {
        'use strict';
        module.exports = simplify;
        function simplify(points, tolerance) {
          var sqTolerance = tolerance * tolerance,
              len = points.length,
              first = 0,
              last = len - 1,
              stack = [],
              i,
              maxSqDist,
              sqDist,
              index;
          points[first][2] = 1;
          points[last][2] = 1;
          while (last) {
            maxSqDist = 0;
            for (i = first + 1; i < last; i++) {
              sqDist = getSqSegDist(points[i], points[first], points[last]);
              if (sqDist > maxSqDist) {
                index = i;
                maxSqDist = sqDist;
              }
            }
            if (maxSqDist > sqTolerance) {
              points[index][2] = maxSqDist;
              stack.push(first);
              stack.push(index);
              first = index;
            } else {
              last = stack.pop();
              first = stack.pop();
            }
          }
        }
        function getSqSegDist(p, a, b) {
          var x = a[0],
              y = a[1],
              bx = b[0],
              by = b[1],
              px = p[0],
              py = p[1],
              dx = bx - x,
              dy = by - y;
          if (dx !== 0 || dy !== 0) {
            var t = ((px - x) * dx + (py - y) * dy) / (dx * dx + dy * dy);
            if (t > 1) {
              x = bx;
              y = by;
            } else if (t > 0) {
              x += dx * t;
              y += dy * t;
            }
          }
          dx = px - x;
          dy = py - y;
          return dx * dx + dy * dy;
        }
      }, {}],
      6: [function(require, module, exports) {
        'use strict';
        module.exports = createTile;
        function createTile(features, z2, tx, ty, tolerance, noSimplify) {
          var tile = {
            features: [],
            numPoints: 0,
            numSimplified: 0,
            numFeatures: 0,
            source: null,
            x: tx,
            y: ty,
            z2: z2,
            transformed: false,
            min: [2, 1],
            max: [-1, 0]
          };
          for (var i = 0; i < features.length; i++) {
            tile.numFeatures++;
            addFeature(tile, features[i], tolerance, noSimplify);
            var min = features[i].min,
                max = features[i].max;
            if (min[0] < tile.min[0])
              tile.min[0] = min[0];
            if (min[1] < tile.min[1])
              tile.min[1] = min[1];
            if (max[0] > tile.max[0])
              tile.max[0] = max[0];
            if (max[1] > tile.max[1])
              tile.max[1] = max[1];
          }
          return tile;
        }
        function addFeature(tile, feature, tolerance, noSimplify) {
          var geom = feature.geometry,
              type = feature.type,
              simplified = [],
              sqTolerance = tolerance * tolerance,
              i,
              j,
              ring,
              p;
          if (type === 1) {
            for (i = 0; i < geom.length; i++) {
              simplified.push(geom[i]);
              tile.numPoints++;
              tile.numSimplified++;
            }
          } else {
            for (i = 0; i < geom.length; i++) {
              ring = geom[i];
              if (!noSimplify && ((type === 2 && ring.dist < tolerance) || (type === 3 && ring.area < sqTolerance))) {
                tile.numPoints += ring.length;
                continue;
              }
              var simplifiedRing = [];
              for (j = 0; j < ring.length; j++) {
                p = ring[j];
                if (noSimplify || p[2] > sqTolerance) {
                  simplifiedRing.push(p);
                  tile.numSimplified++;
                }
                tile.numPoints++;
              }
              if (type === 3)
                rewind(simplifiedRing, ring.outer);
              simplified.push(simplifiedRing);
            }
          }
          if (simplified.length) {
            var tileFeature = {
              geometry: simplified,
              type: type,
              tags: feature.tags || null
            };
            if (feature.id !== null) {
              tileFeature.id = feature.id;
            }
            tile.features.push(tileFeature);
          }
        }
        function rewind(ring, clockwise) {
          var area = signedArea(ring);
          if (area < 0 === clockwise)
            ring.reverse();
        }
        function signedArea(ring) {
          var sum = 0;
          for (var i = 0,
              len = ring.length,
              j = len - 1,
              p1,
              p2; i < len; j = i++) {
            p1 = ring[i];
            p2 = ring[j];
            sum += (p2[0] - p1[0]) * (p1[1] + p2[1]);
          }
          return sum;
        }
      }, {}],
      7: [function(require, module, exports) {
        'use strict';
        exports.tile = transformTile;
        exports.point = transformPoint;
        function transformTile(tile, extent) {
          if (tile.transformed)
            return tile;
          var z2 = tile.z2,
              tx = tile.x,
              ty = tile.y,
              i,
              j,
              k;
          for (i = 0; i < tile.features.length; i++) {
            var feature = tile.features[i],
                geom = feature.geometry,
                type = feature.type;
            if (type === 1) {
              for (j = 0; j < geom.length; j++)
                geom[j] = transformPoint(geom[j], extent, z2, tx, ty);
            } else {
              for (j = 0; j < geom.length; j++) {
                var ring = geom[j];
                for (k = 0; k < ring.length; k++)
                  ring[k] = transformPoint(ring[k], extent, z2, tx, ty);
              }
            }
          }
          tile.transformed = true;
          return tile;
        }
        function transformPoint(p, extent, z2, tx, ty) {
          var x = Math.round(extent * (p[0] * z2 - tx)),
              y = Math.round(extent * (p[1] * z2 - ty));
          return [x, y];
        }
      }, {}],
      8: [function(require, module, exports) {
        'use strict';
        var clip = require('./clip');
        var createFeature = require('./feature');
        module.exports = wrap;
        function wrap(features, buffer, intersectX) {
          var merged = features,
              left = clip(features, 1, -1 - buffer, buffer, 0, intersectX, -1, 2),
              right = clip(features, 1, 1 - buffer, 2 + buffer, 0, intersectX, -1, 2);
          if (left || right) {
            merged = clip(features, 1, -buffer, 1 + buffer, 0, intersectX, -1, 2) || [];
            if (left)
              merged = shiftFeatureCoords(left, 1).concat(merged);
            if (right)
              merged = merged.concat(shiftFeatureCoords(right, -1));
          }
          return merged;
        }
        function shiftFeatureCoords(features, offset) {
          var newFeatures = [];
          for (var i = 0; i < features.length; i++) {
            var feature = features[i],
                type = feature.type;
            var newGeometry;
            if (type === 1) {
              newGeometry = shiftCoords(feature.geometry, offset);
            } else {
              newGeometry = [];
              for (var j = 0; j < feature.geometry.length; j++) {
                newGeometry.push(shiftCoords(feature.geometry[j], offset));
              }
            }
            newFeatures.push(createFeature(feature.tags, type, newGeometry, feature.id));
          }
          return newFeatures;
        }
        function shiftCoords(points, offset) {
          var newPoints = [];
          newPoints.area = points.area;
          newPoints.dist = points.dist;
          for (var i = 0; i < points.length; i++) {
            newPoints.push([points[i][0] + offset, points[i][1], points[i][2]]);
          }
          return newPoints;
        }
      }, {
        "./clip": 1,
        "./feature": 3
      }]
    }, {}, [4])(4);
  });
})(require('process'));
