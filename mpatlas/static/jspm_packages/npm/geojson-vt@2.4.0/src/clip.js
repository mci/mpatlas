/* */ 
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