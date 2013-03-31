// Infinite Corpse js brains for reserving a spot to contribute
// nate beaty @ clixel 2013

$.corpsey = $.corpsey || {};

$.corpsey.contribute = (function() {
    var comic_id;

    function _init() {
        // add .required to inputs
        $('label.required').each(function() {
            $('input#'+$(this).attr('for')).addClass('required');
        });

        // open links in new window (halftones, pg-13)
        $('.user-content a').attr('target','_blank');

        comic_id = $('.comic.single').attr('data-comic-id');

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
