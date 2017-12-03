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
		url: "/updatecompany/",
		data: JSON.stringify({
			supplier_email: $("#supplier-email").val(),
			office: $("#office").val(),
			phone: $("#phone").val(),
			web: $("#web").val(),
			disclaimer: $("#disclaimer").val()
		}),
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

	$('#company-form').submit(function(e) {
		e.preventDefault();
		save();
		window.location.replace("/");
	  });
});