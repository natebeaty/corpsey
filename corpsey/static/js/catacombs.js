$.corpsey = $.corpsey || {};

$.corpsey.catacombs = (function() {
    var History = window.History;
    var State = History.getState();
    var comics_showing = [];
    var comics_data = {};

    var medium_width = false,
        small_width = false,
        delayed_resize_timer,
        build_titles_timer;

    function _init() {
        delayed_resize_timer = false;
        _get_widths();
        State = History.getState();
        comics_showing = _comics_showing();
        History.replaceState({'hash': window.location.pathname, 'direction': 'prev', 'comic_id_arr': comics_showing}, document.title, window.location.pathname);

        // bind to state change
        History.Adapter.bind(window,'statechange',function(){
            State = History.getState();
            if (!comics_data[State.data.hash]) {
                Dajaxice.corpsey.apps.comics.get_comic_panels($.corpsey.catacombs.build_panels, { 'comic_id_arr': State.data.comic_id_arr, 'direction': State.data.direction, 'hash': State.data.hash });
            } else {
                // update the direction
                comics_data[State.data.hash].direction = State.data.direction;
                _build_panels(comics_data[State.data.hash]);
            }
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

            $("html, body").animate({ scrollTop: 0 }, "fast");

            var direction = $(this).hasClass('next') ? 'next' : 'prev';
            var url = $(this).attr('href');
            var comic_id_arr = url.match(/\d+/g);
            History.pushState({'hash': url, 'comic_id_arr': comic_id_arr, 'direction': direction}, document.title, url);

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

    function _build_panels(data){
        _hide_titles();
        var comic_id_arr = History.getState().url.replace(location.host,'').match(/\d+/g);

        // remove strips not in new url
        $('.comic.single').each(function() {
            var $this = $(this);
            if ($.inArray($this.data('comic-id').toString(), comic_id_arr)<0) {
                $('#catacombs').isotope('remove', $this.find('img,h1'), function() {
                    $this.remove();
                });
            }
        });

        if (comic_id_arr.length>1) {
            // build comic template with data
            var comic = ich.comic_single(data.comics[data.direction==='next' ? 1 : 0]);
            setTimeout(function() { _show_panels(data, comic); }, 650);
        }

        comics_data[data.hash] = data;
    }

    function _show_panels(data, comic) {
        // drop in comic
        if (data.direction==='next') {
            $('#catacombs').isotope('insert', comic);
        } else {
            $('#catacombs').prepend(comic).isotope('reloadItems').isotope({ sortBy: 'original-order' });
        }

        // _show_active_comics_in_tree();
        _get_nav_links();

        // var url = (comic_ids.length>1) ? '/catacombs/'+comic_ids[0]+'/'+comic_ids[1]+'/' : '/catacombs/'+comic_ids[0]+'/';
        // var title;
    }

    function _comics_showing() {
        var comic_ids = [];
        $('.comic.single').each(function() {
            comic_ids.push($(this).data('comic-id'));
        });
        return comic_ids;
    }

    function _get_nav_links() {
        comics_showing = _comics_showing();
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

    function _show_active_comics_in_tree() {
        $('ul.tree li').removeClass('active');
        $('.comic.single').each(function() {
            var id = $(this).data('comic-id');
            $('ul.tree li[data-comic-id='+id+']').addClass('active');
        });
    }

    function _hide_titles() {
        $('h1.comic_1, h1.comic_2').fadeOut();
    }
    function _build_titles() {
        $('h1.comic_1, h1.comic_2').remove();
        $('.comic.single').each(function(i) {
            var name = $(this).find('h1').text();
            $('<h1 />').text(name).addClass('comic_'+(i+1)).appendTo('body').css({ 'top' : -1000, 'left' : -1000 });
        });
        _move_titles();
    }
    function _move_titles() {
        $('.comic.single').each(function(i) {
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
