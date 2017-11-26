// Send a request to get the list of inactive users
var requestList;

function dispUsers(users){
  requestList.empty();
  
  users.forEach(function(user) {
  requestList.append('\
    <a class="list-group-item list-group-item-action" onclick="confirmAccept(' + user.id + ')">\
      <strong>' + user.company_name + '</strong>\
      <div class="text-muted smaller">' + user.email + '</div>\
    </a>');
  })
}

function confirmAccept(id) {
  $('#accept-modal').modal('show');
  $('#accept-button').attr('onclick', 'acceptUser(' + id + ')');
}

function showError(){
  requestList.empty();
  var item = document.createElement('h6');
  item.appendChild(document.createTextNode('No account requests users were found.'));
  document.getElementById('generate-users').appendChild(item);
}

// POST request to accept the clicked inactive user
function acceptUser(id) {
  $('#accept-modal').modal('hide');
  $.ajax({
    type: 'POST',
    url: '/acceptUser/',
    data: { 
        user_id: id
    },
    datatype: 'json',
    success: function(result) {
      dispUsers(result);
    },
    error: function(result) {
        showError();
    }
  });
}

$(document).ready(function(){
  requestList = $('#generate-users');
  $.ajax({
    type: 'GET',
    url: '/getInactiveUsers/',
    success: function(result) {
      dispUsers(result);
    },
    error: function(result) {
        showError();
    }
  });
});

