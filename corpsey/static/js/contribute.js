// Infinite Corpse js brains for reserving a spot to contribute
// nate@clixel.com
$.corpsey = $.corpsey || {};

// @codekit-prepend "libs/dropzone.js"
Dropzone.autoDiscover = false;

$.corpsey.contribute = (function() {
    var comic_id,
        contribute_form,
        my_dropzone;

    function _init() {
        // add .required to inputs
        $('label.required').each(function() {
            $('input#'+$(this).attr('for')).addClass('required');
        });

        // open links in new window (halftones, pg-13)
        $('.user-content a').attr('target','_blank');

        comic_id = $('.comic.single').attr('data-comic-id');
        contribute_form = $('form#contribute');
        if ($('.dropzone').length) {
            _initDropzone();
        }

        $('.new-leaf').click(function(e) {
            e.preventDefault();
            comic_id = $('.comic.single').attr('data-comic-id');
            $.get('/ajax/get_new_leaf/', {
                'comic_id': comic_id,
                'hdpi_enabled': ($.corpsey.hdpi_enabled() ? 1 : '')
            }).done(function(data) {
                _show_new_leaf(data);
            });
        });

        $('form.contribute').validate();
    }

    // Hijack upload form, init Dropzone
    function _initDropzone() {

        // Show dropzone ui
        $('.dropzone').addClass('active');

        my_dropzone = new Dropzone('#contribute', {
            paramName: 'comic_panels',
            url: $('#contribute').attr('action'),
            uploadMultiple: true,
            acceptedFiles: 'image/*',
            thumbnailWidth: 250,
            thumbnailHeight: 250,
            maxFiles: 3,
            parallelUploads: 3,
            maxFilesize: 6,
            previewsContainer: '#contribute .dz-previews',
            autoProcessQueue: false,
            addRemoveLinks: true,
            clickable: '#contribute .dz-message a',
            init: function() {
                this.on('maxfilesexceeded', function(file) {
                    // Just remove any more than 3 panels
                    this.removeFile(file);
                });
                this.on('sendingmultiple', function() {
                    contribute_form.addClass('images-uploading');
                });
                this.on('cancelmultiple', function() {
                    contribute_form.removeClass('images-uploading');
                    my_dropzone.removeAllFiles(true);
                });
                $('#contribute [type=submit]').click(function(e) {
                    e.preventDefault();
                    if (contribute_form.hasClass('images-uploading')) {
                        return false;
                    }
                    if (my_dropzone.files.length < 3) {
                        alert('You must upload 3 panels. You only have ' + my_dropzone.files.length + ' queued for upload.');
                        return false;
                    }
                    $('.dropzone').sortable('disable');
                    my_dropzone.processQueue();
                });
                this.on('successmultiple', function(files) {
                    if (files.length === 3) {
                        $('#contribute-form').fadeOut('slow', function() {
                            $('html,body').animate({scrollTop:0 }, 'fast');
                            $('#contribute-ok').fadeIn('slow');
                        });
                    } else {
                        $('.dropzone').sortable('enable');
                        alert('There was an error uploading all 3 files. Please try again.');
                    }
                });
            }
        });

        // Ability to drag to reorder panels before upload
        $('.dropzone').sortable({
            items: '.dz-preview',
            containment: '.dropzone',
            tolerance: 'touch',
            stop: function (){
                // Reorder dropzone file queue to match custom DOM order
                var newQueue = [],
                    queue = my_dropzone.files;
                $('.dropzone [data-dz-name]').each(function() {
                    var name = $(this).text();
                    queue.forEach(function(file) {
                        if (file.name === name) {
                            newQueue.push(file);
                        }
                    });
                });
                my_dropzone.files = newQueue;
            }
        });
    }

    function _show_new_leaf(data) {
        var comic = ich.comic_single(data.comic);
        $('#parent_comic').empty().append(comic);
        $('#id_comic_id').val(data.comic.comic_id);
        comic_id = data.comic.comic_id;
        if (typeof _gaq !== 'undefined') {
            _gaq.push(['_trackEvent', 'Contribute', 'New Leaf']);
        }
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
$(document).ready(function(){
    $.corpsey.contribute.init();
});
