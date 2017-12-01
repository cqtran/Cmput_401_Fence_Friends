var proj_id;

function getMaterialAmounts(layout){
  $.ajax({
    type: 'GET',
    url: '/materialAmounts/?layout_id=' + layout,
    success: function(result) {
      console.log("amounts: " + result)
    },
    error: function(result) {
        alert("shits fucked");
    }
  });
}
function getMaterials(appearance){
  $.ajax({
    type: 'GET',
    url: '/getMaterialLists/?appearance_id=' + appearance,
    success: function(result) {
      console.log(result)
    },
    error: function(result) {
        alert("material appearnce fucked");
    }
  });
}

function getProjectInfo() {
  $.ajax({
    type: 'GET',
    url: '/getproject/' + proj_id,
    success: function(result) {
      var layout = result[0].layout_selected;
      var appearance = result[].appearance_selected;
      console.log("layout: " + layout);
      console.log("appearance: " + appearance)
      getMaterials(layout);
      getMaterials(appearance);
    },
    error: function(result) {
        noProject();
    }
  });
}

$(document).ready(function(){
  proj_id = getParameterByName('proj_id');

  if(proj_id == null) {
    noProject();
  }
  getProjectInfo();

});

function noProject(){
  $('#message').on('hidden.bs.modal', function() {
    window.location.href = '/projects/';
  });
  showMessage("Project does not exist.");
}