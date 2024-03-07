function addFocusHandlers() {
	$('.top-nav-container button').focus(function() {
		$(this).parent().addClass('focused');
	}).blur(function() {
		$(this).parent().removeClass('focused');
	});
}

//document.addEventListener('DOMContentLoaded', addFocusHandlers);

//document.addEventListener('htmx:OnLoad', addFocusHandlers);