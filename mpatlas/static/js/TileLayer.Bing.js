L.TileLayer.Bing = L.TileLayer.extend({
    initialize: function(url, options) {        
        // hard-coded url to the tiles. this allows us to skip the intial call to retrieve metadata
        this._url = url
        L.Util.setOptions(this, options);
    },
    getTileUrl: function(xy, z) {
        var subdomains = [0,1,2,3,4,5,6],
            quadDigits = [],
            i = z,
            digit, mask, quadKey;
            
        // borrowed directly from OpenLayers
        for (; i > 0; --i) {
            digit = '0';
            mask = 1 << (i - 1);
            if ((xy.x & mask) != 0) {
                digit++;
            }
            if ((xy.y & mask) != 0) {
                digit++;
                digit++;
            }
            quadDigits.push(digit);
        }

        return this._url.replace('{subdomain}', subdomains[(xy.x + xy.y) % subdomains.length]).replace('{quadkey}', quadDigits.join(""));
    }

});