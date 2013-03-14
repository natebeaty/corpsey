$.corpsey = $.corpsey || {};

$.corpsey.contribute = (function() {
    var History;
    var State;
    var step_at;
    var comic_id;

    function _init() {
        // add .required to inputs
        $('label.required').each(function() {
            $('input#'+$(this).attr('for')).addClass('required');
        });

        History = window.History;
        State = History.getState();
        comic_id = $('.comic.single').attr('data-comic-id');

        History.replaceState({}, document.title, window.location.pathname );

        // bind to state change
        History.Adapter.bind(window,'statechange',function(){
            State = History.getState();
            _show_step();
        });

        $('.continue').click(function(e) {
            e.preventDefault();
            var url = $(this).attr('href');
            History.pushState({}, document.title, url);
        });

        $('.new-leaf').click(function(e) {
            e.preventDefault();
            comic_id = $('.comic.single').attr('data-comic-id');
            Dajaxice.corpsey.apps.comics.get_new_leaf($.corpsey.contribute.show_new_leaf, {
                'comic_id': comic_id,
                'hdpi_enabled': $.corpsey.hdpi_enabled()
            });
        });

        $('form.contribute').validate();
    }

    function _show_new_leaf(data) {
        var comic = ich.comic_single(data.comic);
        $('#parent_comic').empty().append(comic);
        $('#id_comic_id').val(data.comic.comic_id);
        comic_id = data.comic.comic_id;
        if (typeof _gaq != 'undefined') _gaq.push(['_trackEvent', 'Contribute', 'New Leaf']);
    }

    // public methods
    return {
        init: function() {
            _init();
        },
        show_new_leaf: function(data) {
            _show_new_leaf(data);
        }
    };
})();

// fire up the mothership
$(window).ready(function(){
    $.corpsey.contribute.init();
});
