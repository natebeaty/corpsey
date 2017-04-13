// Infinite Corpse js brains
// nate@clixel.com 2013

// @codekit-prepend "../bower_components/jquery/dist/jquery.js"
// @codekit-prepend "../bower_components/Sortable/Sortable.js"
// @codekit-prepend "../bower_components/history.js/scripts/bundled-uncompressed/html5/jquery.history.js"
// #codekit-prepend "../bower_components/isotope/dist/isotope.pkgd.js"
// @codekit-prepend "libs/jquery.isotope.min.js"
// @codekit-prepend "../bower_components/jquery-validation/dist/jquery.validate.js"
// @codekit-prepend "../bower_components/jquery.quicksearch/dist/jquery.quicksearch.js"
// @codekit-prepend "../bower_components/vanilla-lazyload/dist/lazyload.transpiled.js"
// @codekit-prepend "../bower_components/mustache.js/mustache.js"


$.corpsey = (function() {
    var lazyloader,
        medium_width,
        small_width,
        _touch_enabled,
        _mustache_templates = [];

    function _init() {
        _touch_enabled = ('ontouchstart' in window);
        $('html').toggleClass('no-touchevents', !_touch_enabled);

        Mustache.escape = function(value){ return value; };

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

        // Lazyload images
        _initLazyLoad();

        // Homepage
        if ($('body#homepage').length) {
            // Scroll down to recent contributors from homepage button
            $('li.recent a').click(function() {
                $('html,body').animate({scrollTop:$('#recent-contributors').offset().top }, 'fast');
                return false;
            });
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
        if (typeof LazyLoad !== 'undefined') {
            lazyloader = new LazyLoad({
              threshold: 250,
              elements_selector: 'img.panel',
              callback_load: function(el) {
                // Add class to wrap to remove loading display
                $(el).parents('.panel-wrap').addClass('loaded');
              }
            });
        }
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
              lazyloader.update();
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
    function _render_template(template, data) {
        if (!_mustache_templates[template]) {
            var t = $('#' + template).html();
            Mustache.parse(t); // optional, speeds up future uses
            _mustache_templates[template] = t;
        }
        return Mustache.render(_mustache_templates[template], data);
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
        render_template: function(template, data) {
            return _render_template(template, data);
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
