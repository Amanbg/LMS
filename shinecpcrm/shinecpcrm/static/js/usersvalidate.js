$(document).ready(function(){
 document.getElementById("form_button").addEventListener("click", function () {
 		$.ajax({
			url:"/",
			type:"POST",
			data:$("#login").serialize(),
			success:function(response){
				dat = jQuery.parseJSON(response);
				console.log(dat);
				if (dat.status == "True"){
					top.window.location = dat.url;
				}
				else if (dat.status == "False") {
					alert(dat.msg);	
				}
			},
			error:function() {
				
			}
		});
	});




});  
