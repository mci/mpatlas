(function (root, factory) {
    if (typeof define === "function" && define.amd) {
        define(['jquery', 'jquery.cookie'], factory);
    } else if (typeof module === "object" && module.exports) {
        var jquery = require('jquery');
        var jqcookie = require('jquery.cookie');
        module.exports = factory(jquery);
    } else {
        root.donate_banner = factory(root.jQuery);
    }
})(this, function($){
    var donatecookiename = 'mpatlas_saw_donate_30min';
    var setdonatecookie = function() {
        // set session cookie
        var expdate = new Date();
        var minutes = 30; // 30 minutes
        // var minutes = 12 * 60; // 12 hours
        expdate.setTime(expdate.getTime() + (minutes * 60 * 1000));
        $.cookie(donatecookiename, 'true', { expires: expdate, path: '/' });
        // $.cookie(donatecookiename, 'true', { path: '/' });
    };
    var hasdonatecookie = function() {
        return $.cookie(donatecookiename);
    };

    var set_random_banner = function() {
        var bannerclasses = ["humpback-j4", "angelfish-j4", "turtle-j4", "manatee-j4", "otter-j4"];
        var randomclass = bannerclasses[Math.floor(Math.random() * bannerclasses.length)];
        $('#slidebanner').removeClass(bannerclasses.join(' ')).addClass(randomclass);
    };

    var show_donate_banner = function(force) {
        if (force || !hasdonatecookie()) {
            $('#slidebanner').hide().removeClass('small');
            $('#slidebanner').slideDown('slow', function() {
                setdonatecookie();
            });
        } else {
            // $('#slidebanner').addClass('small').show();
        }
    };

    var ready_banner = function() {
        set_random_banner();
        $('.slidehide').click(function(e) {
            e.preventDefault();
            $('#slidebanner').slideUp('slow', function() {
                // slide away complete
                $('#slidebanner').addClass('small').show();
            });
        });
    };

    try {
        ready_banner();
    } catch (e) {
        //
    }

    return {
        set_random_banner: set_random_banner,
        show_donate_banner: show_donate_banner,
        ready_banner: ready_banner
    };
});
