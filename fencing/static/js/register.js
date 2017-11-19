var companyValid = 0; //0 = invalid, 1 = valid
var emailValid = 0; //0 = invalid, 1 = valid

function checkMail(){
  //checks if email has been taken
  $.ajax({
    type: 'POST',
    url: '/checkemail/',
    data: { 
        email: $("#email").val()
    },
    datatype: 'json',
    success: function(result) {
      emailValid = 1;
      if((companyValid == 1) && (emailValid == 1)){
        allValid();
      }
    },
    error: function(result) {
        alert("Email already registered.");
    }
  });
}

function checkCompany(){
  $.ajax({
    type: 'POST',
    url: '/checkcompany/',
    data: { 
        name: $("#username").val()
    },
    datatype: 'json',
    success: function(result) {
      companyValid = 1;
      if((companyValid == 1) && (emailValid == 1)){
        allValid();
      }
    },
    error: function(result) {
        alert("Company name already registered.");
    }
  });
}

function allValid(){
  companyValid = 0;
  emailValid = 0;
  $('#register-form').submit();

}
//checks if company already taken
$('#submit-button').click(function(){
  companyValid = 0;
  emailValid = 0;
  if(($('#password').val().length < 8) || ($('#password-confirm').val().length < 8)){
    alert("Password must be at least 8 characters long.");
  }
  else{
    checkCompany();
    checkMail();
  }

});
