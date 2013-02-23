// trubble club codes for pleasure

$.corpsey = (function() {
    var _hdpi_enabled;

    function _init() {
        _hdpi_enabled = (window.devicePixelRatio >= 2);

        // search-o-rama
        $('<li><input id="get-artist" placeholder="SEARCH"></li>').prependTo('nav.main ul');
        $('#get-artist').autocomplete({
			source: "/get_artists/",
			minLength: 2,
			select: function( event, ui ) {
				location.href = ui.item.url;
                return false;
			}
         }).on('blur', function() {
            $(this).val('');
         });
    }

    function _retinize() {
        if (_hdpi_enabled) {
            $('img.panel').each(function() {
                $(this).attr('src', $(this).attr('data-hd-src'));
            });
        }
    }

    // public methods
    return {
        init: function() {
            _init();
        },
        retinize: function() {
            _retinize();
        },
        hdpi_enabled: function() {
            return _hdpi_enabled;
        }
    };
})();

// fire up the mothership
$(window).ready(function(){
    $.corpsey.init();
});
$(window).load(function(){
    $.corpsey.retinize();
});
