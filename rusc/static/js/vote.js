jQuery(document).ready(function($)
    {
	$(".vote_form").submit(function(e)
		{
		    e.preventDefault();
		    var btn = $("button", this);
		    var l_id = $(".hidden_id", this).val();
		    btn.attr('disabled', true);
		    $.post("/forum/vote/", $(this).serializeArray(),
			  function(data) {
			      if(data["voteobj"]) {
				     btn.text("-");
                     CallNotification("Has votado","success")
			      }
			      else {
				     btn.text("+");
                     CallNotification("Has retirado tu voto","success")
			      }
			  });
		    btn.attr('disabled', false);
		});


    });

