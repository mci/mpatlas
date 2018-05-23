define([
  // These are path aliases configured in the requireJS bootstrap
  'jquery',
  'jquery.cookie'
], function($){
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

    var set_random_banner = function () {
        var bannerclasses = ["humpback-j4", "angelfish-j4", "turtle-j4", "manatee-j4", "otter-j4"];
        var randomclass = bannerclasses[Math.floor(Math.random() * bannerclasses.length)];
        $('#slidebanner').removeClass(bannerclasses.join(' ')).addClass(randomclass);
    };

    var show_donate_banner = function (force) {
        if (force || !hasdonatecookie()) {
            $('#slidebanner').hide().removeClass('small');
            $('#slidebanner').slideDown('slow', function() {
                setdonatecookie();
            });
        } else {
            // $('#slidebanner').addClass('small').show();
        }
    };

    set_random_banner();
    // $('#slidebanner').hide();
    // $("#slidebanner").css("position", "relative");
    // $("#slidebanner").css("top", "0px");

    $('.slidehide').click(function(e) {
        e.preventDefault();
        $('#slidebanner').slideUp('slow', function() {
            // slide away complete
            $('#slidebanner').addClass('small').show();
        });
    });

    return {
        set_random_banner: set_random_banner,
        show_donate_banner: show_donate_banner
    };
    // What we return here will be used by other modules
});
