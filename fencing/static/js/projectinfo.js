var saveLoadedAppearance = false;

var supplierEmail;

var attachmentPathLength = 20;
var pdfs = [];

var confirmed = false;

var firstLayout = "1";
var firstAppearance = "1";

var activeLayout = "1";
var activeAppearance = "1";

var lastLayout = "1";
var lastAppearance = "1";

var deletedLayout = null;
var deletedAppearance = null;

var layoutCount = 1;
var appearanceCount = 1;
var tabLimit = 15;

var drawiopic;
var imgPath;
var tbnPath;
var pictureList;
var proj_id;

var finalized = false;

var punctuation = "\\.,\\)\\?\"':\\!;\\]\\}";

var urlRegex =
	RegExp(
		"(?:^|\\s)https?:\\/\\/[^\\s]+?(?=[" + punctuation + "]?(?:$|\\s))",
		"g"
	);
var urlReplacement = '<a class="text-primary" href="$&" target="_blank">$&</a>';

// From:
// https://stackoverflow.com/questions/24816/escaping-html-strings-with-jquery/12034334#12034334
// Accessed November 21, 2017
var entityMap = {
	'&': '&amp;',
	'<': '&lt;',
	'>': '&gt;',
	'"': '&quot;',
	"'": '&#39;',
	'/': '&#x2F;',
	'`': '&#x60;',
	'=': '&#x3D;'
};

var angleBracketMap = {
	'<': '&lt;',
	'>': '&gt;'
}

function setConfirmed() {
	confirmed = true;
}

function onConfirm(f, message, title) {
	if (message == null) {
		message = '';
	}

	if (title == null) {
		title = '';
	}

	$('#confirmMessage').html(message);
	$('#confirmTitle').html(title);
	var modal = $('#confirm');
	modal.modal('show');

	modal.one('hidden.bs.modal',
		function() {
			if (confirmed) {
				confirmed = false;
				f();
			}
		}
	);
}

function onInput(f, prompt, defaultValue) {
	if (prompt == null) {
		prompt = '';
	}

	$('#inputTitle').html(prompt);
	var modal = $('#input');
	var inputText = $('#inputText');
	modal.modal('show');

	if (defaultValue == null) {
		defaultValue = '';
	}

	inputText.val(defaultValue);

	modal.one('hidden.bs.modal',
		function() {
			var text = inputText.val().trim();
			if (text == '') {
				text = defaultValue;
			}
			f(text);
		}
	);
}

function closeInput() {
	$('#inputOkay').click();
}

function showMessage(message) {
	$('#message-text').html(message);
	$('#message').modal('show');
}

// From:
// https://stackoverflow.com/questions/24816/escaping-html-strings-with-jquery/12034334#12034334
// Accessed November 21, 2017
function escapeHtml(string) {
	return String(string).replace(/[&<>"'`=\/]/g, function (s) {
		return entityMap[s];
	});
}

function escapeAngleBrackets(string) {
	return String(string).replace(/[<>]/g, function (s) {
		return angleBracketMap[s];
	});
}

function setActiveLayout(number) {
	if (number == deletedLayout) {
		deletedLayout = null;
		return;
	}

	activeLayout = number;
	saveLayoutSelection();
}

function setActiveAppearance(number) {
	if (number == deletedAppearance) {
		deletedAppearance = null;
		return;
	}

	activeAppearance = number;
	saveAppearanceSelection();
}

function editLayoutName(number) {
	if (finalized) {
		showMessage("Cannot edit finalized projects");
		return;
	}

	setLayoutName(number, false, null, layoutCount == 1);
}

function editAppearanceName(number) {
	if (finalized) {
		showMessage("Cannot edit finalized projects");
		return;
	}

	setLayoutName(number, false, null, appearanceCount == 1);
}

function setLayoutName(number, loading, newName, noClose) {
	if (newName == null) {
		var f = function(input) {
			setLayoutName_(number, loading, input, noClose);
		}
		
		var tab = document.getElementById("layout-tab" + activeLayout);
		onInput(f, "Layout Name", tab.layoutName);
	}

	else {
		setLayoutName_(number, loading, newName, noClose);
	}
}

function setLayoutName_(number, loading, newName, noClose) {
	var tab = document.getElementById("layout-tab" + number);
	var tabText = tab.children[0];
	var bodyText = document.getElementById("layout" + number).children[0];

	if (newName != null) {

		newName = escapeAngleBrackets(newName);

		tab.layoutName = newName;

		if (noClose) {
			tabText.innerHTML = newName;
		}

		else {
			tabText.innerHTML = '<button class="close closeTab" onclick="removeLayout(\'' + number + '\')" type="button">×</button>' + newName;
		}

		if (!loading) {
			saveActiveLayoutName();
		}
	}
}

