// Infinite Corpse js brains for catacombs
// nate beaty @ clixel 2013

$.corpsey = $.corpsey || {};

$.corpsey.catacombs = (function() {
    var History = window.History;
    var State = History.getState();
    var comics_showing = [];
    var comics_shown = [];
    var max_comics_loaded = 15;
    var uturns_shown = [];
    var is_uturn = false; // true when on a uturn page
    var uturn_single = false; // true when /uturn/x/

    var medium_width = false,
        small_width = false,
        delayed_resize_timer = false,
        build_titles_timer;

    function _init() {
        // get initial screen width
        _get_widths();
        State = History.getState();
        _get_comics_showing();

        // init first strips as shown
        if (is_uturn) {
            uturns_shown.push(comics_showing[0]);
            $('.comic.single:not(.uturn)').each(function() {
                comics_shown.push($(this).attr('data-comic-id'));
            });
        } else {
            for(var i=0; i<comics_showing.length; i++) {
                comics_shown.push(comics_showing[i]);
            }
        }

        History.replaceState({
            'direction': ''
            }, document.title, window.location.pathname );

        // bind to state change
        History.Adapter.bind(window,'statechange',function(){
            State = History.getState();
            _get_comics_showing();
            _garbage_collection();
            _build_panels();
            if (typeof _gaq != 'undefined') _gaq.push(['_trackPageview', window.location.pathname]);
        });

        // isotopize
        $('#catacombs').isotope({
            itemSelector: 'img,h1',
            onLayout: function() {
                if (build_titles_timer) { clearTimeout(build_titles_timer); }
                build_titles_timer = setTimeout(function() { $.corpsey.catacombs.build_titles(); }, 450);
            }
        });
        setTimeout(function() {
            $('#catacombs').isotope({ filter: (small_width) ? '.comic.active .panel:not(.uturn-pad),.comic.active h1' : (medium_width) ? '.comic.active .panel:not(.uturn-pad)' : '.comic.active .panel' });
        }, 250);

        $('.comic-nav .next, .comic-nav .prev').live('click',function(e) {
            e.preventDefault();

            if ($('.comic-nav').hasClass('loading')) { return false; }
            $('.comic-nav').addClass('loading');

            var direction = $(this).hasClass('next') ? 'next' : 'prev';
            var url = $(this).attr('href');
            var title = $(this).attr('title')+' : The Infinite Corpse';
            History.pushState({'direction': direction}, title, url);

            return false;
        });

        $('.comic-nav .up').live('click', function(e) {
            e.preventDefault();

            if ($('.comic-nav').hasClass('loading')) { return false; }
            $('.comic-nav').addClass('loading');

            History.back();
            return false;
        });

        // keyboard nerds
        $(document).bind('keydown',function(e) {
            if (e.keyCode === 39) {
              $('.next.button:first').trigger('click');
              e.preventDefault();
            } else if (e.keyCode === 37) {
              $('.prev.button:first').trigger('click');
              e.preventDefault();
            }
        });

        // init isotope filter based on window size
        _delayed_resize();
    }

    function _get_comics_showing() {
        // get comic_id array from URL
        comics_showing = State.url.replace(location.host,'').match(/\d+/g);
        
        // build id arr and convert to int
        for(var i=0; i<comics_showing.length; i++) comics_showing[i] = +comics_showing[i];

        // is this a uturn page?
        is_uturn = State.url.match(/uturn/);

        // for /catacombs/uturn/5/ URLs
        if (is_uturn && comics_showing.length==1) {
            comics_showing[1] = +$('.comic.uturn.active').attr('data-portal-to-id');
            uturn_single = true;
        } else {
            uturn_single = false;
        }

        // add class .one-comic-showing to adjust min-height
        $('#catacombs').toggleClass('one-comic-showing', (comics_showing.length===1));

        // add .is-uturn class for small.less to shorten min-height
        $('#catacombs').toggleClass('is-uturn', (is_uturn!==null));
    }

    // try to keep memory use not insane (was getting up to 900mb for one tab)
    function _garbage_collection() {
        // remove first comic if we've shown more than max_comics_loaded
        if (comics_shown.length > max_comics_loaded) {
            $('.comic.single:not(.uturn)[data-comic-id='+comics_shown[0]+']').remove();
            comics_shown.shift();
        }
    }

    function _build_panels(){
        _hide_titles();
        
        // check for comic panels to load
        for(var i=0; i<comics_showing.length; i++) {
            if (is_uturn && (i===0 && !uturns_shown[comics_showing[i]])) {
                Dajaxice.corpsey.apps.comics.get_uturn_panel($.corpsey.catacombs.show_uturn, {
                    'uturn_id': comics_showing[i],
                    'direction': State.data.direction,
                    'hdpi_enabled': $.corpsey.hdpi_enabled()
                });
            } else if (
                // motherfucking uturns breaking my brain
                (is_uturn && i===1 && comics_shown.indexOf(comics_showing[i]) < 0) || 
                (!is_uturn && comics_shown.indexOf(comics_showing[i]) < 0)
            ){
                Dajaxice.corpsey.apps.comics.get_comic_panels($.corpsey.catacombs.show_panels, {
                    'comic_id': comics_showing[i],
                    'direction': State.data.direction,
                    'hdpi_enabled': $.corpsey.hdpi_enabled()
                });
            } else {
                $('.comic.single[data-comic-id='+comics_showing[i]+']').addClass('active');
                _filter_panels();
            }
        }
    }

    function _show_uturn(data) {
        // cache uturn data
        uturns_shown[data.uturn.uturn_id] = 1;
        
        // build from icanhaz template
        var uturn = ich.uturn_single(data.uturn);
        
        // uturn is only ever from Next
        $('#catacombs').isotope('insert', uturn);

        _filter_panels();
    }

    function _show_panels(data) {
        // cache comic data
        if(comics_shown.indexOf(data.comic.comic_id) < 0) {
            comics_shown.push(data.comic.comic_id);
        }

        // build from icanhaz template
        var comic = ich.comic_single(data.comic);

        // show loading status
        comic.find('img').addClass('loading').imagesLoaded(function($imgs) {
            $imgs.removeClass('loading');
        });

        // drop in comic
        if (data.direction==='next') {
            $('#catacombs').isotope('insert', comic);
        } else {
            $('#catacombs').find('.comic.single.active:first').before(comic);
        }
        _filter_panels();
    }

    function _filter_panels() {
        // i do this a lot. todo: clean this up
        _get_comics_showing();

        var visible_comics = [];
        $('.comic.single.active').each(function() { 
            var id = $(this).data('comic-id');
            // somehow comics are duplicating sometimes?
            if ($.inArray(id,visible_comics)>-1 && !$(this).hasClass('uturn')) {
                $(this).remove();
            } else {
                visible_comics.push(id); 
            }
        });

        // if you've looped through from last comic to first comic, make sure the URL matches visible order of comics
        // or if uturn and we're out of sync, swap em around!
        if ((!is_uturn && visible_comics[0]!=comics_showing[0]) ||
            (is_uturn && uturn_single && visible_comics[0]!=comics_showing[0])
            ) {
            $('.comic.active[data-comic-id='+comics_showing[0]+']:first').after($('.comic.active[data-comic-id='+comics_showing[1]+']:first'));
        } else if (is_uturn && !uturn_single && visible_comics[0]==comics_showing[0]) {
            $('.comic.active[data-comic-id='+comics_showing[1]+']:first').after($('.comic.active[data-comic-id='+comics_showing[0]+']:first'));
        }

        // reset sort order for isotope using DOM order
        $('#catacombs').isotope('reloadItems').isotope({ sortBy: 'original-order' });

        // hide strips not in new url
        $('#catacombs .comic.single').each(function(){
            // uturn pages have different 
            if (is_uturn) {
                if (
                    ($(this).hasClass('uturn') && $(this).data('comic-id')!=comics_showing[0]) || 
                    (!$(this).hasClass('uturn') && $(this).data('comic-id')!=comics_showing[1]))
                    {
                        $(this).removeClass('active');
                    }
            } else {
                if ($(this).hasClass('uturn') || $.inArray($(this).data('comic-id'), comics_showing)<0) {
                    $(this).removeClass('active');
                }
            }
        });

        // set isotope to filter visible comics
        $('#catacombs').isotope({ filter: (small_width) ? '.comic.active .panel:not(.uturn-pad),.comic.active h1' : (medium_width) ? '.comic.active .panel:not(.uturn-pad)' : '.comic.active .panel' });

        // if med/small screen, scroll up to comic we just loaded
        if (medium_width || small_width) {
            if (State.data.direction=='next') {
                var scrollTo = small_width ? 960 : 320;
                // for small_width single uturns (only has single first TC panel, scroll to panel 2 on page)
                if (small_width && is_uturn && uturn_single) {
                    scrollTo = 340;
                }
                setTimeout(function() {
                    $('html,body').animate({ scrollTop: scrollTo });
                }, 250);
            } else {
                setTimeout(function() {
                    $('html,body').animate({ scrollTop: small_width ? 40 : 30 });
                }, 250);
            }
        }

        _get_comics_showing();
        _get_nav_links();
    }

    function _get_nav_links() {
        Dajaxice.corpsey.apps.comics.get_nav_links($.corpsey.catacombs.show_nav_links, { 'comic_id_arr': comics_showing, 'is_uturn': is_uturn });
    }

    function _show_nav_links(data) {
        $('.comic-nav').remove();
        var nav;
        // any nav to add?
        if (data.next_comic_links.length>0) {
            nav = ich.next_comic_nav(data);
            $('#content').append(nav);
        } else if (data.uturn_links.length>0) {
            nav = ich.uturn_nav(data.uturn_links[0]);
            $('#content').append(nav);
        }

        if (data.prev_comic_links.length>0) {
            nav = ich.prev_comic_nav(data);
            $('#content').append(nav);
        }
    }

    function _hide_titles() {
        $('h1.comic_1, h1.comic_2').fadeOut();
    }

    function _build_titles() {
        $('h1.comic_1, h1.comic_2').remove();
        $('.comic.single.active').each(function(i) {
            var name = $(this).find('h1').html();
            $('<h1 />').html(name).addClass('comic_'+(i+1)).appendTo('body').css({ 'top' : -1000 });
        });
        _move_titles();
    }

    function _move_titles() {
        $('.comic.single.active').each(function(i) {
            // figure out which comic panel to position next to
            var c = (i===1 && $('#catacombs').width()<980) ? '1' : '0';
            // todo: put this damn title to the right of the strip, ugh
            if (is_uturn && $(this).hasClass('uturn') && $('#catacombs').width()<980) c = '1';
            var $img = $(this).find('img:eq('+c+')');
            var pos = $img.offset();
            var $h1 = $('h1.comic_'+(i+1));
            if ($h1.length>0 && pos!==null) {
                $h1.css({ 'top' : pos.top+$h1.width(), 'left' : pos.left-20 });
            }
        });
        $('h1.comic_1, h1.comic_2').show();
    }

    function _resize() {
        _get_widths();
        _move_titles();
    }

    function _delayed_resize() {
        $('#catacombs').isotope({ filter: (small_width) ? '.comic.active .panel:not(.uturn-pad),.comic.active h1' : (medium_width) ? '.comic.active .panel:not(.uturn-pad)' : '.comic.active .panel' });
    }

    function _get_widths() {
        var screen_width = document.documentElement.clientWidth;
        medium_width = screen_width <= 1020;
        small_width = screen_width <= 700;
    }

    // public methods
    return {
        init: function() {
            _init();
        },
        show_panels: function(data) {
            _show_panels(data);
        },
        show_uturn: function(data) {
            _show_uturn(data);
        },
        resize: function() {
            _resize();
        },
        delayed_resize: function() {
          _delayed_resize();
        },
        build_titles: function() {
            _build_titles();
        },
        show_nav_links: function(data) {
            _show_nav_links(data);
        }
    };
})();

// fire up the mothership
$(window).ready(function(){
    $.corpsey.catacombs.init();
});

// adjust to mothership size variations
$(window).resize(function(){
    $.corpsey.catacombs.resize();

  // delayed resize for more intensive tasks
  if($.corpsey.catacombs.delayed_resize_timer !== false) {
    clearTimeout($.corpsey.catacombs.delayed_resize_timer);
  }
  $.corpsey.catacombs.delayed_resize_timer = setTimeout($.corpsey.catacombs.delayed_resize, 200);
});
