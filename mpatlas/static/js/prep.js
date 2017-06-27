define([
  // These are path aliases configured in the requireJS bootstrap
  'jquery',
  'jqueryui'
], function($){  
    var preparePage = function() {
 		$('.search-main .navbar-form')
 			.on("focusin", function(e) {
	 			$(e.delegateTarget).addClass('focused');
	 		})
	 		.on("focusout", function(e) {
	 			$(e.delegateTarget).removeClass('focused');
	 		})
	 		.on("keyup", function(e) {
	 		     if (e.keyCode == 27) { // escape key maps to keycode `27`
	 		        $('.search-main .navbar-form *').blur();
	 		    }
	 		});;
        $('.mpa-searchbox').autocomplete({
			source: function( request, response ) {
				$.ajax({
					url: "/mpa/sites/json/?q="+request.term,
					success: function( data ) {
						response( $.map( data.mpas, function( item ) {
							return {
								label: item.name + (item.designation ? ", " + item.designation : "") + ", " + item.country,
								value: item.name,
								url: item.url
							}
						}));
					}
				});
			},
			minLength: 2,
			select: function( event, ui ) {
			    if (ui.item) {
			        window.location = ui.item.url
			    }
			}
		});

		// Prep all search boxes to hack in default value placeholder
        $('form input:text.defaultValue, form textarea.defaultValue').each(function(){
	        $.data(this, 'default', $(this).attr("data-placeholder"));
	    }).focus(function(){
	        if ($.data(this, 'default') == $(this).val()) {
	            $(this).val('');
	        }
			$(this).removeClass('defaultValue');

	    }).blur(function(){
	        if ($(this).val() == '') {
	            $(this).val($.data(this, 'default'));
	        }
			$(this).addClass('defaultValue');
	    });
	    
	    // Activate user login form display
	    $('.user_loginlink').on('click', function(e) {
	        e.preventDefault();
	        e.stopPropagation();
	        $('#user_logintab').toggleClass('selected');
	        $('#id_username').focus();
	    });
	    
	    // Set a default Accept headers for javascript and json
	    $.ajaxSetup({
            'beforeSend': function(xhr) {
                xhr.setRequestHeader("Accept", "text/javascript")
                xhr.setRequestHeader("Accept", "application/json")
            }
        })
	    
	    // Run this on a form to automatically change it to submit via ajax
	    $.fn.submitWithAjax = function() {
	        this.submit(function() {
	            $.post(this.action, $(this).serialize(), null, "script");
	            return false;
	        });
            return this;
        };
    };
    
    var showsplashdialog = function() {
        $("#splashdialog").dialog({
			width: "60%",
      zIndex: 99999,
			modal: true
		});
    };

    return {
      preparePage: preparePage,
      showsplashdialog: showsplashdialog
    };
    // What we return here will be used by other modules
});
