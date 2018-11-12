$(document).ready(function() {
    $('#exampleModal').modal('show');
  });
  
  // https://codepen.io/PriscilaCunha/pen/ZGojLL
  $(document).ready(function(){
    $("ul.nav li a[href^='#']").click(function(){
        $("html, body").stop().animate({
            scrollTop: $($(this).attr("href")).offset().top
        }, 400);
    });
  });