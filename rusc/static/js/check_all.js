jQuery(document).ready(function($)
{
    $(".chk_all").click(function(e)
        {
            $('input:checkbox').not(this).prop('checked', this.checked);});
    });