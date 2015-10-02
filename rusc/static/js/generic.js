

$( document ).ready(function() {

    <!-- Script per oucultar el menu -->
    $("#menu-toggle").click(function(e) {
        e.preventDefault();
        /*USO CON STATIC/CSS/simple-sidebar.css*/
        $("#wrapper").toggleClass("toggled");
        var $this = $(this).toggleClass('toggled');
        if($(this).hasClass('toggled')){
            $(this).text('>');
        } else {
            $(this).text('<');
        }
    });


    $("#busk-toggle").click(function(e) {
        e.preventDefault();
        $("#div_bsk_extend").toggle();
    });


 });

/*Script per Notificacións */
function CallNotification(msg,type, position,width,height, multiline, time){
    position = position || "left";
    type = type || "info";
    multiline = multiline || "true";
    time = time || 10000;
    width = width || "all";
    height = height || 80;

    notif({
        msg: msg,
        type: type,
        position: position,
        multiline : multiline,
        time: time,
        width: width

    });

    /*  OPTIONS NOTIFIT
        msg: "<b>Oops!</b> A wild error appeared!",
        type: "success","info", "warning","error",
        position: "center", "left","right",
        bgcolor: "#294447",
        color: "#F19C65"
        time: 1000
        autohide: false,
        multiline: true
        opacity: 0.8
        width: 500,"all",
        height: 60,
    */

}

