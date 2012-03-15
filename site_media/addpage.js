$(document).ready(function() {
	$("#newpagedialog").hide();
	$(".addpagebutton").click(function() {
		$("#newpagedialog").show();
		return false;
	});
	
	$(".cancelbutton").click(function() {
		$("#newpagedialog").hide();
		return false;
	});
});