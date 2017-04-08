// Infinite Corpse js brains
// nate@clixel.com 2013

// @codekit-prepend "libs/jquery-3.2.0.js"
// @codekit-prepend "libs/jquery.lazyload.min.js"
// @codekit-prepend "libs/jquery.isotope.min.js"
// @codekit-prepend "bower_components/imagesloaded/imagesloaded.pkgd.js"
// @codekit-prepend "bower_components/icanhaz/ICanHaz.js"
// @codekit-prepend "bower_components/Sortable/Sortable.js"
// @codekit-prepend "bower_components/history.js/scripts/bundled-uncompressed/html5/jquery.history.js"
// @codekit-prepend "bower_components/jquery-validation/dist/jquery.validate.js"
// @codekit-prepend "bower_components/jquery.quicksearch/dist/jquery.quicksearch.js"

$.corpsey = (function() {
    var _hdpi_enabled,
        medium_width,
        small_width,
        _touch_enabled;

    function _init() {
        // Are we on a retina display?
        _hdpi_enabled = (window.devicePixelRatio >= 2);
        _touch_enabled = ('ontouchstart' in window);
        $('html').toggleClass('no-touchevents', !_touch_enabled);

        // Get screen width and roll up nav if mobile
        _resize();
        if (small_width) {
            $('nav.main ul').hide();
        }

        $('<a id="mobile-nav" />').appendTo('body').click(function() {
            $('nav.main ul').slideToggle('fast');
        });

        // Focus on login form if present
        $('#id_username').focus();

        // Homepage
        if ($('body#homepage').length) {
            // Scroll down to recent contributors from homepage button
            $('li.recent a').click(function() {
                $('html,body').animate({scrollTop:$('#recent-contributors').offset().top }, 'fast');
                return false;
            });

            _initLazyLoad();
            _initLoadMore();
        }

        // Artist page
        if ($('body#artists').length) {
            // Kill form submit that we don't really need (just quicksearch)
            $('.artist-search').on('submit', function(e) {
                e.preventDefault();
            }).find('input[name="term"]').focus();
            // Add "no results" li for quicksearch
            $('<li class="no-results hidden">None found.</li>').appendTo('.artists-list ul');
            $(document).on('keydown',function(e) {
                // Escape clears out search
                if (e.keyCode === 27) {
                    $('.artist-search input[name="term"]').val('');
                }
            });
            _initQuickSearch();

        }

    }

    // Quick resize functions
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

    // Init Lazyload images
    function _initLazyLoad() {
        $('img.panel').lazyload({
            threshold: 250,
            hidpi_support: true
        });
    }

    // Quick search on top of /artists/ page
    function _initQuickSearch() {
        $('.artist-search input[name="term"]').quicksearch('.artists-list ul li:not(.letter)', {
            onAfter: function () {
                $('.artists-list').toggleClass('searching', $('.artist-search input[name="term"]').val()!=='');
            },
            noResults: '.no-results'
        });
    }

    // Load More handler
    function _initLoadMore() {
      $(document).on('click', '.load-more a', function(e) {
        e.preventDefault();
        var $load_more = $(this).closest('.load-more'),
            page = parseInt($load_more.attr('data-page-at')),
            per_page = parseInt($load_more.attr('data-per-page')),
            $more_container = $load_more.parents('section,main').find('.load-more-container');

        $.ajax({
            url: '/ajax/load_more/',
            method: 'get',
            data: {
                page: page+1,
                per_page: per_page
            },
            success: function(data) {
              $more_container.append(data);
              $load_more.attr('data-page-at', page+1);
              $.corpsey.checkLoadMore();
              _initLazyLoad();
              $(window).trigger('scroll');
            }
        });
      });
    }

    // Hide "Load More" if there are no more pages
    function _checkLoadMore() {
      $('.load-more').toggleClass('hide', parseInt($('.load-more').attr('data-page-at')) >= parseInt($('.load-more').attr('data-total-pages')));
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
        checkLoadMore: _checkLoadMore,
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
