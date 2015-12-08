define([
  // These are path aliases configured in the requireJS bootstrap
  'http://libs.cartocdn.com/cartodb.js/v3/3.12.12/cartodb',
], function() {
    var MarkerWrap = function() {
        var markerLocation = new L.LatLng(51.5, -0.09),
      	    markerLocation2 = new L.LatLng(markerLocation.lat, markerLocation.lng + 360, true),
      	    markerLocation3 = new L.LatLng(markerLocation.lat, markerLocation.lng - 360, true);
    };
    
    var GeoJSONWrap = function() {
        
    }
    
    L.Map.include({
        layerPointToLatLngUnbounded: function(point) {
            var unbounded = true; // true to set unbounded LatLng
            return this.unproject(point.add(mpatlas.map.getPixelOrigin()), this.getZoom(), unbounded); 
        }
    });
    
    return {
        MarkerWrap: MarkerWrap,
        GeoJSONWrap: GeoJSONWrap,
        Map: L.Map
    };
});