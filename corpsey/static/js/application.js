// Infinite Corpse js brains
// nate@clixel.com 2013

// @codekit-prepend "libs/jquery-3.2.0.js"
// @codekit-prepend "libs/jquery-ui-1.12.1.js"
// @codekit-prepend "libs/jquery.lazyload.min.js"
// @codekit-prepend "bower_components/imagesloaded/imagesloaded.pkgd.js"
// @codekit-prepend "bower_components/icanhaz/ICanHaz.js"
// @codekit-prepend "libs/jquery.isotope.min.js"
// @codekit-prepend "bower_components/history.js/scripts/bundled-uncompressed/html5/jquery.history.js"
// @codekit-prepend "bower_components/jquery-validation/dist/jquery.validate.js"
// @codekit-prepend "libs/jquery.ui.touch-punch.js"

$.corpsey = (function() {
    var _hdpi_enabled,
        medium_width,
        small_width,
        _touch_enabled;

    function _init() {
        // Are we on a retina display?
        _hdpi_enabled = (window.devicePixelRatio >= 2);
        _touch_enabled = (window.DocumentTouch && document instanceof DocumentTouch);
        $('html').toggleClass('no-touchevents', _touch_enabled);

        // Get screen width and roll up nav if mobile
        _resize();
        if (small_width) {
            $('nav.main ul').hide();
        }

        $('<a id="mobile-nav" />').appendTo('body').click(function() {
            $('nav.main ul').slideToggle('fast');
        });

        // Search-o-rama
        $('<li><input id="get-artist" placeholder="SEARCH" autocomplete="off" autocorrect="off" autocapitalize="off"></li>').prependTo('nav.main ul');
        $('#get-artist').autocomplete({
            source: "/get_artists/",
            minLength: 2,
            focus: function( event, ui ) {
                $('.ui-autocomplete div').removeClass('active');
                $('.ui-autocomplete div:contains('+ui.item.value+')').addClass('active');
                return false;
            },
            search: function( event, ui ) {
                _trackEvent('Search', $('#get-artist').val())
            },
            select: function( event, ui ) {
                location.href = ui.item.url;
                return false;
            }
         }).on('blur', function() {
            $(this).val('');
         });

        // Focus on login form if present
        $('#id_username').focus();

        // Homepage?
        if ($('body#homepage').length) {
            // Scroll down to recent contributors from homepage button
            $('li.recent a').click(function() {
                $('html,body').animate({scrollTop:$('#recent-contributors').offset().top }, 'fast');
                return false;
            });

            // Lazy load images
            $('img.panel').lazyload({
                threshold: 250,
                hidpi_support: true
            });
        }
    }

    function _resize() {
        var screen_width = document.documentElement.clientWidth;
        medium_width = screen_width <= 1020;
        small_width = screen_width <= 700;
        // Show mobile "=" nav toggler if not on homepage
        if (small_width && $('#homepage').length===0) {
            $('#mobile-nav').show();
        } else {
            $('nav.main ul').show();
            $('#mobile-nav').hide();
        }
    }

    // Track AJAX pages in Analytics
    function _trackPage() {
      if (typeof ga !== 'undefined') {
        ga('send', 'pageview', location.pathname);
      }
    }

    // Track events in Analytics
    function _trackEvent(category, action) {
      if (typeof ga !== 'undefined') {
        ga('send', 'event', category, action);
      }
    }

    // Public methods
    return {
        init: _init,
        resize: _resize,
        trackPage: _trackPage,
        trackEvent: function(category, action) {
            _trackEvent(category, action);
        },
        hdpi_enabled: function() {
            return _hdpi_enabled;
        },
        touch_enabled: function() {
            return _touch_enabled;
        }
    };
})();

// Fire up the mothership
$(window).ready(function(){
    $.corpsey.init();
});
$(window).resize(function(){
    $.corpsey.resize();
});