function setAppearanceName(number, loading, newName, noClose) {
	if (newName == null) {
		var f = function(input) {
			setAppearanceName_(number, loading, input, noClose);
		}

		var tab = document.getElementById("appearance-tab" + activeAppearance);
		onInput(f, "Appearance Name", tab.appearanceName);
	}

	else {
		setAppearanceName_(number, loading, newName, noClose);
	}
}

function setAppearanceName_(number, loading, newName, noClose) {
	var tab = document.getElementById("appearance-tab" + number);
	var tabText = tab.children[0];
	var bodyText = document.getElementById("appearance" + number).children[0];

	if (newName != null) {

		newName = escapeAngleBrackets(newName);

		tab.appearanceName = newName;

		if (noClose) {
			tabText.innerHTML = newName;
		}

		else {
			tabText.innerHTML = '<button class="close closeTab" onclick="removeAppearance(\'' + number + '\')" type="button">×</button>' + newName;
		}

		if (!loading) {
			saveActiveAppearance();
		}
	}
}

function setActiveLayoutId(dbId) {
	document.getElementById("layout-tab" + activeLayout).dbId =
		dbId.toString();
}

function setActiveDisplayStrings(displayStrings) {
	var display = $("#layout" + activeLayout).find("p:first");
	display.html("");
	var hr = $("#layout" + activeLayout).find("hr:first");
	
	if (displayStrings.length == 0) {
		hr.css("display", "none");
		return;
	}

	hr.css("display", "block");
	var string;

	for (var i = 0; i < displayStrings.length; i++) {
		string = "<b>" + displayStrings[i].replace("×", "×</b>").replace(
			"(Removal)", "<span style='color:grey;'>(Removal)</span>");
		display.append(string + "<br>");
	}
}

function setActiveAppearanceId(dbId) {
	document.getElementById("appearance-tab" + activeAppearance).dbId =
		dbId.toString();
}

function addLayout(loading) {
	if (finalized) {
		showMessage("Cannot edit finalized projects");
		return;
	}

	if (layoutCount >= tabLimit) {
		showMessage(
			"Cannot have more than " + tabLimit.toString() + " layouts");
		return;
	}

	var active = document.getElementById("layout" + activeLayout);
	var activeTab = document.getElementById("layout-tab" + activeLayout);
	var activeLink = activeTab.children[0];
	lastLayout = (parseInt(lastLayout) + 1).toString();
	activeLayout = lastLayout;

	var clone = active.cloneNode(true);
	clone.id = "layout" + lastLayout;
	clone.children[0].setAttribute("onclick",
		"editLayoutName('" + lastLayout + "')");
	clone.children[1].children[0].id = "image" + lastLayout;
	document.getElementById("layouts").appendChild(clone);

	var cloneTab = activeTab.cloneNode(true);
	cloneTab.id = "layout-tab" + lastLayout;
	cloneTab.setAttribute("onclick", "setActiveLayout('" + lastLayout + "')");
	cloneTab.setAttribute("oncontextmenu", "layoutMenu(event, '" + lastLayout + "')");
	var link = cloneTab.children[0];
	link.href = "#layout" + lastLayout;
	link.innerHTML = '<button class="close closeTab" onclick="removeLayout(\'' + lastLayout + '\')" type="button">×</button>Untitled';
	document.getElementById("layout-tabs").insertBefore(cloneTab,
		document.getElementById("add-layout"));
	cloneTab.layoutName = "Untitled";

	activeLink.classList.remove("active");
	active.classList.remove("active");
	active.classList.remove("show");

	layoutCount += 1;

	if (!loading) {
		var f = function(input) {
			setLayoutName_(activeLayout, true, input);
			saveActiveLayout(true);
			setLayoutCloseButton();
		}
		
		onInput(f, "Layout Name", "Untitled");
	}
}

function addAppearance(loading) {
	if (finalized) {
		showMessage("Cannot edit finalized projects");
		return;
	}

	if (appearanceCount >= tabLimit) {
		showMessage(
			"Cannot have more than " + tabLimit.toString() + " appearances");
		return;
	}

	var active = document.getElementById("appearance" + activeAppearance);
	var activeTab = document.getElementById("appearance-tab" + activeAppearance);
	var activeLink = activeTab.children[0];
	lastAppearance= (parseInt(lastAppearance) + 1).toString();
	activeAppearance = lastAppearance;

	var clone = active.cloneNode(true);
	clone.id = "appearance" + lastAppearance;
	clone.children[0].setAttribute("onclick",
		"editAppearanceName('" + lastAppearance + "')");

	document.getElementById("appearances").appendChild(clone);

	var cloneTab = activeTab.cloneNode(true);
	cloneTab.id = "appearance-tab" + lastAppearance;
	cloneTab.setAttribute("onclick", "setActiveAppearance('" + lastAppearance + "')");
	cloneTab.setAttribute("oncontextmenu", "appearanceMenu(event, '" + lastLayout + "')");
	var link = cloneTab.children[0];
	link.href = "#appearance" + lastAppearance;
	link.innerHTML = '<button class="close closeTab" onclick="removeAppearance(\'' + lastAppearance + '\')" type="button">×</button>Untitled';
	document.getElementById("appearance-tabs").insertBefore(cloneTab,
		document.getElementById("add-appearance"));
	cloneTab.appearanceName = "Untitled";

	activeLink.classList.remove("active");
	active.classList.remove("active");
	active.classList.remove("show");

	appearanceCount += 1;

	if (!loading) {
		var f = function(input) {
			setAppearanceName_(activeAppearance, true, input);
			saveActiveAppearance(true);
			setAppearanceCloseButton();
		}
		
		onInput(f, "Appearance Name", "Untitled");
	}
}

