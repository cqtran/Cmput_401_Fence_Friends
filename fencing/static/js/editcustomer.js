var cust_id;
var isDirty = false;

// Get Customer Information
function custData(cust) {
  document.getElementById('cust_name').value = cust[0].first_name;
  document.getElementById('email').value = cust[0].email;
  document.getElementById('cellphone').value = cust[0].cellphone;
  $('#companyNameNav').html(cust[0].company_name);
}

function showMessage(message) {
  $('#message-text').html(message);
  $('#message').modal('show');
}

function confirmDiscard() {
  return "Discard changes?";
}

function markDirty() {
  isDirty = true;
  window.onbeforeunload = confirmDiscard;
}

function markClean() {
  isDirty = false;
  window.onbeforeunload = null;
}

function deleteCustomer(){
  $.ajax({
      type: 'POST',
      url: '/deletecustomer/',
      data: { 
          cust_id: cust_id,
      },
      datatype: 'json',
      success: function(result) {
          window.location.href = '/';
      },
      error: function(result) {
          showMessage('error');
      }
  });
}

function makeClean() {
  window.onbeforeload = null;
}

function getCustomerData() {
  $.ajax({
    type: 'GET',
    url: '/getCustomer/' + cust_id,
    success: function(result) {
      console.log(result[0].first_name);
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
      url: '/updatecustomer/',
      data: {
        cust_id: cust_id,
        fname: $('#cust_name').val(),
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
  console.log(cust_id);
  if(cust_id == null) {
    alert('Customer  NULL');
    window.location.href = '/';
  }
  getCustomerData();

  $("#confirmDiscardSave").click(function() {
    $("#save").trigger("click");
  });

  $("a").click(function(event) {
    var href = $(this).attr("href");

    if (!isDirty || href.startsWith("#") || href == "" || href == null) {
      return;
    }

    event.preventDefault();

    $("#confirmDiscardOkay").click(function() {
      window.onbeforeunload = null;
      window.location.replace(href);
    });

    $("#confirmDiscard").modal("show");
  });
});
$('#delete-project').click(function(){
  deleteCustomer();
});

