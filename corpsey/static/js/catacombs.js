// Infinite Corpse js brains for catacombs
// nate@clixel.com
$.corpsey = $.corpsey || {};

$.corpsey.catacombs = (function() {
  var History = window.History,
    State = History.getState(),
    comics_showing = [],
    comics_shown = [],
    nav_cache = [],
    max_comics_loaded = 15,
    uturns_shown = [],
    is_uturn = false, // true when on a uturn page
    uturn_single = false, // true when /uturn/xx
    $catacombs,
    medium_width = false,
    small_width = false,
    build_titles_timer;

  function _init() {
    // Get initial screen width
    _get_widths();
    State = History.getState();
    $catacombs = $('#catacombs');
    _get_comics_showing();

    // Init first strips as shown
    if (is_uturn) {
      uturns_shown.push(comics_showing[0]);
      $('.comic.single:not(.uturn)').each(function() {
        comics_shown.push(parseInt($(this).attr('data-comic-id')));
      });
    } else {
      for(var i=0; i<comics_showing.length; i++) {
        comics_shown.push(comics_showing[i]);
      }
    }
    $('<div id="flonav" />').appendTo('body').hide();

    History.replaceState(
      { 'direction': '' },
      document.title,
      window.location.pathname );

    // Bind to state change
    History.Adapter.bind(window, 'statechange', function(){
      State = History.getState();
      _get_comics_showing();
      _garbage_collection();
      _build_panels();
      $.corpsey.trackPage();
    });

    // Isotopize
    $catacombs.isotope({
      itemSelector: 'img,h1',
      transitionDuration: 0
    }).on('layoutComplete', function() {
      if (build_titles_timer) { clearTimeout(build_titles_timer); }
      build_titles_timer = setTimeout($.corpsey.catacombs.build_titles, 450);
    }).isotope({ filter: (small_width) ? '.comic.active img:not(.uturn-pad),.comic.active h1' : (medium_width) ? '.comic.active img:not(.uturn-pad)' : '.comic.active img' });
    _build_titles();

    // Next/prev buttons
    $('#content').on('click', 'a.prev,a.next', function(e) {
      e.preventDefault();

      if ($('.comic-nav').hasClass('loading')) { return false; }
      $('.comic-nav').addClass('loading');

      var direction = $(this).hasClass('next') ? 'next' : 'prev';
      var url = $(this).attr('href');
      var title = $(this).attr('title')+' : The Infinite Corpse';
      History.pushState({'direction': direction}, title, url);

      return false;
    });

    // Back button?
    $('#content').on('click', 'a.up', function(e) {
      e.preventDefault();

      if ($('.comic-nav').hasClass('loading')) { return false; }
      $('.comic-nav').addClass('loading');

      History.back();
      return false;
    });

    // Keyboard nerds
    $(document).on('keydown',function(e) {
      if (!e.metaKey) {
        if (e.keyCode === 39) {
          $('.next.button:first').trigger('click');
          e.preventDefault();
        } else if (e.keyCode === 37) {
          $('.prev.button:first').trigger('click');
          e.preventDefault();
        } else if (e.keyCode === 27) {
          _hide_flonav();
        }
      }
    });

     // Mobile nerds
    // $catacombs.on('swipeone', function (e, obj) {
    //     return; // disabling for now
    //     // var direction = obj.description.split(":")[2]
    //     // if (obj.delta[0].moved > 200) {
    //     //     if (direction === "left") {
    //     //         $('.prev.button:first').trigger('click');
    //     //     } else if (direction === "right") {
    //     //         $('.next.button:first').trigger('click');
    //     //     }
    //     // }
    // });
    // $catacombs.on('swipetwo', function (e, obj) {
    //     return; // disabling for now
    //     var direction = obj.description.split(":")[2]
    //     // todo, send along next or prev dir to show appropriate nav
    //     _show_flonav(e);
    // });

    // Init isotope filter based on window size
    _delayed_resize();
  }

  function _show_flonav(e) {
    var nav = $('.next.comic-nav').html();
    $('#flonav').show().css({left: e.pageX, top: e.pageY}).html(nav);
  }

  function _hide_flonav() {
    $('#flonav').hide();
  }

  function _get_comics_showing() {
    // Get comic_id array from URL
    comics_showing = State.url.replace(location.host,'').match(/\d+/g);

    // Build id arr and convert to int
    for(var i=0; i<comics_showing.length; i++) {
      comics_showing[i] = +comics_showing[i];
    }

    // Is this a uturn page?
    is_uturn = (State.url.match(/uturn/) !== null);

    // For /catacombs/uturn/5/ URLs
    if (is_uturn && comics_showing.length==1) {
      comics_showing[1] = +$('.comic.uturn.active').attr('data-portal-to-id');
      uturn_single = true;
    } else {
      uturn_single = false;
    }

    // Add class .one-comic-showing to adjust min-height
    $catacombs.toggleClass('one-comic-showing', (comics_showing.length===1));

    // Add .is-uturn class for small.less to shorten min-height
    $catacombs.toggleClass('is-uturn', is_uturn);
  }

  // Try to keep memory use not insane (was getting up to 900mb for one tab)
  function _garbage_collection() {
    // Remove first comic if we've shown more than max_comics_loaded
    if (comics_shown.length > max_comics_loaded) {
      $('.comic.single:not(.uturn)[data-comic-id='+comics_shown[0]+']').remove();
      var index = $.inArray(comics_shown[0], comics_shown);
      comics_shown.splice(index, 1);
    }
  }

  function _build_panels(){
    _hide_titles();
    // Check for comic panels to load
    for(var i=0; i<comics_showing.length; i++) {
      if (is_uturn && (i===0 && uturns_shown.indexOf(comics_showing[i]) < 0)) {
        $.get('/ajax/get_uturn_panel/', {
          'uturn_id': comics_showing[i],
          'direction': State.data.direction
        }).done(function(data) {
          _show_uturn(data);
        });
      } else if (
        // Uturns breaking my brain
        (is_uturn && i===1 && comics_shown.indexOf(comics_showing[i]) < 0) ||
        (!is_uturn && comics_shown.indexOf(comics_showing[i]) < 0)
      ){
        $.get('/ajax/get_comic_panels/', {
          'comic_id': comics_showing[i],
          'direction': State.data.direction
        }).done(function(data) {
          if (data.success) {
            _show_panels(data);
            _build_titles();
          }
        });
      } else {
        $('.comic.single[data-comic-id='+comics_showing[i]+']').addClass('active');
        _filter_panels();
      }
    }
    _build_titles();
  }

  function _show_uturn(data) {
    // Cache uturn data
    uturns_shown.push(data.uturn.uturn_id);

    // Build from mustache template
    var uturn = $($.corpsey.render_template('uturn_single', data.uturn));

    // Uturn is only ever from Next
    // $catacombs.append(uturn);
    $catacombs.isotope('appended', uturn);

    _filter_panels();
  }

  function _show_panels(data) {
    _hide_flonav();

    // Cache comic data
    comics_shown.push(data.comic.comic_id);

    // Build from mustache template
    var comic = $($.corpsey.render_template('comic_single', data.comic));

    // Drop in comic
    if (data.direction==='next') {
      $catacombs.append(comic);
      $catacombs.isotope('appended', comic);
    } else {
      $('#catacombs .comic.single.active:first').before(comic);
      $catacombs.isotope('prepended', comic);
    }
    _filter_panels();
  }

  function _filter_panels() {
    // I do this a lot. todo: clean this up
    _get_comics_showing();

    var visible_comics = [];
    $('#catacombs .comic.single.active').each(function() {
      var id = $(this).data('comic-id');
      // Somehow comics are duplicating sometimes?
      if ($.inArray(id,visible_comics)>-1 && !$(this).hasClass('uturn')) {
        $(this).remove();
      } else {
        visible_comics.push(id);
      }
    });

    // If you've looped through from last comic to first comic, make sure the URL matches visible order of comics
    // or if uturn and we're out of sync, swap em around!
    if ((!is_uturn && visible_comics[0]!==comics_showing[0]) ||
      (is_uturn && uturn_single && visible_comics[0]!==comics_showing[0])) {
      $('.comic.active[data-comic-id='+comics_showing[0]+']:first').after($('.comic.active[data-comic-id='+comics_showing[1]+']:first'));
    } else if (is_uturn && !uturn_single && visible_comics[0]===comics_showing[0]) {
      $('.comic.active[data-comic-id='+comics_showing[1]+']:first').after($('.comic.active[data-comic-id='+comics_showing[0]+']:first'));
    }

    // Reset sort order for isotope using DOM order
    $catacombs.isotope('reloadItems').isotope({ sortBy: 'original-order' });

    // Hide strips not in new url
    $('#catacombs .comic.single').each(function(){
      // Uturn pages have different logic, naturally
      if (is_uturn) {
        if (
          ($(this).hasClass('uturn') && $(this).data('comic-id')!==comics_showing[0]) ||
          (!$(this).hasClass('uturn') && $(this).data('comic-id')!==comics_showing[1]))
          {
            $(this).removeClass('active');
          }
      } else {
        if ($(this).hasClass('uturn') || $.inArray($(this).data('comic-id'), comics_showing)<0) {
          $(this).removeClass('active');
        }
      }
    });

    // Set isotope to filter visible comics
    $catacombs.isotope({ filter: (small_width) ? '.comic.active img:not(.uturn-pad),.comic.active h1' : (medium_width) ? '.comic.active img:not(.uturn-pad)' : '.comic.active img' });

    // If med/small screen, scroll up to comic we just loaded
    if (medium_width || small_width) {
      if (State.data.direction==='next') {
        var scrollTo = small_width ? 960 : 320;
        // For small_width single uturns (only has single first TC panel, scroll to panel 2 on page)
        if (small_width && is_uturn && uturn_single) {
          scrollTo = 340;
        }
        setTimeout(function() {
          $('html,body').animate({ scrollTop: scrollTo });
        }, 250);
      } else {
        setTimeout(function() {
          $('html,body').animate({ scrollTop: small_width ? 40 : 30 });
        }, 250);
      }
    }

    _get_comics_showing();
    _get_nav_links();
  }

  function _get_nav_links() {
    if (comics_showing[0]=='NaN') {
      return;
    }
    if (nav_cache[comics_showing.join('-')]) {
      _show_nav_links(nav_cache[comics_showing.join('-')]);
    } else {
      $.get('/ajax/get_nav_links/', {
        'comic_id_arr': comics_showing,
        'is_uturn': (is_uturn ? 1 : '')
      }).done(function(data) {
        nav_cache[comics_showing.join('-')] = data;
        _show_nav_links(data);
      });
    }
  }

  function _show_nav_links(data) {
    $('.comic-nav').remove();
    var nav;
    // Any nav to add?
    if (data.next_comic_links.length>0) {
      nav = $.corpsey.render_template('next_comic_nav', data);
      $('#content').append(nav);
    } else if (data.uturn_links.length>0) {
      nav = $.corpsey.render_template('uturn_nav', data.uturn_links[0]);
      $('#content').append(nav);
    }

    if (data.prev_comic_links.length>0) {
      nav = $.corpsey.render_template('prev_comic_nav', data);
      $('#content').append(nav);
    }
  }

  function _hide_titles() {
    $('h1.comic_1, h1.comic_2').fadeOut();
  }

  function _build_titles() {
    $('h1.comic_1, h1.comic_2').remove();
    $('.comic.single.active').each(function(i) {
      var name = $(this).find('h1').html();
      $('<h1 />').html(name).addClass('comic_'+(i+1)).appendTo('body').css({ 'top' : -1000 });
    });
    _move_titles();
  }

  function _move_titles() {
    $('.comic.single.active').each(function(i) {
      // Figure out which comic panel to position next to
      var c = (i===1 && $catacombs.width()<980) ? '1' : '0';
      // Todo: put this damn title to the right of the strip, ugh
      if (is_uturn && $(this).hasClass('uturn') && $catacombs.width()<980) {
        c = '1';
      }
      var $img = $(this).find('img:eq('+c+')');
      var pos = $img.offset();
      var $h1 = $('h1.comic_'+(i+1));
      if ($h1.length>0 && pos!==null) {
        $h1.css({ 'top' : pos.top+$h1.width(), 'left' : pos.left-16 });
      }
    });
    $('h1.comic_1, h1.comic_2').show();
  }

  function _resize() {
    _get_widths();
    _move_titles();
  }

  function _delayed_resize() {
    // $catacombs.isotope({ filter: (small_width) ? '.comic.active img:not(.uturn-pad),.comic.active h1' : (medium_width) ? '.comic.active img:not(.uturn-pad)' : '.comic.active img' });
  }

  function _get_widths() {
    var screen_width = document.documentElement.clientWidth;
    medium_width = screen_width <= 1020;
    small_width = screen_width <= 700;
  }

  // Public methods
  return {
    init: _init,
    resize: _resize,
    delayed_resize: _delayed_resize,
    build_titles: _build_titles,
    show_panels: function(data) {
      _show_panels(data);
    },
    show_uturn: function(data) {
      _show_uturn(data);
    },
    show_nav_links: function(data) {
      _show_nav_links(data);
    }
  };
})();

// Fire up the mothership
$(document).ready(function(){
  $.corpsey.catacombs.init();
});

// Adjust to mothership size variations
$(window).resize(function(){
  $.corpsey.catacombs.resize();

  // Delayed resize for more intensive tasks
  if($.corpsey.catacombs.delayed_resize_timer !== false) {
    clearTimeout($.corpsey.catacombs.delayed_resize_timer);
  }
  $.corpsey.catacombs.delayed_resize_timer = setTimeout($.corpsey.catacombs.delayed_resize, 200);
});
