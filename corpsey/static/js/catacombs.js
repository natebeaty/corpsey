$.corpsey = $.corpsey || {};

$.corpsey.catacombs = (function() {
    var History = window.History;
    var State = History.getState();
    var comics_showing = [];
    var comics_shown = [];

    var medium_width = false,
        small_width = false,
        delayed_resize_timer,
        build_titles_timer;

    function _init() {
        delayed_resize_timer = false;
        _get_widths();
        State = History.getState();

        _get_comics_showing();

        // init first strips as shown
        for(var i=0; i<comics_showing.length; i++) comics_shown[comics_showing[i]] = 1;

        History.replaceState({
            'direction': ''
            }, document.title, window.location.pathname );

        // bind to state change
        History.Adapter.bind(window,'statechange',function(){
            State = History.getState();
            _get_comics_showing();
            _build_panels();
        });

        // isotopize
        $('#catacombs').isotope({
            itemSelector: 'img,h1',
            onLayout: function() {
                if (build_titles_timer) { clearTimeout(build_titles_timer); }
                build_titles_timer = setTimeout(function() { $.corpsey.catacombs.build_titles(); }, 650);
            }
        });
        if (!small_width) {
            $('#catacombs').isotope({ filter: '.panel' });
        }

        $('.comic-nav .next, .comic-nav .prev').live('click',function(e) {
            e.preventDefault();

            if ($('.comic-nav').hasClass('loading')) { return false; }
            $('.comic-nav').addClass('loading');

            var direction = $(this).hasClass('next') ? 'next' : 'prev';
            var url = $(this).attr('href');
            History.pushState({'direction': direction}, document.title, url);

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

        _init_nav_waypoints();
    }

    // build id arr and convert to int
    function _get_comics_showing() {
        comics_showing = State.url.replace(location.host,'').match(/\d+/g);
        for(var i=0; i<comics_showing.length; i++) comics_showing[i] = +comics_showing[i];
    }

    function _init_nav_waypoints() {
        $('.comic-nav.next').waypoint(function(d) {
            $(this).toggleClass('stuck', d==='down');
        }, {
            offset: 200
        });
        $('.comic-nav.prev').waypoint(function(d) {
            $(this).toggleClass('stuck', d==='down');
        }, {
            offset: 40
        });
    }

    function _build_panels(){
        _hide_titles();
        
        // check for comic panels to load
        for(var i=0; i<comics_showing.length; i++) {
            if (!comics_shown[comics_showing[i]]) {
                Dajaxice.corpsey.apps.comics.get_comic_panels($.corpsey.catacombs.show_panels, {
                    'comic_id': comics_showing[i],
                    'direction': State.data.direction
                });
            } else {
                $('.comic.single[data-comic-id='+comics_showing[i]+']').show();
                _filter_panels();
            }
        }
    }

    function _show_panels(data) {

        // cache comic data
        comics_shown[data.comic.comic_id] = 1;

        // build from icanhaz template
        var comic = ich.comic_single(data.comic);

        // drop in comic
        if (data.direction==='next') {
            $('#catacombs').find('.comic.single:visible:last').after(comic);
        } else {
            $('#catacombs').find('.comic.single:visible:first').before(comic);
        }
        _filter_panels();
    }

    function _filter_panels() {
        $('#catacombs').isotope('reloadItems').isotope({ sortBy: 'original-order' });

        // filter strips not in new url
        var comics_to_show = $('#catacombs .comic.single').filter(function(){
            return ($.inArray($(this).data('comic-id'), comics_showing)<0);
        });

        comics_to_show.hide();
        $('#catacombs').isotope({ filter: '.comic.single:visible .panel,.comic.single:visible .h1' });

        _get_nav_links();
    }

    function _find_comic(id) {
        return $('#catacombs').find('.comic.single[data-comic-id='+id+']');
    }

    function _get_nav_links() {
        Dajaxice.corpsey.apps.comics.get_nav_links($.corpsey.catacombs.show_nav_links, { 'comic_id_arr': comics_showing });
    }

    function _show_nav_links(data) {
        $('.comic-nav').removeClass('stuck').waypoint('destroy');
        $('.comic-nav').remove();
        var nav;

        // any nav to add?
        if (data.next_comic_links.length>0) {
            nav = ich.next_comic_nav(data);
            $('#content').append(nav);
        } else if (data.up_comic_links) {
            nav = ich.up_comic_nav(data);
            $('#content').append(nav);
        }

        if (data.prev_comic_links.length>0) {
            nav = ich.prev_comic_nav(data);
            $('#content').append(nav);
        }

        _init_nav_waypoints();
    }

    function _hide_titles() {
        $('h1.comic_1, h1.comic_2').fadeOut();
    }
    function _build_titles() {
        $('h1.comic_1, h1.comic_2').remove();
        $('.comic.single:visible').each(function(i) {
            var name = $(this).find('h1').text();
            $('<h1 />').text(name).addClass('comic_'+(i+1)).appendTo('body').css({ 'top' : -1000, 'left' : -1000 });
        });
        _move_titles();
    }
    function _move_titles() {
        $('.comic.single:visible').each(function(i) {
            var c = (i===1 && $('#catacombs').width()<980) ? '1' : '0';
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
        if (!small_width) {
            $('#catacombs').isotope({ filter: '.panel' });
        } else {
            $('#catacombs').isotope({ filter: '.panel,h1' });
        }
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
        build_panels: function(data) {
            _build_panels(data);
        },
        show_panels: function(data) {
            _show_panels(data);
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

$(window).resize(function(){
    $.corpsey.catacombs.resize();

  // delayed resize for more intensive tasks
  if($.corpsey.catacombs.delayed_resize_timer !== false) {
    clearTimeout($.corpsey.catacombs.delayed_resize_timer);
  }
  $.corpsey.catacombs.delayed_resize_timer = setTimeout($.corpsey.catacombs.delayed_resize, 200);
});
