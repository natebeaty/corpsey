$.corpsey = $.corpsey || {};

$.corpsey.home = (function() {

    function _init() {
        $('.comic').each(function(i) {
            var dim = '.'+(100-((i+1)*4));
            $(this).data('dim', dim).find('img').css('opacity', dim);
            $(this).on('mouseover', function() {
                $(this).find('img').stop().animate({'opacity': 1});
            }).on('mouseout', function() {
                $(this).find('img').stop().animate({'opacity': $(this).data('dim')});
            });
        });
    } // end _init()

    // public methods
    return {
        init: function() {
            _init();
        }
    };
})();

// fire up the mothership
$(window).ready(function(){
    $.corpsey.home.init();
});
