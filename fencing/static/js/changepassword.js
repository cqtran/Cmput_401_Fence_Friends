function getCompany(){
//get details
  $.ajax({
      type: 'GET',
      url: '/getcompany/',
      success: function(result) {
        $('#companyNameNav').text(result);
        if(result == "Admin"){
        	changeAdmin();
        }

      }
  });
}
function changeAdmin(){
	//remove non admin buttons
	console.log("yes");
	$('.delete-admin').remove();
	$('#admin-users').text("Users");
	$('#admin-request').text("Account Requests");
	$('#admin-request-link').attr("href", "/accountrequests/");
	$('#admin-request-icon').attr("class", "fa fa-user-plus");
}

$(document).ready(function(){
	getCompany();
});