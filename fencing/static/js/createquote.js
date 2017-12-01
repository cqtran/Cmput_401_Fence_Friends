var proj_id;

function getMaterialAmounts(layout){
  $.ajax({
    type: 'GET',
    url: '/getMaterialAmounts/?layout_id=' + layout,
    success: function(result) {
      dealNumber(result["metal_post"], "metal_post");
      dealNumber(result["metal_u_channel"], "metal_u_channel");
      dealNumber(result["metal_lsteel"], "metal_lsteel");
      dealNumber(result["plastic_t_post"], "plastic_t_post");
      dealNumber(result["plastic_corner_post"], "plastic_corner_post");
      dealNumber(result["plastic_line_post"], "plastic_line_post");
      dealNumber(result["plastic_end_post"], "plastic_end_post");
      dealNumber(result["plastic_gate_post"], "plastic_gate_post");
      dealNumber(result["plastic_rail"], "plastic_rail");
      dealNumber(result["plastic_u_channel"], "plastic_u_channel");
      dealNumber(result["plastic_panel"], "plastic_panel");
      dealNumber(result["plastic_collar"], "plastic_collar");
      dealNumber(result["plastic_cap"], "plastic_cap");
      dealNumber(result["gate_hinge"], "gate_hinge");
      dealNumber(result["gate_latch"], "gate_latch");
      console.log(result["metal_post"]);
    },
    error: function(result) {
        showMessage("Error getting material amounts.");
    }
  });
}
function getMaterials(appearance){
  $.ajax({
    type: 'GET',
    url: '/getMaterialLists/?appearance_id=' + appearance,
    success: function(result) {
      dealLists(result["metal_post"], "metal_post");
      dealLists(result["metal_u_channel"], "metal_u_channel");
      dealLists(result["metal_lsteel"], "metal_lsteel");
      dealLists(result["plastic_t_post"], "plastic_t_post");
      dealLists(result["plastic_corner_post"], "plastic_corner_post");
      dealLists(result["plastic_line_post"], "plastic_line_post");
      dealLists(result["plastic_end_post"], "plastic_end_post");
      dealLists(result["plastic_gate_post"], "plastic_gate_post");
      dealLists(result["plastic_rail"], "plastic_rail");
      dealLists(result["plastic_u_channel"], "plastic_u_channel");
      dealLists(result["plastic_panel"], "plastic_panel");
      dealLists(result["plastic_collar"], "plastic_collar");
      dealLists(result["plastic_cap"], "plastic_cap");
      dealLists(result["gate_hinge"], "gate_hinge");
      dealLists(result["gate_latch"], "gate_latch");
    },
    error: function(result) {
        showMessage("Error getting material lists");
    }
  });
}

function getProjectInfo() {
  $.ajax({
    type: 'GET',
    url: '/getProject/' + proj_id,
    success: function(result) {
      var layout = result[0].layout_selected;
      var appearance = result[0].appearance_selected;
      console.log("layout: " + layout);
      console.log("appearance: " + appearance)
      getMaterialAmounts(layout);
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

function saveQuote(e) {
  var formdata = new FormData(document.getElementById("create-form"));
  $.ajax({
      type: 'POST',
      url: '/finalizeQuote/',
      data : formdata,
      processData: false,
      contentType: false,
      success: function(response){
        console.log('good')
        window.location.href = '/projectinfo/?proj_id=' + proj_id;
      },
      error: function(result){
        showMessage("Error saving data.");
      }
  });
}

function dealLists(types, name){
  types.forEach(function(type) {
    $('select[name=' + name + '-type]').append('<option value="' + type.material_id + '">' + type.material_name + '</option>');
  });
  $('.selectpicker').selectpicker('refresh');
}

function dealNumber(type, name){
  $('#' + name).val(type);
}

function noProject(){
  $('#message').on('hidden.bs.modal', function() {
    window.location.href = '/projects/';
  });
  showMessage("Project does not exist.");
}
function showMessage(message) {
  $('#message-text').html(message);
  $('#message').modal('show');
}

$('form').submit(function(e) {
  e.preventDefault();
  saveQuote(e);
});
