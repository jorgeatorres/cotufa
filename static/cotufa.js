
$(function() {
   
   $('.movielist .movie .actions li a').click(function(e){
      e.preventDefault();
      $(this).parents('.bodywrapper').find('.tabcontent').children().hide();
      $(this).parents('.bodywrapper').find('.tabcontent ' + '.' + $(this).attr('rel')).show();
      $(this).parents('ul.actions').find('li').removeClass('selected');
      $(this).parent('li').addClass('selected');

   });
   
   $('.movielist .movie .header .metadata').click(function(e) {
      e.stopPropagation(); 
   });
   
   $('.movielist .movie .metadata .seenoneditor').blur(function(e) {
       var val = $(this).val();
       var $seenon = $(this).parents('.seenon');

       $.get($(this).attr('rel') + '&value=' + val, function(res) {
           $seenon.find('.value').text(val == '' ? '?' : val).show();
           $seenon.find('.seenoneditor').hide();
       });

   });
   
   $('.movielist .movie .header .metadata .seenon .value').click(function(e) {
       var $seenon = $(this).parents('.seenon');
       var value = $seenon.find('.value').hide().text();
       
       $seenon.find('.seenoneditor').val(value == '?' ? '' : value).show();
   });
   
   $('.movielist .movie .header').click(function(e) {
       var $movie = $(this).parents('.movie');
       
       if ($movie.find('.bodywrapper').is(':visible')) {
           $movie.find('.bodywrapper').slideToggle();
       } else {
           $movie.find('.ajaxloader').show();
       
           $movie.find('.body').load($movie.attr('rel'), function() {
               $movie.find('.ajaxloader').hide();
               $movie.find('.bodywrapper').slideToggle();
           });
       }
   });
   
   $('.movie .rating .star').click(function(e) {
       e.preventDefault();

       var $movie = $(this).parents('.movie');
       $movie.find('.ajaxloader').show();
       
       $.get($(this).attr('href'), function(res) {
           if (res._status == 'ok') {
               $movie.find('.ajaxloader').hide();
               
               $movie.find('.rating a').each(function(i, v) {
                   $(v).removeClass('on');

                   if (i < res.value) {
                       $(v).addClass('on');
                    }
               });
           }
       }, 'json');
   });
   
   $('.movie .movie-notes textarea').live('blur', function(e) {
       var $notesform = $(this).parent('form');
       var $movie = $(this).parents('.movie');
       var $textarea = $(this);
       
       $movie.find('.ajaxloader').show();
       $.post($notesform.attr('action'), {notes: $textarea.val()}, function(res) {
           if (res._status != 'ok') {
               $(this).addClass('error');
           }
           
           $movie.find('.ajaxloader').hide();
       }, 'json');
   });
   
});
