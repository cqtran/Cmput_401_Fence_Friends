// Send a request to get the list of inactive users
var requestList = document.getElementById('genereate-users')

function dispUsers(users){
  $('#genereate-users').empty();
  users.forEach(function(user) {
    var item = document.createElement('a');
    item.setAttribute('href', '#')
    item.setAttribute('id', user.id)
    item.setAttribute('class', 'list-group-item list-group-item-action');
    item.setAttribute('onclick', 'acceptUser('+user.id+')')
    item.appendChild(document.createTextNode(user.company_name));
    item.appendChild(document.createTextNode(" " + user.email));
    item.appendChild(document.createTextNode(" " + user.username));
    requestList.appendChild(item);
  })
}

// POST request to accept the clicked inactive user
function acceptUser(id) {
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
        alert("Failed");
    }
  });
}


$(document).ready(function(){
  $.ajax({
    type: 'GET',
    url: '/getInactiveUsers/',
    success: function(result) {
      dispUsers(result);
    },
    error: function(result) {
        alert("Failed");
    }
  });
});

