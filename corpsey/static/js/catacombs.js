$.corpsey = $.corpsey || {};

$.corpsey.catacombs = (function() {
    var History = window.History;
    var State = History.getState();
    var comics_showing = [];
    var comics_data = {};

    function _init() {
        State = History.getState();
        comics_showing = _comics_showing();
        History.replaceState({'hash': window.location.pathname, 'direction': '', 'comic_id': comics_showing[0]}, document.title, window.location.pathname);

        // Bind to State Change
        History.Adapter.bind(window,'statechange',function(){
            State = History.getState();
            // console.log(State.data, State.title, State.url, State.internal);
            if (!comics_data[State.data.hash]) {
                Dajaxice.corpsey.apps.comics.get_comic_panels($.corpsey.catacombs.build_panels, { 'comic_id': State.data.comic_id, 'direction': State.data.direction, 'hash': State.data.hash });
            } else {
                _build_panels(comics_data[State.data.hash], State.data.hash);
            }
        });

        // isotopize
        $('#catacombs').isotope({
            itemSelector: 'img',
            onLayout: function() { setTimeout(function() { $.corpsey.catacombs.build_titles(); }, 600); }
        });

        $('.comic-nav .next, .comic-nav .prev').live('click',function(e) {
            comics_showing = _comics_showing();
            e.preventDefault();
            if ($('.comic-nav').hasClass('loading')) {
                return false;
            }
            $("html, body").animate({ scrollTop: 0 }, "fast");

            $('.comic-nav').addClass('loading');
            var comic_id = $(this).data('comic-id');
            var direction = $(this).hasClass('next') ? 'next' : 'prev';
            var url = (direction==='next') ? '/catacombs/'+(comics_showing.length>1 ? comics_showing[1] : comics_showing[0])+'/'+comic_id+'/' : '/catacombs/'+comic_id+'/'+comics_showing[0]+'/';
            History.pushState({'hash': url+direction, 'comic_id': comic_id, 'direction': direction}, document.title, url);

            return false;
        });

        $('.comic-nav .up').live('click', function(e) {
            e.preventDefault();
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

        // check url for /3/4/
        var two_comics = History.getState().url.match(/\/\d+\/\d+\//);

        // build comic template with data
        var comic = ich.comic_single(data);
        
        // remove first comic if viewing two already
        if ($('.comic.single').length > 1) {
            if (!two_comics) {
                $('#catacombs').isotope('remove', $('.comic.single[data-comic-id!='+data.comic_id+']').find('img'));
                return false;
            } else {
                var comicToRemove = data.direction==='next' ? $('.comic.single:first') : $('.comic.single:last');
                var imgs = comicToRemove.find('img');
                $('#catacombs').isotope('remove', imgs, function() {
                    comicToRemove.remove();
                    _show_panels(data, comic);
                });
            }
        } else {
            _show_panels(data, comic);
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

        _show_active_comics_in_tree();
        _get_nav_buttons();

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

    function _get_nav_buttons() {
        var comic_id = $('.comic.single:first').data('comic-id');
        var comic_id_2 = $('.comic.single:last').data('comic-id');
        Dajaxice.corpsey.apps.comics.get_nav_links($.corpsey.catacombs.show_nav_buttons, { 'comic_id': comic_id, 'comic_id_2': comic_id_2 });
    }

    function _show_nav_buttons(data) {
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
        $('.comic.single h1, h1.comic_1, h1.comic_2').fadeOut();
    }
    function _build_titles() {
        $('h1.comic_1, h1.comic_2').remove();
        $('.comic.single').each(function(i) {
            $(this).find('h1').clone().addClass('comic_'+(i+1)).appendTo('body').css({ 'top' : -1000, 'left' : -1000 });
        });
        _move_titles();
    }
    function _move_titles() {
        $('.comic.single').each(function(i) {
            var c = (i===1 && $('#catacombs').width()<980) ? '1' : '0';
            var $img = $(this).find('img:eq('+c+')');
            var pos = $img.offset();
            var $h1 = $('h1.comic_'+(i+1));
            $h1.css({ 'top' : pos.top+$h1.width(), 'left' : pos.left-20 });
        });
        $('h1.comic_1, h1.comic_2').show();
    }

    // public methods
    return {
        init: function() {
            _init();
        },
        build_panels: function(data) {
            _build_panels(data);
        },
        move_titles: function() {
            _move_titles();
        },
        build_titles: function() {
            _build_titles();
        },
        show_nav_buttons: function(data) {
            _show_nav_buttons(data);
        }
    };
})();

// fire up the mothership
$(window).ready(function(){
    $.corpsey.catacombs.init();
});

$(window).load(function(){
    $('#catacombs').imagesLoaded(function() {
       $.corpsey.catacombs.build_titles();
    });
});

$(window).resize(function(){
    $.corpsey.catacombs.move_titles();
});
