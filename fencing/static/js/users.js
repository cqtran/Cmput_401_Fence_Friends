// Send a request to get the list of inactive users
var requestList;

function dispUsers(users){
  requestList.empty();
  users.forEach(function(user) {
  requestList.append('\
    <a class="list-group-item list-group-item-action" onclick="confirmDeactivate(' + user.id + ')">\
      <strong>' + user.company_name + '</strong>\
      <div class="text-muted smaller">' + user.email + '</div>\
    </a>');
  })
}

function confirmDeactivate(id) {
  $('#accept-modal').modal('show');
  $('#accept-button').attr('onclick', 'deactivateUser(' + id + ')');
}

function showError(){
  requestList.empty();
  var item = document.createElement('h6');
  item.appendChild(document.createTextNode('No active users were found.'));
  document.getElementById('generate-users').appendChild(item);
}

// POST request to accept the clicked inactive user
function deactivateUser(id) {
  $('#accept-modal').modal('hide');
  $.ajax({
    type: 'POST',
    url: '/deactivateUser/',
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
    url: '/getActiveUsers/',
    success: function(result) {
      dispUsers(result);
    },
    error: function(result) {
        showError();
    }
  });
});