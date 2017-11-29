var cust_id;

// Get Customer Information
function custData(cust) {
  document.getElementById('first_name').value = cust[0].first_name;
  document.getElementById('email').value = cust[0].email;
  document.getElementById('cellphone').value = cust[0].cellphone;
  $('#companyNameNav').html(cust[0].company_name);
  getCustomer(cust[0].customer_id);
}

function confirmDiscard() {
  return "Discard Changes?";
}

function makeDirty() {
  window.onbeforeload = confirmDiscard;
}

function makeClean() {
  window.onbeforeload = null;
}

function getCustomerData(cust_id) {
  $.ajax({
    type: 'GET',
    url: '/getCustomer/' + cust_id,
    success: function(result) {
      custData(result);
    }
  });
}

$('#edit-form').submit(function(e) {
  e.preventDefault();
  makeClean();
  if(typeof cust_id != "undefined" && cust_id != null) {
    $.ajax({
      type: 'POST',
      url: '/updatecustomer',
      data: {
        cust_id: cust_id,
        fname: $('#first_name').val(),
        email: $('#email').val(),
        cellphone: $('#cellphone').val(),
        companyname: $('company_name').val() 
      },
      datatype: 'json',
      success: function(result) {
        window.location.href = '/customerinfo?cust_id=' + cust_id + '&status=ALL';
      },

      error: function(result) {
        alert('error');
      }
    });
  }
  else {
    alert('A customer must be selected');
  }
});

// Runs after html loaded, all calls done here
$(document).ready(function() {
  cust_id = getParameterByName('cust_id');
  if(cust_id == null) {
    alert('Customer  NULL');
    window.location.href = '/';
  }
  getCustomerData();
});


