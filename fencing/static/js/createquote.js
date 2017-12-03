var proj_id;
var listDict;
var amountDict;
var isDirty = true;

function markClean() {
  isDirty = false;
  window.onbeforeunload = null;
}

window.onbeforeunload = function() {
  return "Discard changes?";
};

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
    },
    error: function(result) {
        showMessage("Error getting material amounts. Are you sure you have a CSV uploaded? Check settings.");
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
        showMessage("Error getting material lists. Are you sure you have a CSV uploaded? Check settings.");
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

  $("#confirmDiscardSave").click(function() {
    $("#submit").trigger("click");
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

function saveQuote() {
  $.ajax({
      type: 'POST',
      url: '/finalizeQuote/',
      data: { 
          material_types: JSON.stringify(listDict),
          material_amounts: JSON.stringify(amountDict),
          proj_id: proj_id,
          misc_modifier: $('#adjustment').val()
      },
      dataType: "json",
      success: function(response){
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

function makeDictionary(){
  amountDict = {};
  listDict = {};
  amountDict["metal_post"] = $('#metal_post').val();
  amountDict["metal_u_channel"] = $('#metal_u_channel').val();
  amountDict["metal_lsteel"] = $('#metal_lsteel').val();
  amountDict["plastic_t_post"] = $('#plastic_t_post').val();
  amountDict["plastic_corner_post"] = $('#plastic_corner_post').val();
  amountDict["plastic_line_post"] = $('#plastic_line_post').val();
  amountDict["plastic_end_post"] = $('#plastic_end_post').val();
  amountDict["plastic_gate_post"] = $('#plastic_gate_post').val();
  amountDict["plastic_rail"] = $('#plastic_rail').val();
  amountDict["plastic_u_channel"] = $('#plastic_u_channel').val();
  amountDict["plastic_panel"] = $('#plastic_panel').val();
  amountDict["plastic_collar"] = $('#plastic_collar').val();
  amountDict["plastic_cap"] = $('#plastic_cap').val();
  amountDict["gate_hinge"] = $('#gate_hinge').val();
  amountDict["gate_latch"] = $('#gate_latch').val();

  listDict["metal_post"] = $('#metal_post-type').val();
  listDict["metal_u_channel"] = $('#metal_u_channel-type').val();
  listDict["metal_lsteel"] = $('#metal_lsteel-type').val();
  listDict["plastic_t_post"] = $('#plastic_t_post-type').val();
  listDict["plastic_corner_post"] = $('#plastic_corner_post-type').val();
  listDict["plastic_line_post"] = $('#plastic_line_post-type').val();
  listDict["plastic_end_post"] = $('#plastic_end_post-type').val();
  listDict["plastic_gate_post"] = $('#plastic_gate_post-type').val();
  listDict["plastic_rail"] = $('#plastic_rail-type').val();
  listDict["plastic_u_channel"] = $('#plastic_u_channel-type').val();
  listDict["plastic_panel"] = $('#plastic_panel-type').val();
  listDict["plastic_collar"] = $('#plastic_collar-type').val();
  listDict["plastic_cap"] = $('#plastic_cap-type').val();
  listDict["gate_hinge"] = $('#gate_hinge-type').val();
  listDict["gate_latch"] = $('#gate_latch-type').val();
}
$('#submit').click(function(){
  makeDictionary();
  saveQuote();
});