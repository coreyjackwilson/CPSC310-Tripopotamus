jQuery(function ($) {
	   $('[id*=basic-modal] > ul > li > a').click(function(){
	    var that = $(this),
	     index = that[0].className.split('-')[1],
	     selector = '#basic-modal-content' + index;

	    $(selector).modal();
	    return false;
	   });
	    });
