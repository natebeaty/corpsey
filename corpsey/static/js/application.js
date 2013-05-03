// trubble club codes for pleasure

$.corpsey = (function() {
    var _hdpi_enabled;

    var medium_width = false,
        small_width = false,
        delayed_resize_timer = false;

    function _init() {
        // are we on a retina display?
        _hdpi_enabled = (window.devicePixelRatio >= 2);

        // get screen width and roll up nav if mobile
        _resize();
        if (small_width) $('nav.main ul').hide();

        $('<a id="mobile-nav" />').appendTo('body').click(function() {
            $('nav.main ul').slideToggle('fast');    
        });

        // search-o-rama
        $('<li><input id="get-artist" placeholder="SEARCH" autocomplete="off" autocorrect="off" autocapitalize="off"></li>').prependTo('nav.main ul');
        $('#get-artist').autocomplete({
            source: "/get_artists/",
            minLength: 2,
            focus: function( event, ui ) {
                $('.ui-autocomplete a').removeClass('active');
                $('.ui-autocomplete a:contains('+ui.item.value+')').addClass('active');
                return false;
            },
            search: function( event, ui ) {
                if (typeof _gaq != 'undefined') _gaq.push(['_trackEvent', 'Search', $('#get-artist').val() ]);
            },
            select: function( event, ui ) {
                location.href = ui.item.url;
                return false;
            }
         }).on('blur', function() {
            $(this).val('');
         });

        // focus on login form 
        $('#id_username').focus();
    }

    function _retinize() {
        // reload @2x images 
        if (_hdpi_enabled) {
            $('img.panel').each(function() {
                $(this).attr('src', $(this).attr('data-hd-src'));
            });
        }
    }

    function _resize() {
        var screen_width = document.documentElement.clientWidth;
        medium_width = screen_width <= 1020;
        small_width = screen_width <= 700;
        if (small_width) {
            $('#mobile-nav').show();
        } else {
            $('nav.main ul').show();
            $('#mobile-nav').hide();
        }
    }

    // public methods
    return {
        init: function() {
            _init();
        },
        retinize: function() {
            _retinize();
        },
        resize: function() {
            _resize();
        },
        hdpi_enabled: function() {
            return _hdpi_enabled;
        }
    };
})();

// fire up the mothership
$(window).ready(function(){
    $.corpsey.init();
});
$(window).load(function(){
    $.corpsey.retinize();
});
$(window).resize(function(){
    $.corpsey.resize();
});
