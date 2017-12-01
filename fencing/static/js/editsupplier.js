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

function save() {
	$.ajax({
		type: 'POST',
		url: "/updatesupplier/",
		data: JSON.stringify({email: $("#email").val()}),
		contentType: "application/json;charset=UTF-8",
		dataType: "json",
		error: function(xhr, textStatus, error) {
			console.log(xhr.statusText);
			console.log(textStatus);
			console.log(error);
		}
	});
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

	$('#supplier-form').submit(function(e) {
		e.preventDefault();
		save();
		window.location.replace("/");
	  });
});