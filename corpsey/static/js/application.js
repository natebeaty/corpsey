// trubble club codes for pleasure

$.corpsey = (function() {

    function _init() {
        $('<li><input id="get-artist" placeholder="SEARCH"></li>').prependTo('nav.main ul');
        $('#get-artist').autocomplete({
			source: "/get_artists/",
			minLength: 2,
			select: function( event, ui ) {
				location.href = ui.item.url;
			}
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
    $.corpsey.init();
});
