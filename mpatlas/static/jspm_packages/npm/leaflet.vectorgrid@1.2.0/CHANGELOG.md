
## 1.2.0

* Refactored the code modules into ES6 modules
* Switched the build system and dependencies to use RollupJS
* Store styles set through `setFeatureStyle` so the changes persist after zooming/panning

## 1.1.0

* Support for mouse/pointer events on geometries (by @perliedman)
* Support for point symbolizers as basic `CircleMarker`s (by @perliedman)

## 1.0.1

* Updated dependencies, notably Leaflet 1.0.1.
* Updated build script so Windows users don't hit a 20-year-old legacy filesystem bug (by @LuSilf)

## 1.0.0

* Switch to web workers for most of the heavy lifting (geojson-vt, topojson).

## 0.1.2

* Do not throw errors when trying (and failing) to render points

## 0.1.0

* TopoJSON support

## 0.0.0

* Initial, supprt-buggy release
