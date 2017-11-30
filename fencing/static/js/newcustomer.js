var isDirty = false;

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