$.corpsey = $.corpsey || {};

$.corpsey.catacombs = (function() {

    function _init() {
        var History = window.History;
        var State = History.getState();

        // Log Initial State
        History.log('initial:', State.data, State.title, State.url);

        // Bind to State Change
        History.Adapter.bind(window,'statechange',function(){
            var State = History.getState();
            History.log('statechange:', State.data, State.title, State.url);
        });

        // isotopize
        // $('#catacombs').isotope({
        //     itemSelector: 'li'
        // });

        $('.next-comic .button').live('click',function(e) {
            e.preventDefault();
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
        // $('#catacombs').isotope('insert', comic);
        // any nav to add?
        if (data.comic_links.length>0) {
            var nav = ich.comic_nav(data);
            $('#catacombs').append(nav);
        } else {

        }
        _move_titles();
    }

    function _move_titles() {
        $('.comic.single:even').each(function() {
            var pos = $(this).offset();
            var width = $(this).width();
            $(this).find('h1').css({'top' : pos.top-380});
        });
        $('.comic.single:odd').each(function() {
            var pos = $(this).offset();
            var width = $(this).width();
            // console.log(pos.left,width);
            $(this).find('h1').css({'top' : pos.top+240,'left' : pos.left});
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

$(window).resize(function(){
    $.corpsey.catacombs.move_titles();
});
