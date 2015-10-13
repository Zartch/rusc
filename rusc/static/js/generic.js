

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


$(".id_text").keyup(function(e)
{

   var links = new Array;
   var text = $('#id_text').val();
   var regexp = /(\b(https?|ftp|file):\/\/[-A-Z0-9+&@#\/%?=~_|!:,.;]*[-A-Z0-9+&@#\/%=~_|])/ig;
//   var urlExists = (function(url){
//        return $.ajax({
//            type: 'HEAD',
//            url : url
//        });
//   });

    var url;


e.preventDefault();

   while(matches = regexp.exec(text))
{

url=matches[0];
links.push(url);

}
if(links.length>0){
$.ajax({
//                cache: false,
//                async: false,
                url: "/forum/url/",
                data: {
//                    csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
                    'links[]': links},
                type: "POST",
                success: function(response) {
//     $.post("/url/", links,
//			  function(data) {


                    var z = 0
    var i = 0
    var final_links = new Array;
    var f = $("#l1").attr('href')

//    var
    if(f){
    final_links.push(f);
         f = $("#l2").attr('href')
        if(f){
            final_links.push(f);
            f = $("#l3").attr('href')
            if(f){
                final_links.push(f);
                f = $("#l4").attr('href')
                if(f){
                    final_links.push(f);
        }
        }
        }
    }
    while(response[i])
    {
        if(response[i] == final_links[0]||response[i] == final_links[1]||response[i] == final_links[2]||response[i] == final_links[3]){
            i++;
            continue
        }
        else{
            final_links.push(response[i]);
            z=1;
        }
        i++;

//        $("#result").html("<a href='"+links[i]+"' class='oembed'/>").add()


    }
    var d;
    var s;
    var input;
    if(z==1){
//        while(final_links[d]){
        for (d = 0; d < final_links.length; ++d) {
            if(d==0){
//            $('<button/>', {
//                text: 'holaaaaaaaa', //set text 1 to 10
//                id: 'l1',
//                click: function remove_link(){
//
//
//
//
//                }
//    });


            $("#result1").html(("<a href='"+final_links[d]+"' id='l1' class='oembed'>link1 "+final_links[d]+"</a> <button type='button' class='r1'>x</button>"))
            //$("#l1").oembed(final_links[d],
            //{
            //////    //embedMethod: "append", // you can use .. fill , auto , replace
            //maxWidth: 600,
            //maxHeight: 350
            //}, "append");
            //$("#result1").oembed("http://www.flickr.com/photos/14516334@N00/345009210/");
            //$("#result1").oembed(final_links[d]);
            $("#l1").oembed(null,
                {
                embedMethod: "append", // you can use .. fill , auto , replace
                maxWidth: 200,
                maxHeight: 123
                });

            }
            //$("#result1").oembed();
            if(d==1){
            $("#result2").html("<a href='"+final_links[d]+"' id='l2' class='oembed'>link2 "+final_links[d]+"</a> <button type='button' class='r2'>x</button>").add()
            $("#l2").oembed(null,
                {
                embedMethod: "append", // you can use .. fill , auto , replace
                maxWidth: 200,
                maxHeight: 123
                });
            }
            if(d==2){
            $("#result3").html("<a href='"+final_links[d]+"' id='l3' class='oembed'>link3 "+final_links[d]+"</a> <button type='button' class='r3'>x</button>").add()
            $("#l3").oembed(null,
                {
                embedMethod: "append", // you can use .. fill , auto , replace
                maxWidth: 200,
                maxHeight: 123
                });
            }
            if(d==3){
            $("#result4").html("<a href='"+final_links[d]+"' id='l4' class='oembed'>link4 "+final_links[d]+"</a> <button type='button' class='r4'>x</button>").add()
            $("#l4").oembed(null,
                {
                embedMethod: "append", // you can use .. fill , auto , replace
                maxWidth: 200,
                maxHeight: 123
                });
    }
            }
    }



},
                    error: function(){
//                    links.push(matches[0]);
                }
   })
}




});



$('#result1').on("click", "button.r1", function(){

    var final_links = new Array;

    var f = $("#l2").attr('href')
    if(f){
        final_links.push(f);
        f = $("#l3").attr('href')
        if(f){
            final_links.push(f);
            f = $("#l4").attr('href')
            if(f){
                final_links.push(f);
    }
    }
    }

    $("#result1").html("").add()
    $("#result2").html("").add()
    $("#result3").html("").add()
    $("#result4").html("").add()

    var d;
    for (d = 0; d < final_links.length; ++d) {
        if(d==0){
        $("#result1").html("<a href='"+final_links[d]+"' id='l1' class='oembed'>link1 "+final_links[d]+"</a> <button type='button' class='r1'>x</button>").add()
          $("#l1").oembed(null,
            {
            embedMethod: "append", // you can use .. fill , auto , replace
            maxWidth: 200,
            maxHeight: 123
            });
        }
        if(d==1){
        $("#result2").html("<a href='"+final_links[d]+"' id='l2' class='oembed'>link2 "+final_links[d]+"</a> <button type='button' class='r2'>x</button>").add()
        $("#l2").oembed(null,
            {
            embedMethod: "append", // you can use .. fill , auto , replace
            maxWidth: 200,
            maxHeight: 123
            });
        }
        if(d==2){
        $("#result3").html("<a href='"+final_links[d]+"' id='l3' class='oembed'>link3 "+final_links[d]+"</a> <button type='button' class='r3'>x</button>").add()
         $("#l3").oembed(null,
            {
            embedMethod: "append", // you can use .. fill , auto , replace
            maxWidth: 200,
            maxHeight: 123
            });
        }
        if(d==3){
        $("#result4").html("<a href='"+final_links[d]+"' id='l4' class='oembed'>link4 "+final_links[d]+"</a> <button type='button' class='r4'>x</button>").add()
        $("#l4").oembed(null,
            {
            embedMethod: "append", // you can use .. fill , auto , replace
            maxWidth: 200,
            maxHeight: 123
            });
        }
    }



});

$('#result2').on("click", "button.r2", function(){

//        $("#result1").html("").add()


        var final_links = new Array;

        var f = $("#l1").attr('href')
        if(f){
            final_links.push(f);
            f = $("#l3").attr('href')
            if(f){
                final_links.push(f);
                f = $("#l4").attr('href')
                if(f){
                    final_links.push(f);
        }
        }
        }


        $("#result1").html("").add()
        $("#result2").html("").add()
        $("#result3").html("").add()
        $("#result4").html("").add()



        var d;
        for (d = 0; d < final_links.length; ++d) {
            if(d==0){
            $("#result1").html("<a href='"+final_links[d]+"' id='l1' class='oembed' >link1 "+final_links[d]+"</a> <button type='button' class='r1'>x</button>").add()
              $("#l1").oembed(null,
                {
                embedMethod: "append", // you can use .. fill , auto , replace
                maxWidth: 200,
                maxHeight: 123
                });
                }
            if(d==1){
            $("#result2").html("<a href='"+final_links[d]+"' id='l2' class='oembed'>link2 "+final_links[d]+"</a> <button type='button' class='r2'>x</button>").add()
            $("#l2").oembed(null,
                {
                embedMethod: "append", // you can use .. fill , auto , replace
                maxWidth: 200,
                maxHeight: 123
                });
            }
            if(d==2){
            $("#result3").html("<a href='"+final_links[d]+"' id='l3' class='oembed'>link3 "+final_links[d]+"</a> <button type='button' class='r3'>x</button>").add()
             $("#l3").oembed(null,
                {
                embedMethod: "append", // you can use .. fill , auto , replace
                maxWidth: 200,
                maxHeight: 123
                });
            }
            if(d==3){
            $("#result4").html("<a href='"+final_links[d]+"' id='l4' class='oembed'>link4 "+final_links[d]+"</a> <button type='button' class='r4'>x</button>").add()
            $("#l4").oembed(null,
                {
                embedMethod: "append", // you can use .. fill , auto , replace
                maxWidth: 200,
                maxHeight: 123
                });
            }
        }



    });

$('#result3').on("click", "button.r3", function(){

//        $("#result1").html("").add()


        var final_links = new Array;

        var f = $("#l1").attr('href')
        if(f){
            final_links.push(f);
            f = $("#l2").attr('href')
            if(f){
                final_links.push(f);
                f = $("#l4").attr('href')
                if(f){
                    final_links.push(f);
        }
        }
        }


        $("#result1").html("").add()
        $("#result2").html("").add()
        $("#result3").html("").add()
        $("#result4").html("").add()



        var d;
        for (d = 0; d < final_links.length; ++d) {
            if(d==0){
            $("#result1").html("<a href='"+final_links[d]+"' id='l1' class='oembed' >link1 "+final_links[d]+"</a> <button type='button' class='r1'>x</button>").add()
              $("#l1").oembed(null,
                {
                embedMethod: "append", // you can use .. fill , auto , replace
                maxWidth: 200,
                maxHeight: 123
                });
                }
            if(d==1){
            $("#result2").html("<a href='"+final_links[d]+"' id='l2' class='oembed'>link2 "+final_links[d]+"</a> <button type='button' class='r2'>x</button>").add()
            $("#l2").oembed(null,
                {
                embedMethod: "append", // you can use .. fill , auto , replace
                maxWidth: 200,
                maxHeight: 123
                });
            }
            if(d==2){
            $("#result3").html("<a href='"+final_links[d]+"' id='l3' class='oembed'>link3 "+final_links[d]+"</a> <button type='button' class='r3'>x</button>").add()
             $("#l3").oembed(null,
                {
                embedMethod: "append", // you can use .. fill , auto , replace
                maxWidth: 200,
                maxHeight: 123
                });
            }
            if(d==3){
            $("#result4").html("<a href='"+final_links[d]+"' id='l4' class='oembed'>link4 "+final_links[d]+"</a> <button type='button' class='r4'>x</button>").add()
            $("#l4").oembed(null,
                {
                embedMethod: "append", // you can use .. fill , auto , replace
                maxWidth: 200,
                maxHeight: 123
                });
            }
        }




    });

$('#result4').on("click", "button.r4", function(){

//        $("#result1").html("").add()


        var final_links = new Array;

        var f = $("#l1").attr('href')
        if(f){
            final_links.push(f);
            f = $("#l2").attr('href')
            if(f){
                final_links.push(f);
                f = $("#l3").attr('href')
                if(f){
                    final_links.push(f);
        }
        }
        }


        $("#result1").html("").add()
        $("#result2").html("").add()
        $("#result3").html("").add()
        $("#result4").html("").add()



        var d;
        for (d = 0; d < final_links.length; ++d) {
            if(d==0){
            $("#result1").html("<a href='"+final_links[d]+"' id='l1' class='oembed'>link1 "+final_links[d]+"</a> <button type='button' class='r1'>x</button>").add()
              $("#l1").oembed(null,
                {
                embedMethod: "append", // you can use .. fill , auto , replace
                maxWidth: 200,
                maxHeight: 123
                });
                }
            if(d==1){
            $("#result2").html("<a href='"+final_links[d]+"' id='l2' class='oembed'>link2 "+final_links[d]+"</a> <button type='button' class='r2'>x</button>").add()
            $("#l2").oembed(null,
                {
                embedMethod: "append", // you can use .. fill , auto , replace
                maxWidth: 200,
                maxHeight: 123
                });
            }
            if(d==2){
            $("#result3").html("<a href='"+final_links[d]+"' id='l3' class='oembed'>link3 "+final_links[d]+"</a> <button type='button' class='r3'>x</button>").add()
             $("#l3").oembed(null,
                {
                embedMethod: "append", // you can use .. fill , auto , replace
                maxWidth: 200,
                maxHeight: 123
                });
            }
            if(d==3){
            $("#result4").html("<a href='"+final_links[d]+"' id='l4' class='oembed'>link4 "+final_links[d]+"</a> <button type='button' class='r4'>x</button>").add()
            $("#l4").oembed(null,
                {
                embedMethod: "append", // you can use .. fill , auto , replace
                maxWidth: 200,
                maxHeight: 123
                });
            }
        }




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


