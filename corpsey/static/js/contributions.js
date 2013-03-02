$.corpsey = $.corpsey || {};

$.corpsey.contributions = (function() {

    function _init() {
        var rule_broke = 0;
        $('.button').click(function(e) {
            e.preventDefault();
            var $queue = $(this).parents('.queue:first');
            if (!$queue.hasClass('voted')){
                var yea = $(this).text()=='Yea' ? 1 : 0;
                var contribution_id = $queue.attr('data-contribution-id');
                Dajaxice.corpsey.apps.comics.contribution_vote($.corpsey.contributions.after_vote, {
                    'contribution_id': contribution_id,
                    'yea': yea,
                    'rule_broke': rule_broke
                });
            }
        });
    } // end _init()

    function _after_vote(data) {
        console.log(data);
        $('.queue[data-contribution-id='+data.contribution_id+']').addClass('voted').toggleClass('yea',data.yea==1).toggleClass('nay',data.yea==0).find('.actions').slideUp();
    }

    // public methods
    return {
        init: function() {
            _init();
        },
        after_vote: function(contribution_id,yea) {
            _after_vote(contribution_id,yea);
        }
    };
})();

// fire up the mothership
$(window).ready(function(){
    $.corpsey.contributions.init();
});
