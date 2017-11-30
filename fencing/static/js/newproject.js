var chosenCustomers = [];
var isDirty = false;

function showMessage(message) {
	$('#message-text').html(message);
	$('#message').modal('show');
}

function removeCust(customer, torem){
  return customer != torem;
}

//add customer to html
function addToList(customer){
  if(chosenCustomers.length > 0){
    return;
  }
  //append to list of customers
  chosenCustomers.push(customer.cust_id);
  console.log(chosenCustomers);

  //get customer list element
  var customerList = document.getElementById('customers-list');

  $('#customers-list').append('\
  <div class="rounded customer-item container-fluid bottom-margin"> \
    <div class="col-12"> \
      <div class="row justify-content-between"> \
        <p class="top-bot-pad"><b>' + customer.value + '</b> - Phone ' + customer.phone + ' </p> \
        <button class="btn btn-grey float-right" type="button" id="' + customer.cust_id + '"> \
          <i class="fa fa-times" aria-hidden="true"></i> \
        </button> \
      </div> \
    </div> \
  </div>');
}
//delete html customer item on click
$(document).on('click', '.btn-grey', function(e) {
  var cid = this.id;
  console.log(chosenCustomers);
  chosenCustomers = chosenCustomers.filter(removeCust.bind(this, cid));
  console.log(JSON.stringify(chosenCustomers));
  $(e.target).parent().parent().parent().remove();
});

//send request to create project
$('form').submit(function(e) {
  e.preventDefault();
  if(typeof chosenCustomers != "undefined" && chosenCustomers != null && chosenCustomers.length > 0){
    $.ajax({
        type: 'POST',
        url: '/addproject/',
        data: { 
            customer: JSON.stringify(chosenCustomers), // < note use of 'this' here
            name: $("#name").val(),
            address: $('#address').val()
        },
        datatype: 'json',
        success: function(result) {
            var id = $.parseJSON(result);
            window.location.href = '/projectinfo?proj_id=' + id;
        },
        error: function(result) {
            showMessage('error');
        }
    });
  }
  else {
    showMessage("A customer must be selected.");
  }
});

//populate typeahead with customers
$('#add-project .typeahead').typeahead({
    highlight: true
  },
  {
    name: 'customers',
    displayKey: 'value',
    source: customers.ttAdapter(),
    templates: {
        suggestion: Handlebars.compile("<div class='container-fluid'><p class='top-bot-pad'><b>{{value}}</b> - Phone {{phone}} </p></div>")
    }
  }).on('typeahead:selected', function(event, selection) {
  if(!chosenCustomers.includes(selection.cust_id)){
    markDirty();
    addToList(selection);
  }
});

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

$(document).ready(function() {
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