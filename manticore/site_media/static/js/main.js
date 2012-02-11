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

             $('.container').imagesLoaded(function() {
                   $('.nail').wookmark({offset: 20, itemWidth: 280});
               });
               $(window).resize(function() {
                 $('.nail').wookmark({offset: 20, itemWidth: 280});
               });
       });
