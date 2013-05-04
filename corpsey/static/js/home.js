// Infinite Corpse js brains for homepage
// nate beaty @ clixel 2013

$.corpsey = $.corpsey || {};

$.corpsey.home = (function() {

    function _init() {
        var isiPad = navigator.userAgent.match(/iPad/i) != null;

        // scroll down to recent contributors from homepage button
        $('li.recent a').click(function() {
            $('html,body').animate({scrollTop:$('#recent-contributors').offset().top }, 'fast');
            return false;
        });

        // lazy load for everything but ipad
        $("img.panel").lazyload({
            threshold: (isiPad) ? 99999 : 200,
            hidpi_support: true
        });
    }

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
