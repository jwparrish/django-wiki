$(document).ready(function() {
	$("#newpagedialog").hide();
	$(".addpagebutton").click(function() {
		$("#newpagedialog").show();
		return false;
	});
	
	$("body #content").click(function() {
		$("#newpagedialog").hide();
		return false;
	});
});