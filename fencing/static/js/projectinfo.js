var attachmentPathLength = 20;
var pdf = null;

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

function setProgressTitle(title) {
	var progressTitle = document.getElementById("progressTitle");
	progressTitle.innerHTML = title;
}

function showSendingQuote() {
	setProgressTitle("Sending quote");
	var quoteButton = document.getElementById("sendQuoteButton");
	var materialListButton = document.getElementById("sendMaterialListButton");
	quoteButton.disabled = true;
	materialListButton.disabled = true;
	quoteButton.value = "Sending Quote...";
}

function showSendingMaterialList() {
	setProgressTitle("Sending material list");
	var quoteButton = document.getElementById("sendQuoteButton");
	var materialListButton = document.getElementById("sendMaterialListButton");
	quoteButton.disabled = true;
	materialListButton.disabled = true;
	materialListButton.value = "Sending Material List...";
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

		newName = escapeHtml(newName);

		tab.layoutName = newName;

		if (noClose) {
			tabText.innerHTML = newName;
		}

		else {
			tabText.innerHTML = '<button class="close closeTab" onclick="removeLayout(\'' + number + '\')" type="button">×</button>' + newName;
		}

		bodyText.innerHTML = newName + '&nbsp;<i class="fa fa-pencil" aria-hidden="true"></i>';

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

		newName = escapeHtml(newName);

		tab.appearanceName = newName;

		if (noClose) {
			tabText.innerHTML = newName;
		}

		else {
			tabText.innerHTML = '<button class="close closeTab" onclick="removeAppearance(\'' + number + '\')" type="button">×</button>' + newName;
		}

		bodyText.innerHTML = newName + '&nbsp;<i class="fa fa-pencil" aria-hidden="true"></i>';

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
		"setLayoutName('" + lastLayout + "')");
	clone.children[0].innerHTML = '<b>Untitled</b>&nbsp;<i class="fa fa-pencil" aria-hidden="true"></i>';
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
		"setAppearanceName('" + lastAppearance + "')");
	clone.children[0].innerHTML = '<b>Untitled</b>&nbsp;<i class="fa fa-pencil" aria-hidden="true"></i>';

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
	window.location.replace("/projectinfo/?proj_id=" + proj_id);
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

	$('#delete-others').click(function() {
		deleteOtherLayouts(number);
	});

	$('#menu').modal('show');
}

function appearanceMenu(event, number) {
	event.preventDefault();

	$('#delete-others').click(function() {
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

function loadAppearance(appearance, number) {
	var form = $("#appearance" + number + " > div");
	form.find("#basePrice").val(appearance.base_price);
	form.find("#height").val(appearance.height);
	form.find("#style").val(appearance.style);
	form.find("#borderColor").val(appearance.border_colour);
	form.find("#panelColor").val(appearance.panel_colour);
	setAppearanceName(number, true, appearance.appearance_name);
	document.getElementById("appearance-tab" + number).dbId =
		appearance.appearance_id;
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
	  document.getElementById("status").setAttribute('class', 'float-right paid-text');
	}
	else if(project[0].status_name == "Not Reached"){
	  document.getElementById("status").setAttribute('class', 'float-right not-reached-text');
	}
	else if(project[0].status_name == "Appraisal Booked"){
	  document.getElementById("status").setAttribute('class', 'float-right appraisal-booked-text');
	}
	else if(project[0].status_name == "Waiting for Appraisal"){
	  document.getElementById("status").setAttribute('class', 'float-right waiting-appraisal-text');
	}
	else if(project[0].status_name == "Appraised"){
	  document.getElementById("status").setAttribute('class', 'float-right appraised-text');
	}
	else if(project[0].status_name == "Quote Sent"){
	  document.getElementById("status").setAttribute('class', 'float-right quote-sent-text');
	}
	else if(project[0].status_name == "Waiting for Alberta1Call"){
	  document.getElementById("status").setAttribute('class', 'float-right waiting-alberta-text');
	}
	else if(project[0].status_name == "Installation Pending"){
	  document.getElementById("status").setAttribute('class', 'float-right install-pending-text');
	}
	else if(project[0].status_name == "Installing"){
	  document.getElementById("status").setAttribute('class', 'float-right installing-text');
	}
	else if(project[0].status_name == "No Longer Interested"){
	  document.getElementById("status").setAttribute('class', 'float-right not-interested-text');
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

	final.addEventListener('click', function(){
		$("#file-upload").click();
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
        setProjectInfo(result);
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

//get details
function moreDetails(){
  $.ajax({
      type: 'GET',
      url: '/projectdetails/' + proj_id,
      success: function(result) {
    	  imgPath = result[0].replace(/^'(.*)'$/, '$1');
        tbnPath = result[1].replace(/^'(.*)'$/, '$1');
			  var layouts = result[2];
			  var appearances = result[3];
			  $('#companyNameNav').html(result[4]);
			  var selectedLayout = result[5];
			  var selectedAppearance = result[6];
			  var displayStrings = result[7];
			  var customerName = $('#customer-name');
			  customerName.text(result[8]);
			  var oldHref = customerName.attr('href');
			  customerName.attr('href', oldHref + result[9] + '&status=All');
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

//this runs after the html has loaded, all function calls should be in here
$(document).ready(function(){
  pictureList = document.getElementById('projectPictures');
  proj_id = getParameterByName('proj_id');

  if(proj_id == null) {
	$('#message').on('hidden.bs.modal', function() {
		window.location.href = '/projects/';
	});

    showMessage("Project does not exist.");
  }

  $("#pencil-button").removeClass('hide');
  $('#edit').click(function(){
    window.location.href= '/editprojectinfo?proj_id=' + proj_id;
  });

  moreDetails();
  getProjects();

  $('#input').on('shown.bs.modal', function() {
	var inputText = $('#inputText');
	inputText.focus();
	inputText.select();
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
			pdf = result['url'];
			$('pdfFallback').attr('href', pdf);
			$('#pdfContent').attr('src', pdf);
			$('#pdf').modal("show");
		}
    },
    error: function(xhr, textStatus, error) {
		console.log(xhr.statusText);
		console.log(textStatus);
		console.log(error);
    }
	});
});
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
			pdf = result['url'];
			$('pdfFallback').attr('href', pdf);
			$('#pdfContent').attr('src', pdf);
			$('#pdf').modal("show");
		}
    },
    error: function(xhr, textStatus, error) {
		console.log(xhr.statusText);
		console.log(textStatus);
		console.log(error);
    }
	});
});

function deleteAttachment() {
	$.ajax({
    type: 'POST',
    url: "/deleteAttachment/?attachment=" + pdf.slice(attachmentPathLength),
	contentType: "application/json;charset=UTF-8",
	dataType: "json",
    error: function(xhr, textStatus, error) {
		console.log(xhr.statusText);
		console.log(textStatus);
		console.log(error);
    }
	});
}

$('#pdf').on("hidden.bs.modal", function() {
	deleteAttachment();
	pdf = null;
});

window.onbeforeunload = function() {
	if (pdf != null) {
		deleteAttachment();
	}

	return;
}