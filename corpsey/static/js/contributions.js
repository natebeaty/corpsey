// Infinite Corpse js brains for voting on contributions
// nate beaty @ clixel 2013

$.corpsey = $.corpsey || {};

$.corpsey.contributions = (function() {
    function _init() {
        $('.button.yea').click(function(e) {
            e.preventDefault();
            var $queue = $(this).parents('.queue:first');
            var contribution_id = $queue.attr('data-contribution-id');
            Dajaxice.corpsey.apps.comics.contribution_vote($.corpsey.contributions.after_vote, {
                'contribution_id': contribution_id, 
                'yea': 1
            });
            return false;
        });
        $('.button.nay').click(function(e) {
            e.preventDefault();
            $('#rules').hide().appendTo($(this).parents('.actions:first')).slideDown();
            return false;
        });
        $('.button.rule').click(function(e) {
            e.preventDefault();
            var rule_broke = 0;
            var notes = '';

            var $queue = $(this).parents('.queue:first');
            var contribution_id = $queue.attr('data-contribution-id');

            if ($(this).hasClass('other')) {
                notes = $('#notes').val();
                if (notes=='') {
                    alert('Please enter a reason for Other!');
                    return false;
                }
            } else {
                rule_broke = $(this).attr('data-rule-id');
            }
            Dajaxice.corpsey.apps.comics.contribution_vote($.corpsey.contributions.after_vote, {
                'contribution_id': contribution_id, 
                'yea': 0,
                'rule_broke': rule_broke,
                'notes': notes
            });
            return false;
        });
    } // end _init()

    function _after_vote(data) {
        // console.log(data);
        if (data.message!='') {
            alert(data.message);
        }
        $('#rules').slideUp();
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