function removeLayout(number) {
	if (finalized) {
		showMessage("Cannot edit finalized projects");
		return;
	}

	var f = function() {
		removeLayout_(number);
	}
	
	onConfirm(f, "Clicking delete will permanently delete the layout.",
		"Delete Layout?");
}

function setLayoutCloseButton() {
	var tab = document.getElementById("layout-tab" + firstLayout);
	setLayoutName(firstLayout, true, tab.layoutName, layoutCount == 1);
}

function setAppearanceCloseButton() {
	var tab = document.getElementById("appearance-tab" + firstAppearance);
	setAppearanceName(firstAppearance, true, tab.appearanceName,
		appearanceCount == 1);
}

function removeLayout_(number) {
	removeLayoutFromDb(number);

	var layout;

	if (firstLayout == number) {
		layout = $("#layout" + firstLayout).next();
		firstLayout = layout.attr("id").slice(6);
	}

	var element = document.getElementById("layout" + number);
	element.parentNode.removeChild(element);
	element = document.getElementById("layout-tab" + number);
	element.parentNode.removeChild(element);

	if (activeLayout == number) {
		setActiveLayout(firstLayout);
		layout = document.getElementById("layout" + firstLayout);
		var layoutTab = document.getElementById("layout-tab" + firstLayout);
		layout.classList.add("active");
		layout.classList.add("show");
		layoutTab.children[0].classList.add("active");
	}

	deletedLayout = number;
	layoutCount -= 1;
	setLayoutCloseButton();
}

function removeAppearance(number) {
	if (finalized) {
		showMessage("Cannot edit finalized projects");
		return;
	}

	var f = function() {
		removeAppearance_(number);
	}
	
	onConfirm(f, "Clicking delete will permanently delete the appearance.",
		"Delete Appearance?");
}

function removeAppearance_(number) {
	removeAppearanceFromDb(number);

	var appearance;

	if (firstAppearance == number) {
		appearance = $("#appearance" + firstAppearance).next();
		firstAppearance = appearance.attr("id").slice(10);
	}

	var element = document.getElementById("appearance" + number);
	element.parentNode.removeChild(element);
	element = document.getElementById("appearance-tab" + number);
	element.parentNode.removeChild(element);

	if (activeAppearance == number) {
		setActiveAppearance(firstAppearance);
		appearance = document.getElementById("appearance" + firstAppearance);
		var appearanceTab = document.getElementById(
			"appearance-tab" + firstAppearance);
		appearance.classList.add("active");
		appearance.classList.add("show");
		appearanceTab.children[0].classList.add("active");
	}

	deletedAppearance = number;
	appearanceCount -= 1;
	setAppearanceCloseButton();
}

function reloadPage() {
	location.reload();
}

function deleteOtherLayouts(number) {
	$('#menu').modal('hide');

	var numbers = [];
	var n = null;
	$("[id^=layout-tab]").each(function(index, element) {
		if (element.id == "layout-tabs") {
			return;
		}

		n = element.id.slice(10);

		if (n == number) {
			return;
		}

		numbers.push(n);
	});

	var f = function() {
		for (var i = 0; i < numbers.length; i++) {
			removeLayout_(numbers[i]);
		}
	};

	onConfirm(f, "Clicking delete will permanently delete all other layouts.",
		"Delete Other Layouts?");
}

function deleteOtherAppearances(number) {
	$('#menu').modal('hide');

	var numbers = [];
	var n = null;
	$("[id^=appearance-tab]").each(function(index, element) {
		if (element.id == "appearance-tabs") {
			return;
		}

		n = element.id.slice(14);

		if (n == number) {
			return;
		}

		numbers.push(n);
	});

	var f = function() {
		for (var i = 0; i < numbers.length; i++) {
			removeAppearance_(numbers[i]);
		}
	};

	onConfirm(f, "Clicking delete will permanently delete all other appearances.",
		"Delete Other Appearances?");
}

function layoutMenu(event, number) {
	event.preventDefault();

	$('#rename').one("click", function() {
		editLayoutName(number);
	});

	$('#delete-others').one("click", function() {
		deleteOtherLayouts(number);
	});

	$('#menu').modal('show');
}

