define([
  // These are path aliases configured in the requireJS bootstrap
  'leaflet',
], function() {
    var MarkerWrap = function() {
        var markerLocation = new L.LatLng(51.5, -0.09),
      	    markerLocation2 = new L.LatLng(markerLocation.lat, markerLocation.lng + 360, true),
      	    markerLocation3 = new L.LatLng(markerLocation.lat, markerLocation.lng - 360, true),
    };
    
    var GeoJSONWrap = function() {
        
    }
    
    return {
        MarkerWrap: MarkerWrap,
        GeoJSONWrap: GeoJSONWrap
    };
};