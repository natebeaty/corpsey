$.corpsey = $.corpsey || {};

$.corpsey.catacombs = (function() {

    function _init() {
        var History = window.History;
        // var State = History.getState();

        // Log Initial State
        // History.log('initial:', State.data, State.title, State.url);

        // Bind to State Change
        History.Adapter.bind(window,'statechange',function(){
            // var State = History.getState();
            // History.log('statechange:', State.data, State.title, State.url);
        });

        // isotopize
        $('#catacombs').isotope({
            itemSelector: 'img',
            onLayout: $.corpsey.catacombs.build_titles
        });

        $('.comic-nav .button').live('click',function(e) {
            e.preventDefault();
            if ($('.comic-nav').hasClass('loading') || $(this).hasClass('up')) {
                return false;
            }
            $("html, body").animate({ scrollTop: 0 }, "fast");

            $('.comic-nav').addClass('loading');
            var comic_id = $(this).data('comic-id');
            var direction = $(this).hasClass('next') ? 'next' : 'prev';
            History.pushState(null, null, '/catacombs/'+comic_id+'/'); // '/catacombs/'+comic_id+'/'
            Dajaxice.corpsey.apps.comics.get_comic_panels($.corpsey.catacombs.build_panels, { 'comic_id': comic_id, 'direction': direction });
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

        // build comic template with data
        var comic = ich.comic_single(data);
        
        // remove first comic if viewing two already
        if ($('.comic.single').length > 1) {
            var comicToRemove = data.direction==='next' ? $('.comic.single:first') : $('.comic.single:last');
            var imgs = comicToRemove.find('img');
            $('#catacombs').isotope('remove', imgs, function() {
                comicToRemove.remove();
                _show_panels(data, comic);
            });
        } else {
            _show_panels(data, comic);
        }
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

    function _up_link() {
        var imgs = $('.comic.single:last img');
        $('#catacombs').isotope('remove', imgs, function() {
            $('.comic.single:last').remove();
            _get_nav_buttons();
        });
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
        up_link: function() {
            _up_link();
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