function appearanceMenu(event, number) {
	event.preventDefault();

	$('#rename').one("click", function() {
		editAppearanceName(number);
	});


	$('#delete-others').one("click", function() {
		deleteOtherAppearances(number);
	});

	$('#menu').modal('show');
}

function saveActiveLayoutName() {
	var tab = document.getElementById("layout-tab" + activeLayout);
	var layout_id = tab.dbId;
	var layout_name = tab.layoutName;
	var dat = JSON.stringify({layoutId: layout_id, name: layout_name});

	$.ajax({
      type: 'POST',
      url: "/saveLayoutName/",
      data: dat,
	  contentType: "application/json;charset=UTF-8",
	  dataType: "json",
	    error: function(xhr, textStatus, error) {
			console.log(xhr.statusText);
			console.log(textStatus);
			console.log(error);
      }
  });
}

function saveActiveLayout(includeSelection) {
	if (finalized) {
		showMessage("Cannot edit finalized projects");
		return;
	}

	var img = document.getElementById("image" + activeLayout).getAttribute('src');
	var tab = document.getElementById("layout-tab" + activeLayout);
	var layout_id = tab.dbId;
	var layout_name = tab.layoutName;
	var dat = {image: img, layoutId: layout_id, name: layout_name};

	if (includeSelection) {
		dat["saveSelection"] = "true";
	}

	var dat = JSON.stringify(dat);

	$.ajax({
    type: 'POST',
    url: "/saveDiagram/?proj_id=" + proj_id,
    data: dat,
	  contentType: "application/json;charset=UTF-8",
	  dataType: "json",
    success: function(result) {
			if (result["reload"]) {
				reloadPage();
			}
			else {
				setActiveLayoutId(result["layoutId"]);
				setActiveDisplayStrings(result["displayStrings"]);
			}
    },
    error: function(xhr, textStatus, error) {
			console.log(xhr.statusText);
			console.log(textStatus);
			console.log(error);
      }
  });
}

function saveActiveAppearance(includeSelection) {
	if (finalized) {
		$("#message").on("hidden.bs.modal", function() {
			reloadPage();
		});
		showMessage("Cannot edit finalized projects");
		return;
	}

	var tab = document.getElementById("appearance-tab" + activeAppearance);
	var appearance_id = tab.dbId;
	var appearance_name = tab.appearanceName;
	var form = $("#appearance" + activeAppearance + " > div");
	var basePrice = form.find("#basePrice").val();
	var height = form.find("#height").val();
	var style = form.find("#style").val();
	var borderColor = form.find("#borderColor").val();
	var panelColor = form.find("#panelColor").val();
	var dat = {
		appearanceId: appearance_id,
		name: appearance_name,
		basePrice: basePrice,
		height: height,
		style: style,
		borderColor: borderColor,
		panelColor: panelColor
	};

	if (includeSelection) {
		dat["saveSelection"] = "true";
	}

	var dat = JSON.stringify(dat);

	$.ajax({
    type: 'POST',
    url: "/saveAppearance/?proj_id=" + proj_id,
    data: dat,
	  contentType: "application/json;charset=UTF-8",
	  dataType: "json",
    success: function(result) {
			setActiveAppearanceId(result["appearanceId"]);
    },
    error: function(xhr, textStatus, error) {
			console.log(xhr.statusText);
			console.log(textStatus);
			console.log(error);
    }
  });
}

function removeLayoutFromDb(number) {
	var tab = document.getElementById("layout-tab" + number);
	var layout_id = tab.dbId;
	var dat = JSON.stringify({layoutId: layout_id});
	$.ajax({
		type: 'POST',
		url: "/removeLayout/?proj_id=" + proj_id,
		data: dat,
		contentType: "application/json;charset=UTF-8",
		dataType: "json",
		error: function(xhr, textStatus, error) {
			showMessage("Error");
			console.log(xhr.statusText);
			console.log(textStatus);
			console.log(error);
		}
	});
}

function removeAppearanceFromDb(number) {
	var tab = document.getElementById("appearance-tab" + number);
	var appearance_id = tab.dbId;
	var dat = JSON.stringify({appearanceId: appearance_id});
	$.ajax({
		type: 'POST',
		url: "/removeAppearance/?proj_id=" + proj_id,
		data: dat,
		contentType: "application/json;charset=UTF-8",
		dataType: "json",
		error: function(xhr, textStatus, error) {
			showMessage("Error");
			console.log(xhr.statusText);
			console.log(textStatus);
			console.log(error);
		}
	});
}

function loadLayout(layout, number) {
	document.getElementById("image" + number).src = layout.layout_info;
	setLayoutName(number, true, layout.layout_name);
	document.getElementById("layout-tab" + number).dbId = layout.layout_id;
}

function loadLayouts(layouts, displayStrings){
	loadLayout(layouts[0], "1");
	setActiveDisplayStrings(displayStrings[0]);
	var currentLayout = 2;

	for(var i = 1; i < layouts.length; i++) {
		addLayout(true);
		loadLayout(layouts[i], currentLayout.toString());
		setActiveDisplayStrings(displayStrings[i]);
		currentLayout++;
	}

	setLayoutCloseButton();
}

