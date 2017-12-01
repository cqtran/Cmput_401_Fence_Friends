// Get the <datalist> and <input> elements.
var customerList = document.getElementById('customerlist');

function createCustomers(customers){
  customers.forEach(function(customer) {
    var item = document.createElement('div');
    var final = document.createElement('div');
    var link = document.createElement('a');
    var inner = document.createElement('div');
    var name = document.createElement('h2');
    var number = document.createElement('h6');
    var email = document.createElement('h6');

    email.setAttribute('class', 'card-body mb-1 text-center no-padding');
    email.innerText = customer.email;

    number.setAttribute('class', 'card-body mb-1 text-center no-padding');
    number.innerText = customer.cellphone;

    name.setAttribute('class', 'card-title mb-1 text-center no-padding');
    name.innerText = customer.first_name;

    link.setAttribute('href', '#')

    inner.setAttribute('class', 'card-body');
    inner.appendChild(name);
    inner.appendChild(number);
    inner.appendChild(email);

    link.appendChild(inner);
    item.setAttribute('class', 'card mb-2 full-width');
    final.setAttribute('class', 'less-padding card-row col-lg-4 col-md-6');

    // this is where you want to go when you click
    //item.setAttribute('onclick', 'window.location.href="{{ url_for('projects') }}"' )
    link.setAttribute('onclick', 'customerClicked('+customer.customer_id+')');
    link.setAttribute('oncontextmenu',
      'customerMenu(event,'+customer.customer_id+')');
    link.setAttribute('class', 'no-select');

    item.appendChild(link);
    final.appendChild(item);
    // Add it to the list:
    customerList.appendChild(final);
  });
}

function showError(){
  var item = document.createElement('a');
  item.appendChild(document.createTextNode('No customers were found.'));
  customerList.appendChild(item);

  var createNew = document.createElement('a');
  createNew.setAttribute('class', 'btn btn-primary btn-block')
  createNew.appendChild(document.createTextNode('Click here to create a new customer'));
  createNew.setAttribute('href', "/newcustomer")
  customerList.appendChild(createNew);
}

function updateCustomerList() {
  request.open('GET', '/getCustomerList', true);
  request.send();
}

function customerClicked(id) {
	window.location.href= '/customerinfo?cust_id=' + id + "&status=All"
}

$(document).ready(function(){
  $.ajax({
    type: 'GET',
    url: '/getCustomerList/',
    success: function(result) {
      createCustomers(result);
      $('#companyNameNav').html(result[0].company_name);
    },
    error: function(result) {
        showError();
    }
  });
});

function customerMenu(event, id) {
  event.preventDefault();

	$('#edit-customer').click(function() {
		window.location.href = '/editcustomer?cust_id=' + id;
	});

	$('#menu').modal('show');
}