$.corpsey=$.corpsey||{},Dropzone.autoDiscover=!1,$.corpsey.contribute=function(){function e(){$("label.required").each(function(){$("input#"+$(this).attr("for")).addClass("required")}),$(".user-content a").attr("target","_blank"),o=$(".comic.single").attr("data-comic-id"),a=$("form#contribute"),$(".dropzone").length&&i(),$(".new-leaf").click(function(e){e.preventDefault(),o=$(".comic.single").attr("data-comic-id"),$.get("/ajax/get_new_leaf/",{comic_id:o,hdpi_enabled:$.corpsey.hdpi_enabled()?1:""}).done(function(e){n(e)})}),$("form.contribute").validate()}function i(){$(".dropzone").addClass("active"),c=new Dropzone("#contribute",{paramName:"comic_panels",url:$("#contribute").attr("action"),uploadMultiple:!0,acceptedFiles:"image/*",thumbnailWidth:250,thumbnailHeight:250,maxFiles:3,parallelUploads:3,maxFilesize:6,previewsContainer:"#contribute .dz-previews",autoProcessQueue:!1,addRemoveLinks:!0,clickable:"#contribute .dz-message a",init:function(){this.on("maxfilesexceeded",function(e){this.removeFile(e)}),this.on("sendingmultiple",function(){a.addClass("images-uploading")}),this.on("addedfile",function(){t()}),$("#contribute [type=submit]").click(function(e){return e.preventDefault(),!a.hasClass("images-uploading")&&(c.files.length<3?(alert("You must upload 3 panels. You only have "+c.files.length+" queued for upload."),!1):(r.option("disabled",!0),void c.processQueue()))}),this.on("successmultiple",function(e){3===e.length?$("#contribute-form").fadeOut("slow",function(){$("html,body").animate({scrollTop:0},"fast"),$("#contribute-ok").fadeIn("slow")}):(r.option("disabled",!1),alert("There was an error uploading all 3 files. Please try again."))})}}),t()}function t(){r&&r.destroy(),r=Sortable.create($(".dz-previews")[0],{draggable:".dz-preview",animation:250,onEnd:function(){var e=[],i=c.files;$(".dropzone [data-dz-name]").each(function(){var t=$(this).text();i.forEach(function(i){i.name===t&&e.push(i)})}),c.files=e}})}function n(e){var i=ich.comic_single(e.comic);$("#parent_comic").empty().append(i),$("#id_comic_id").val(e.comic.comic_id),o=e.comic.comic_id,"undefined"!=typeof _gaq&&_gaq.push(["_trackEvent","Contribute","New Leaf"])}var o,a,c,r;return{init:function(){e()},show_new_leaf:function(e){n(e)}}}(),$(document).ready(function(){$.corpsey.contribute.init()});