function setDropdownValue(dropdown, value) {
	if (value == null) {
		dropdown.val(dropdown.find("option:first").val());
		saveLoadedAppearance = true;
	}

	else {
		dropdown.val(value);
	}
}

function loadAppearance(appearance, number) {
	var form = $("#appearance" + number + " > div");
	setDropdownValue(form.find("#basePrice"), appearance.base_price);
	setDropdownValue(form.find("#height"), appearance.height);
	setDropdownValue(form.find("#style"), appearance.style);
	setDropdownValue(form.find("#borderColor"), appearance.border_colour);
	setDropdownValue(form.find("#panelColor"), appearance.panel_colour);
	setAppearanceName(number, true, appearance.appearance_name);
	document.getElementById("appearance-tab" + number).dbId =
		appearance.appearance_id;
	
	if (saveLoadedAppearance) {
		saveActiveAppearance();
		saveLoadedAppearance = false;
	}
}

function loadAppearances(appearances){
	loadAppearance(appearances[0], "1");
	var currentAppearance = 2;

	for(var i = 1; i < appearances.length; i++) {
		addAppearance(true);
		loadAppearance(appearances[i], currentAppearance.toString());
		currentAppearance++;
	}

	setAppearanceCloseButton();
}

function setProjectInfo(project){
	document.getElementById('project-name').innerHTML =
		escapeHtml(project[0].project_name);
	document.getElementById('status').innerHTML =
		"■ " + escapeHtml(project[0].status_name);
	document.getElementById('address').innerHTML =
		escapeHtml(project[0].address);
		document.getElementById('address').href = 'https://www.google.com/maps/place/'+project[0].address;
	document.getElementById('start-date').innerHTML =
		escapeHtml(project[0].start_date);
	if(project[0].status_name == "Paid"){
	  document.getElementById("status").setAttribute('class', 'float-right paid-text text-grey');
	}
	else if(project[0].status_name == "Not Reached"){
	  document.getElementById("status").setAttribute('class', 'float-right not-reached-text text-grey');
	}
	else if(project[0].status_name == "Appraisal Booked"){
	  document.getElementById("status").setAttribute('class', 'float-right appraisal-booked-text text-grey');
	}
	else if(project[0].status_name == "Waiting for Appraisal"){
	  document.getElementById("status").setAttribute('class', 'float-right waiting-appraisal-text text-grey');
	}
	else if(project[0].status_name == "Appraised"){
	  document.getElementById("status").setAttribute('class', 'float-right appraised-text text-grey');
	}
	else if(project[0].status_name == "Quote Sent"){
	  document.getElementById("status").setAttribute('class', 'float-right quote-sent-text text-grey');
	}
	else if(project[0].status_name == "Waiting for Alberta1Call"){
	  document.getElementById("status").setAttribute('class', 'float-right waiting-alberta-text text-grey');
	}
	else if(project[0].status_name == "Installation Pending"){
	  document.getElementById("status").setAttribute('class', 'float-right install-pending-text text-grey');
	}
	else if(project[0].status_name == "Installing"){
	  document.getElementById("status").setAttribute('class', 'float-right installing-text text-grey');
	}
	else if(project[0].status_name == "No Longer Interested"){
	  document.getElementById("status").setAttribute('class', 'float-right not-interested-text text-grey');
	}

	// Sets the project_id into the uploadpicture form
	document.getElementById('project_id').setAttribute('value', proj_id);

	if (project[0].end_date != null) {
		document.getElementById('end_date').innerHTML =
			escapeHtml(project[0].end_date);
	}
	var note = project[0].note;
	if (note == null) {
		note = "";
	}
	note = escapeAngleBrackets(note).replace(urlRegex, urlReplacement);
	if (note.trim() != "") {
		document.getElementById('savednote').innerHTML = note;
		document.getElementById('noteContainer').style.display = "block";
	}
}

function makeNewPictureButton() {
	var img = document.createElement('img');
	var final = document.createElement('a');

	img.height = '50';
	img.width = '50';
	img.src = tbnPath + "New_Picture.png";
	img.alt = 'Thumbnail not found';
	final.setAttribute('href', '#');
	final.setAttribute('class', 'PictureThumbnail newPicture zero-padding');

	final.addEventListener('click', function(event){
		$("#file-upload").click();
		event.preventDefault();
	});

	final.appendChild(img);
	pictureList.appendChild(final);
}

