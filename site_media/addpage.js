$(document).ready(function() {
	$("#newpagedialog").hide();
	$(".addpagebutton").click(function() {
		$("#newpagedialog").show();
		return false;
	});
	
	$(".closebutton").click(function() {
		$("#newpagedialog").hide();
		return false;
	});
});