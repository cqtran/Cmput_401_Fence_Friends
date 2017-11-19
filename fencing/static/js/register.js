//checks if company already taken
$('#submit-button').click(function(){
  if(($('#password').val().length < 8) || ($('#password-confirm').val().length < 8)){
    alert("Password must be at least 8 characters long.");
  }
  else{
    $.ajax({
        type: 'POST',
        url: '/checkcompany/',
        data: { 
            name: $("#username").val()
        },
        datatype: 'json',
        success: function(result) {
          $('#register-form').submit();
        },
        error: function(result) {
            alert("Company name already registered.");
        }
    });
  }

});