function makePictures(pictures) {
	$('#projectPictures').empty();
	makeNewPictureButton();

	pictures.forEach(function(picture) {
		var img = document.createElement('img');
		var final = document.createElement('a');

		img.src = tbnPath + picture.thumbnail_name;
		img.alt = 'Thumbnail not found';
		final.setAttribute('href', '#');
		final.setAttribute('class', 'PictureThumbnail card zero-padding');
		// this is where you want to go when you click
		final.addEventListener('click', function(){
		$('#imagepreview').attr('src', imgPath + picture.file_name);
				$('#imagepopup').modal('show');
		});
		//link.setAttribute('onclick', 'customerClicked('+customer.customer_id+')')
		final.appendChild(img);

		//img.className += 'img-thumbnail'
		// Add it to the list:
		pictureList.appendChild(final);
	})
}

function imagesError(){
	$('#projectPictures').empty();
	makeNewPictureButton();
}

function editDiagram(image) {
	if (finalized) {
		showMessage("Cannot edit finalized projects");
		return;
	}

	var initial = image.getAttribute('src');
	image.setAttribute('src', 'https://fencythat.cavalryfence.ca/images/ajax-loader.gif');
	var iframe = document.createElement('iframe');
	iframe.setAttribute('style', "position:fixed; top:0px; left:0px; bottom:0px; right:0px; width:100%; height:100%; border:none; margin:0; padding:0; overflow:hidden; z-index:999999;")
	//iframe.setAttribute('frameborder', '0');
	//iframe.setAttribute('width', '80%');
	//iframe.setAttribute('height', '1000');
	//iframe.setAttribute('align', 'right');

	var close = function() {
		image.setAttribute('src', initial);
		document.body.removeChild(iframe);
		window.removeEventListener('message', receive);
	};
	var receive = function(evt) {
		if (evt.data.length > 0) {
			var msg = JSON.parse(evt.data);

			if (msg.event == 'init') {
				iframe.contentWindow.postMessage(JSON.stringify({action: 'load',
					xml: initial}), '*');
			}
			else if (msg.event == 'export') {
				close();
				image.setAttribute('src', msg.data);
				save(location.href);
				saveActiveLayout();
			}
			else if (msg.event == 'save') {
				iframe.contentWindow.postMessage(JSON.stringify({action: 'export',
					format: 'xmlsvg', spin: 'Updating page'}), '*');
			}
			else if (msg.event == 'exit') {
				close();
			}
		}
	};
	window.addEventListener('message', receive);
	iframe.setAttribute('src', 'https://fencythat.cavalryfence.ca//?embed=1&ui=atlas&spin=1&modified=unsavedChanges&proto=json');
	document.body.appendChild(iframe);
};

function save(url) {
	if (url != null) {
		var req = new XMLHttpRequest();
		req.withCredentials = true;
		var wnd = (url != window.location.href) ? window.open() : null;

		req.onreadystatechange = function() {
			if (req.readyState == 4) {
				if (req.status != 200 && req.status != 201) {
					if (wnd != null) {
						wnd.close();
					}
					showMessage('Error ' + req.status);
				}
				else if (wnd != null) {
					wnd.location.href = url;
				}
			}
		};
		req.open('PUT', url, true);
		req.send(document.documentElement.outerHTML);
	}
}

//get project info
function getProjects(){
  $.ajax({
      type: 'GET',
      url: '/getProject/' + proj_id,
      success: function(result) {
		finalized = result[0].finalize;
		updateFinalized(true);
        setProjectInfo(result);
      },
      error: function(xhr, textStatus, error) {
		if (proj_id != null) {
			noProject();
		}

		console.log(xhr.statusText);
		console.log(textStatus);
		console.log(error);
      }
  });
}

//get details
function moreDetails(){
  $.ajax({
      type: 'GET',
      url: '/projectdetails/' + proj_id,
      success: function(result) {
    	imgPath = result[0].replace(/^'(.*)'$/, '$1');
		tbnPath = result[1].replace(/^'(.*)'$/, '$1');
		loadAppearanceValues(result[10], result[11], result[12]);
		var layouts = result[2];
		var appearances = result[3];
		$('#companyNameNav').text(result[4]);
		var selectedLayout = result[5];
		var selectedAppearance = result[6];
		var displayStrings = result[7];
		var customerName = $('#customer-name');
		customerName.text(result[8]);
		var oldHref = customerName.attr('href');
		customerName.attr('href', oldHref + result[9] + '&status=All');
		supplierEmail = result[13];
		getPics();
		loadLayouts(layouts, displayStrings);
		loadAppearances(appearances);
		selectLayout(selectedLayout, layouts);
		selectAppearance(selectedAppearance, appearances);
      },
      error: function(xhr, textStatus, error) {
		if (proj_id != null) {
			showMessage("Error");
		}
		
		console.log(xhr.statusText);
		console.log(textStatus);
		console.log(error);
      }
  });
}

function makeOption(value, addFeet) {
	var feet = "'";

	if (!addFeet) {
		feet = '';
	}

	value = escapeAngleBrackets(value);
	return '<option value="' + value + '">' + value + feet + '</option>';
}

