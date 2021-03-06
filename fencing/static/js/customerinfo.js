// Get the project list element
var projectList = document.getElementById('projectlist');
var cust_id;

function escapeAngleBrackets(string) {
	return String(string).replace(/[<>]/g, function (s) {
		return angleBracketMap[s];
	});
}

function showMessage(message) {
	$('#message-text').html(message);
	$('#message').modal('show');
}

function updateProjects(projects){
  $('#projectlist').empty();
  projects.forEach(function(project) {
    var item = document.createElement('div');
    var final = document.createElement('div');
    var link = document.createElement('a');
    var inner = document.createElement('div');
    var name = document.createElement('h2');
    var status = document.createElement('h6');
    var address = document.createElement('h6');

    status.setAttribute('class', 'card-body mb-1 text-center no-padding');
    status.innerText = project.status_name;

    address.setAttribute('class', 'card-body mb-1 text-center no-padding');
    address.innerText = project.address;

    name.setAttribute('class', 'card-title mb-1 text-center no-padding');
    name.innerText = project.project_name;

    link.setAttribute('href', '#')

    inner.setAttribute('class', 'card-body');
    inner.appendChild(name);
    inner.appendChild(status);
    inner.appendChild(address);

    link.appendChild(inner);
    if(project.status_name == "Paid"){
      item.setAttribute('class', 'card mb-2 paid full-width');
    }
    else if(project.status_name == "Not Reached"){
      item.setAttribute('class', 'card mb-2 not-reached full-width');
    }
    else if(project.status_name == "Appraisal Booked"){
      item.setAttribute('class', 'card mb-2 appraisal-booked full-width');
    }
    else if(project.status_name == "Waiting for Appraisal"){
      item.setAttribute('class', 'card mb-2 waiting-appraisal full-width');
    }
    else if(project.status_name == "Appraised"){
      item.setAttribute('class', 'card mb-2 appraised full-width');
    }
    else if(project.status_name == "Quote Sent"){
      item.setAttribute('class', 'card mb-2 quote-sent full-width');
    }
    else if(project.status_name == "Waiting for Alberta1Call"){
      item.setAttribute('class', 'card mb-2 waiting-alberta full-width');
    }
    else if(project.status_name == "Installation Pending"){
      item.setAttribute('class', 'card mb-2 install-pending full-width');
    }
    else if(project.status_name == "Installing"){
      item.setAttribute('class', 'card mb-2 installing full-width');
    }
    else if(project.status_name == "No Longer Interested"){
      item.setAttribute('class', 'card mb-2 not-interested full-width');
    }
    else{
      item.setAttribute('class', 'card mb-2 full-width');
    }
    final.setAttribute('class', 'less-padding card-row col-lg-4 col-md-6');

    // this is where you want to go when you click
    //item.setAttribute('onclick', 'window.location.href="{{ url_for('projects') }}"' )
    link.setAttribute('onclick', 'projectClicked('+project.project_id+')');
    link.setAttribute('oncontextmenu',
      'projectMenu(event,'+project.project_id+')');
    link.setAttribute('class', 'no-select');

    item.appendChild(link);
    final.appendChild(item);
    // Add it to the list:
    projectList.appendChild(final);
  });
}

function showError(){
  $('#projectlist').empty();
  var item = document.createElement('a');
  item.appendChild(document.createTextNode('No projects were found for this customer'));
  projectList.appendChild(item);

  var createNew = document.createElement('a');
  createNew.setAttribute('class', 'btn btn-primary btn-block')
  createNew.appendChild(document.createTextNode('Click here to start a new project'));
  createNew.setAttribute('href', "/newproject")
  projectList.appendChild(createNew);
}

//get customer info
function getCustInfo(){
  $.ajax({
      type: 'GET',
      url: '/getCustomer/' + cust_id,
      success: function(result) {
          $('#title').text(result[0].first_name);
          $('#phone').text(result[0].cellphone);
          $('#phone').attr('href', 'tel:' + escapeAngleBrackets(result[0].cellphone));
          $('#email').text(result[0].email);
          $('#email').attr('href', 'mailto:' + escapeAngleBrackets(result[0].email));
          $('#companyNameNav').text(result[0].company_name);
      },
      error: function(result) {
          noCustomer();
      }
  });
}

//get customers projects
function getProjects(){
  $.ajax({
      type: 'GET',
      url: '/getProjectList/' + cust_id + '?status=' + $('#status').val(),
      success: function(result) {
          updateProjects(result);
      },
      error: function(result) {
          showError();
      }
  });
}

$(document).ready(function(){
  var url = window.location.querystring;
  cust_id = getParameterByName('cust_id');
  if(cust_id == null) {
    noCustomer();
  }
  $("#pencil-button").removeClass('hide');
  $('#edit').click(function(){
    window.location.href = '/editcustomer?cust_id=' + cust_id;
  });
  getStatus();
  getCustInfo();
  getProjects();
});

//sort by this
$('#status').on('change', function() {
  getProjects();
});

function projectClicked(id) {
	window.location.href = '/projectinfo?proj_id=' + id;
}

function noCustomer(){
  $('#message').on('hidden.bs.modal', function() {
    window.location.href = '/customers';
  });

  showMessage("Customer does not exist.");
}
function projectMenu(event, id) {
  event.preventDefault();

	$('#edit-project').click(function() {
		window.location.href = '/editprojectinfo?proj_id=' + id;
	});

	$('#menu').modal('show');
}