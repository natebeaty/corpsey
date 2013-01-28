$.corpsey = $.corpsey || {};

$.corpsey.catacombs = (function() {

    function _init() {
        var History = window.History;
        var State = History.getState();

        // Log Initial State
        // History.log('initial:', State.data, State.title, State.url);

        // Bind to State Change
        History.Adapter.bind(window,'statechange',function(){
            var State = History.getState();
            // History.log('statechange:', State.data, State.title, State.url);
        });

        // isotopize
        // $('#catacombs').isotope({
        //     itemSelector: 'li'
        // });

        $('.next-comic .button').live('click',function(e) {
            e.preventDefault();
            $('.next-comic').css('opacity',.5);
            var comic_id = $(this).data('comic-id');
            History.pushState(null, null, '/catacombs/'+comic_id+'/'); // '/catacombs/'+comic_id+'/'
            Dajaxice.corpsey.apps.comics.get_comic_panels($.corpsey.catacombs.draw_panels, { 'comic_id': comic_id });
            return false;
        });
    }

    function _draw_panels(data){
        // build comic icanhaz template
        var comic = ich.comic_single(data);
        
        // clear out nav
        $('.next-comic-nav').remove();

        // drop in comic
        $('#catacombs').append(comic);

        comic.find('img').each(function(i,el) {
            $(this).hide().fadeIn(1000*(i+1), function() {
                if (i==1) {
                    $('#catacombs').imagesLoaded(function() {
                        _move_titles();
                    });
                }
            });
        });
        // $('#catacombs').isotope('insert', comic);
        
        // any nav to add?
        if (data.comic_links.length>0) {
            var nav = ich.comic_nav(data);
            $('#catacombs').append(nav);
            $('.next-comic').animate({'opacity':1});
        } else {

        }
        _show_active_comics();
    }


    function _show_active_comics() {
        $('ul.tree li').removeClass('active');
        $('.comic.single').each(function() {
            var id = $(this).data('comic-id');
            $('ul.tree li[data-comic-id='+id+']').addClass('active');
        });
    }

    function _move_titles() {
        $('.comic.single:even').each(function() {
            var $img = $(this).find('img:first');
            var pos = $img.position();
            $(this).find('h1').css({'top' : pos.top+20 });
        });
        $('.comic.single:odd').each(function() {
            var $img = $(this).find('img:last');
            var pos = $img.position();
            $(this).find('h1').css({'top' : pos.top + $img.height()-130 ,'left' : pos.left + $img.width()+20 });
        });
    }

    // public methods
    return {
        init: function() {
            _init();
        },
        draw_panels: function(data) {
            _draw_panels(data);
        },
        move_titles: function(data) {
            _move_titles(data);
        }
    };
})();

// fire up the mothership
$(window).ready(function(){
    $.corpsey.catacombs.init();
});

$(window).load(function(){
    $('#catacombs').imagesLoaded(function() {
       $.corpsey.catacombs.move_titles(); 
    });
});

$(window).resize(function(){
    $.corpsey.catacombs.move_titles();
});
