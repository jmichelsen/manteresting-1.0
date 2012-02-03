function __man_show() {
    var preview_width = 200;
    var preview_height = 200;
    var min_width = 300;
    var min_height = 300;

    if (typeof jQuery == 'undefined') {// jQuery isn't loaded yet. Get back later
        setTimeout(__man_show, 500);
        return;
    }

    // Helpers
    function add_css(filename) {
        var link = document.createElement("link");
        link.setAttribute("rel", "stylesheet");
        link.setAttribute("type", "text/css");
        link.setAttribute("href", filename);
        document.getElementsByTagName("head")[0].appendChild(link);
    }

    function add_js(filename) {
        var s = document.createElement('script');
        s.setAttribute('src', filename);
        s.setAttribute('type','text/javascript');
        document.getElementsByTagName("body")[0].appendChild(s);
    }

    function error(m) {
        if (window.console && window.console.error) {
          window.console.error(m);
        }
    }


    // Application logic
    (function($){
        function close() {
            $('.man-overlay, .man-controls, .man-previews').fadeOut();
        }

        function show() {
            var man_elements = $('.man-overlay, .man-controls, .man-previews');

            if (man_elements.length > 0) {
                /* Don't do the same job twice, just show controls if they are already there. */
                man_elements.fadeIn();
                $('body').scrollTop(0);
                return;
            }

            add_css(__man_base + 'site_media/static/css/bookmarklet.css');
            add_js(__man_base + 'site_media/static/js/jquery-1.7.min.js');

            var overlay = $('<div class="man-overlay"></div>');
            var controls = $('<div class="man-controls"><h1>Manteresting</h1><a class="man-hide-button" href="#">Hide</a></div>');

            controls.find('.man-hide-button').click(function(ev) {
                close();
                ev.preventDefault();
            });

            var previews = $('<div class="man-previews"></div>');

            $('img').each(function(idx, el) {
                var width = el.width;
                var height = el.height;

                if (width >= min_width && height >= min_height) {
                    var preview = $('<div class="man-preview"><div><a href="#"><img /></a></div><span></span></div>');
                    var img = preview.find('img')[0];
                    img.src = el.src;

                    // Scale image to fit into the preview
                    if (width > height) {
                        img.width = preview_width;
                        img.height = height * preview_width / width;
                    } else {
                        img.height = preview_height;
                        img.width = width * preview_height / height;
                    }

                    preview.find('span').text(width + 'x' + height);

                    var link = preview.find('a')[0];
                    link.href = __man_base + 'nail/add/?media=' + el.src + '&source_title=' + document.title + '&source_url=' + window.location;
                    previews.append(preview);
                }
            });

            $('body').append(overlay);
            $('body').append(controls);
            $('body').append(previews);
            $('body').scrollTop(0);
        }

        show();
    })(jQuery);
}

__man_show();
