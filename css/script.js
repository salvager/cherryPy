$(document).ready(function(){
	$('#numFound').slideDown();		
	 $('.button').each(function(){
	        var toggle_div_id = 'description_' + $(this).attr('id');
		var button_id = $(this).attr('id');
       		$('#'+toggle_div_id).toggle(false);
	 	$(this).click(function(){
            		$('#'+toggle_div_id).toggle();
        	});
    	});
});
