    $(document).ready(function() {
           var $loading = $("<div class='loading'><p>Loading more items&hellip;</p></div>"),
           $footer = $('footer'),
           opts = {
             offset: '100%'
             };

             $footer.waypoint(function(event, direction) {
                 $footer.waypoint('remove');
                 $('body').append($loading);
                 $.get($('.more a').attr('href'), function(data) {
                   var $data = $(data);
                   $('#container').append($data.find('.article'));
                   $loading.detach();
                   $('.more').replaceWith($data.find('.more'));
                   $footer.waypoint(opts);
                 });
               }, opts);

             var wookmark_options = {offset: 16, itemWidth: 280, container: $('#nails_container')};
             $('.container').imagesLoaded(function() {
                   $('.nail').wookmark(wookmark_options);
               });
               $(window).resize(function() {
                 $('.nail').wookmark(wookmark_options);
               });
           // Not elegant, but possibly the only way to force a wookmark
           // re-flow after loading more nails
           $('.container').ajaxComplete(function() {
               $('.nail').wookmark(wookmark_options);
           });
       });
