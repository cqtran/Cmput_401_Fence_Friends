var _STATUS;
var chosenCustomers = [];
var proj_id;
var statusList; = document.getElementById('status');

var requestStatus = new XMLHttpRequest();
requestStatus.onreadystatechange = function(response) {
  if (requestStatus.readyState === 4) {
    if (requestStatus.status === 200) {
      // Parse the JSON
      var jsonStatus = JSON.parse(requestStatus.responseText);
      jsonStatus.forEach(function(status) {
        var item = document.createElement('option');
        item.setAttribute('value', status.status_name);
        item.innerHTML = status.status_name;
        // Add it to the list:
        statusList.appendChild(item);
        statusList.value = _STATUS;
        //$('.selectpicker').selectpicker('refresh'); 
    });
    }
  }
}
requestStatus.open('GET', '/getStatusList', true);
requestStatus.send()

var requestProj = new XMLHttpRequest();
requestProj.onreadystatechange = function(response) {
  if (requestProj.readyState === 4) {
    if (requestProj.status === 200) {
      // Parse the JSON
      var project = JSON.parse(requestProj.responseText);
function projectData(project){
  document.getElementById('project_id').value = project[0].project_id;
  document.getElementById('project_name').value = project[0].project_name;
  document.getElementById('address').value = project[0].address;
  _STATUS = project[0].status_name;
  document.getElementById('note').value = project[0].note;
}

requestProj.open('GET', '/getProject/' + proj_id, true);
requestProj.send();

function confirmDiscard() {
  return "Discard changes?";
}

function markDirty() {
  window.onbeforeunload = confirmDiscard;
}

function markClean() {
  window.onbeforeunload = null;
}