function loadAppearanceValues(heights, styles, colours) {
	var form = $("#appearance1 > div");
	var height = form.find("#height");
	var style = form.find("#style");
	var borderColor = form.find("#borderColor");
	var panelColor = form.find("#panelColor");
	var i;

	height.empty();
	style.empty();
	borderColor.empty();
	panelColor.empty();

	for (i = 0; i < heights.length; i++) {
		height.append(makeOption(heights[i], true));
	}

	for (i = 0; i < styles.length; i++) {
		style.append(makeOption(styles[i]));
	}

	for (i = 0; i < colours.length; i++) {
		borderColor.append(makeOption(colours[i]));
		panelColor.append(makeOption(colours[i]));
	}
}

//get details
function getPics(){
  $.ajax({
      type: 'GET',
      url: '/getPictureList/' + proj_id,
      success: function(result) {
      	makePictures(result);
      },
      error: function(xhr, textStatus, error) {
		console.log(xhr.statusText);
		console.log(textStatus);
		console.log(error);
        imagesError();
      }
  });
}

function uploadPicture(e) {
  var formdata = new FormData(document.getElementById("upload-form"));
  $.ajax({
      type: 'POST',
      url: '/uploadPicture/',
      data : formdata,
      processData: false,
      contentType: false,
      success: function(response){
      	getPics();
      }
  });
}

function deletePicture(e) {
	var image = document.getElementById("imagepreview");
	var imageNameArr = image.src.split("/");
	var imageName = imageNameArr[imageNameArr.length-1]
	console.log(imageName)

	$.ajax({
			type: 'DELETE',
			url: '/deletePicture/?picName=' + imageName + "&proj_id=" + proj_id,
			processData: false,
			contentType: false,
			success: function(response){
				getPics();
			}
	});
}

function saveLayoutSelection() {
	var selectedId = document.getElementById("layout-tab" + activeLayout).dbId;
	var selectionData = JSON.stringify({selected: selectedId});
	$.ajax({
		type: 'POST',
		url: "/saveLayoutSelection/?proj_id=" + proj_id,
		data: selectionData,
		contentType: "application/json;charset=UTF-8",
		dataType: "json"
	});
}

function saveAppearanceSelection() {
	var selectedId =
		document.getElementById("appearance-tab" + activeAppearance).dbId;
	var selectionData = JSON.stringify({selected: selectedId});
	$.ajax({
		type: 'POST',
		url: "/saveAppearanceSelection/?proj_id=" + proj_id,
		data: selectionData,
		contentType: "application/json;charset=UTF-8",
		dataType: "json"
	});
}

function selectLayout(layoutId) {
	var tabs = document.getElementById("layout-tabs");
	var tab;

	for (var i = 0; i < tabs.children.length; i++) {
		if (tabs.children[i].dbId == layoutId) {
			tab = tabs.children[i];
			break;
		}
	}

	document.getElementById(
		"layout-tab" + activeLayout).children[0].classList.remove("active");
	document.getElementById("layout" + activeLayout).classList.remove("active");
	document.getElementById("layout" + activeLayout).classList.remove("show");

	activeLayout = tab.id.slice(10);
	document.getElementById("layout" + activeLayout).classList.add("active");
	document.getElementById("layout" + activeLayout).classList.add("show");
	document.getElementById(
		"layout-tab" + activeLayout).children[0].classList.add("active");
}

function selectAppearance(appearanceId) {
	var tabs = document.getElementById("appearance-tabs");
	var tab;
	for (var i = 0; i < tabs.children.length; i++) {
		if (tabs.children[i].dbId == appearanceId) {
			tab = tabs.children[i];
			break;
		}
	}

	document.getElementById("appearance-tab" + activeAppearance)
		.children[0].classList.remove("active");
	document.getElementById("appearance" + activeAppearance)
		.classList.remove("active");
	document.getElementById("appearance" + activeAppearance)
		.classList.remove("show");

	activeAppearance = tab.id.slice(14);
	document.getElementById("appearance" + activeAppearance)
		.classList.add("active");
	document.getElementById("appearance" + activeAppearance)
		.classList.add("show");
	document.getElementById("appearance-tab" + activeAppearance)
		.children[0].classList.add("active");
}

function addPdf(url) {
	pdfs.push(url.slice(attachmentPathLength));
}

//this runs after the html has loaded, all function calls should be in here
$(document).ready(function(){
  pictureList = document.getElementById('projectPictures');
  proj_id = getParameterByName('proj_id');

  if(proj_id == null) {
  	noProject();
  }

  $("#pencil-button").removeClass('hide');
  $('#edit').click(function(){
    window.location.href= '/editprojectinfo?proj_id=' + proj_id;
  });

  moreDetails();
  getProjects();

  $('#material-list-send').click(function(e) {
	sendMaterialList();
  });

  $('#input').on('shown.bs.modal', function() {
	var inputText = $('#inputText');
	inputText.focus();
	inputText.select();
  });

  $('#material-list-modal').on('shown.bs.modal', function() {
	var email = $('#material-list-email');
	email.focus();
	email.select();
  });
});

