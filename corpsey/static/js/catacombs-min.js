$.corpsey=$.corpsey||{},$.corpsey.catacombs=function(){function t(){if(v(),_=g.getState(),e(),x)k.push(y[0]),$(".comic.single:not(.uturn)").each((function(){b.push(parseInt($(this).attr("data-comic-id")))}));else for(var t=0;t<y.length;t++)b.push(y[t]);$('<div id="flonav" />').appendTo("body").hide(),g.replaceState({direction:""},document.title,window.location.pathname),g.Adapter.bind(window,"statechange",(function(){_=g.getState(),e(),o(),n(),$.corpsey.trackPage()})),$("#catacombs").isotope({itemSelector:"img,h1",onLayout:function(){j&&clearTimeout(j),j=setTimeout($.corpsey.catacombs.build_titles,450)}});var i=".comic.active img";S?i=".comic.active img:not(.uturn-pad),.comic.active h1":z&&(i=".comic.active img:not(.uturn-pad)"),$("#catacombs").isotope({filter:i}),$("#content").on("click","a.prev,a.next",(function(t){if(t.preventDefault(),$(".comic-nav").hasClass("loading"))return!1;$(".comic-nav").addClass("loading");var i=$(this).hasClass("next")?"next":"prev",c=$(this).attr("href"),e=$(this).attr("title")+" : The Infinite Corpse";return g.pushState({direction:i},e,c),!1})),$("#content").on("click","a.up",(function(t){return t.preventDefault(),$(".comic-nav").hasClass("loading")||($(".comic-nav").addClass("loading"),g.back()),!1})),$(document).on("keydown",(function(t){t.metaKey||(39===t.keyCode?($(".next.button:first").trigger("click"),t.preventDefault()):37===t.keyCode?($(".prev.button:first").trigger("click"),t.preventDefault()):27===t.keyCode&&c())})),f()}function i(t){var i=$(".next.comic-nav").html();$("#flonav").show().css({left:t.pageX,top:t.pageY}).html(i)}function c(){$("#flonav").hide()}function e(){y=_.url.replace(location.host,"").match(/\d+/g);for(var t=0;t<y.length;t++)y[t]=+y[t];(x=null!==_.url.match(/uturn/))&&1==y.length?(y[1]=+$(".comic.uturn.active").attr("data-portal-to-id"),T=!0):T=!1,$("#catacombs").toggleClass("one-comic-showing",1===y.length),$("#catacombs").toggleClass("is-uturn",x)}function o(){if(b.length>15){$(".comic.single:not(.uturn)[data-comic-id="+b[0]+"]").remove();var t=$.inArray(b[0],b);b.splice(t,1)}}function n(){d();for(var t=0;t<y.length;t++)x&&0===t&&k.indexOf(y[t])<0?$.get("/ajax/get_uturn_panel/",{uturn_id:y[t],direction:_.data.direction}).done((function(t){a(t)})):x&&1===t&&b.indexOf(y[t])<0||!x&&b.indexOf(y[t])<0?$.get("/ajax/get_comic_panels/",{comic_id:y[t],direction:_.data.direction}).done((function(t){t.success&&s(t)})):($(".comic.single[data-comic-id="+y[t]+"]").addClass("active"),r())}function a(t){k.push(t.uturn.uturn_id);var i=$.corpsey.render_template("uturn_single",t.uturn);$("#catacombs").isotope("insert",$(i)),r()}function s(t){c(),b.push(t.comic.comic_id);var i=$($.corpsey.render_template("comic_single",t.comic));"next"===t.direction?$("#catacombs").append(i):$("#catacombs .comic.single.active:first").before(i),r()}function r(){e();var t=[];if($("#catacombs .comic.single.active").each((function(){var i=$(this).data("comic-id");$.inArray(i,t)>-1&&!$(this).hasClass("uturn")?$(this).remove():t.push(i)})),!x&&t[0]!==y[0]||x&&T&&t[0]!==y[0]?$(".comic.active[data-comic-id="+y[0]+"]:first").after($(".comic.active[data-comic-id="+y[1]+"]:first")):x&&!T&&t[0]===y[0]&&$(".comic.active[data-comic-id="+y[1]+"]:first").after($(".comic.active[data-comic-id="+y[0]+"]:first")),$("#catacombs").isotope("reloadItems").isotope({sortBy:"original-order"}),$("#catacombs .comic.single").each((function(){x?($(this).hasClass("uturn")&&$(this).data("comic-id")!==y[0]||!$(this).hasClass("uturn")&&$(this).data("comic-id")!==y[1])&&$(this).removeClass("active"):($(this).hasClass("uturn")||$.inArray($(this).data("comic-id"),y)<0)&&$(this).removeClass("active")})),$("#catacombs").isotope({filter:S?".comic.active img:not(.uturn-pad),.comic.active h1":z?".comic.active img:not(.uturn-pad)":".comic.active img"}),z||S)if("next"===_.data.direction){var i=S?960:320;S&&x&&T&&(i=340),setTimeout((function(){$("html,body").animate({scrollTop:i})}),250)}else setTimeout((function(){$("html,body").animate({scrollTop:S?40:30})}),250);e(),m()}function m(){var t=y.join("-")+(x?"-uturn":"");C[t]?u(C[t]):$.get("/ajax/get_nav_links/",{comic_id_arr:y,is_uturn:x?1:""}).done((function(i){C[t]=i,u(i)}))}function u(t){var i;$(".comic-nav").remove(),t.next_comic_links.length>0?(i=$.corpsey.render_template("next_comic_nav",t),$("#content").append(i)):t.uturn_links.length>0&&(i=$.corpsey.render_template("uturn_nav",t.uturn_links[0]),$("#content").append(i)),t.prev_comic_links.length>0&&(i=$.corpsey.render_template("prev_comic_nav",t),$("#content").append(i))}function d(){$("h1.comic_1, h1.comic_2").fadeOut()}function l(){$("h1.comic_1, h1.comic_2").remove(),$(".comic.single.active").each((function(t){var i=$(this).find("h1").html();$("<h1 />").html(i).addClass("comic_"+(t+1)).appendTo("body").css({top:-1e3})})),h()}function h(){$(".comic.single.active").each((function(t){var i=1===t&&$("#catacombs").width()<980?"1":"0";x&&$(this).hasClass("uturn")&&$("#catacombs").width()<980&&(i="1");var c,e=$(this).find("img:eq("+i+")").offset(),o=$("h1.comic_"+(t+1));o.length>0&&null!==e&&o.css({top:e.top+o.width(),left:e.left-16})})),$("h1.comic_1, h1.comic_2").show()}function p(){v(),h()}function f(){$("#catacombs").isotope({filter:S?".comic.active img:not(.uturn-pad),.comic.active h1":z?".comic.active img:not(.uturn-pad)":".comic.active img"})}function v(){var t=document.documentElement.clientWidth;z=t<=1020,S=t<=700}var g=window.History,_=g.getState(),y=[],b=[],C=[],w=15,k=[],x=!1,T=!1,z=!1,S=!1,j;return{init:t,resize:p,delayed_resize:f,build_titles:l,show_panels:function(t){s(t)},show_uturn:function(t){a(t)},show_nav_links:function(t){u(t)}}}(),$(document).ready((function(){$.corpsey.catacombs.init()})),$(window).resize((function(){$.corpsey.catacombs.resize(),!1!==$.corpsey.catacombs.delayed_resize_timer&&clearTimeout($.corpsey.catacombs.delayed_resize_timer),$.corpsey.catacombs.delayed_resize_timer=setTimeout($.corpsey.catacombs.delayed_resize,200)}));