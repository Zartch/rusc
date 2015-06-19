$(".menu-toggle").click(function(e) {
        e.preventDefault();
        $(".wrapper").toggleClass("active");
});

$(document).ready(function(){
    $(".hide").click(function(){
        $("sidebar").hide();
    });
    $(".show").click(function(){
        $("sidebar").show();
    });
});