$('#imagepopup').on('click', '.btn-ok', function(e) {
		console.log("Delete Picture");
		deletePicture(e);
});

$('#imagepopup').on('shown.bs.modal', function (event) {
  var vert = ($(window).height() - $(this).find('#image-modal').outerHeight())/2;
  var hor = ($(window).width() - $('.imagemodal').outerWidth())/2;
  console.log("winh" + $(window).height());
  console.log("winw" + $(window).width());
  console.log("vert" + $(this).find('#image-modal').outerHeight());
  console.log("hor" + $('.imagemodal').outerWidth());
  $('#image-dialog').css({"margin-left" : hor, "margin-right" : hor, "margin-top" : vert, "margin-bottom" : vert});
});
$('#file-upload').change(function(){
	$('#upload-form').submit();
});
$('#upload-form').submit(function(e) {
  e.preventDefault();
  uploadPicture(e);
});

$('#view-quote').submit(function(e) {
	e.preventDefault();

	$.ajax({
    type: 'POST',
    url: "/viewQuote/?proj_id=" + proj_id,
	contentType: "application/json;charset=UTF-8",
	dataType: "json",
    success: function(result) {
		if (result["reload"]) {
			reloadPage();
		}
		else {
			addPdf(result['url']);
			window.open(result['url']);
		}
    },
    error: function(xhr, textStatus, error) {
		console.log(xhr.statusText);
		console.log(textStatus);
		console.log(error);
    }
	});
});
$('#send-material-list').submit(function(e) {
	e.preventDefault();
	$('#material-list-email').val(supplierEmail);
	$('#material-list-modal').modal('show');
});

$('#quote-form').submit(function(e) {
	sendQuote();
});

function sendQuote() {
	$.ajax({
		type: 'POST',
		url: "/sendQuote/?proj_id=" + proj_id,
		contentType: "application/json;charset=UTF-8",
		dataType: "json",
		error: function(xhr, textStatus, error) {
			console.log(xhr.statusText);
			console.log(textStatus);
			console.log(error);
			showMessage("Error sending quote");
		}
	});

	showMessage("Quote sent");
}

function sendMaterialList() {
	$('#material-list-modal').modal('hide');

	$.ajax({
		type: 'POST',
		url: "/sendMaterialList/?proj_id=" + proj_id,
		data: JSON.stringify({email: $("#material-list-email").val()}),
		contentType: "application/json;charset=UTF-8",
		dataType: "json",
		error: function(xhr, textStatus, error) {
			console.log(xhr.statusText);
			console.log(textStatus);
			console.log(error);
			showMessage("Error sending material list");
		}
	});

	showMessage("Material list sent");
}

$('#view-material-list').submit(function(e) {
	e.preventDefault();

	$.ajax({
    type: 'POST',
    url: "/viewMaterialList/?proj_id=" + proj_id,
	contentType: "application/json;charset=UTF-8",
	dataType: "json",
    success: function(result) {
		if (result["reload"]) {
			reloadPage();
		}
		else {
			addPdf(result['url']);
			window.open(result['url']);
		}
    },
    error: function(xhr, textStatus, error) {
		console.log(xhr.statusText);
		console.log(textStatus);
		console.log(error);
    }
	});
});

function deleteAttachments() {
	$.ajax({
    type: 'POST',
	url: "/deleteAttachments/",
	data: JSON.stringify({attachments: pdfs}),
	contentType: "application/json;charset=UTF-8",
	dataType: "json",
    error: function(xhr, textStatus, error) {
		console.log(xhr.statusText);
		console.log(textStatus);
		console.log(error);
    }
	});
}

function toggleFinalized() {
	if (finalized) {
		finalized = !finalized;
		updateFinalized();
	}

	else {
		window.location.replace("/createquote?proj_id=" + proj_id);
	}
}

function updateFinalized(loading) {
	if (finalized) {
		$("#finalize").removeClass("finalize-off");
		$("#finalize-check").removeClass("finalize-check-off");
		$("#finalize-text").html("Finalized");
		$("#edit").css("display", "none");
	}

	else {
		$("#finalize").addClass("finalize-off");
		$("#finalize-check").addClass("finalize-check-off");
		$("#finalize-text").html("Finalize");
		$("#edit").css("display", "block");
	}

	if (!loading) {
		$.ajax({
		type: 'POST',
		url: "/finalizeQuote/?proj_id=" + proj_id,
		data: JSON.stringify({finalize: finalized}),
		contentType: "application/json;charset=UTF-8",
		dataType: "json",
		error: function(xhr, textStatus, error) {
			console.log(xhr.statusText);
			console.log(textStatus);
			console.log(error);
		}
		});
	}
}

function noProject(){
	$('#message').on('hidden.bs.modal', function() {
		window.location.href = '/projects/';
	});
  showMessage("Project does not exist.");
}

window.onbeforeunload = function() {
	if (pdfs.length > 0) {
		deleteAttachments();
	}

	return;
}