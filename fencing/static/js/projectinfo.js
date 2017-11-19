var activeLayout = "1";
var activeAppearance = "1";

var lastLayout = "1";
var lastAppearance = "1";

var deletedLayout = null;
var deletedAppearance = null;

var layoutCount = 1;
var appearanceCount = 1;
var tabLimit = 10;

var drawiopic;
var imgpath;
var tbnpath;
var pictureList;
var proj_id;

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
}

function setActiveAppearance(number) {
	if (number == deletedAppearance) {
		deletedAppearance = null;
		return;
	}

	activeAppearance = number;
}

function setLayoutName(number, newName, loading) {
	var tab = document.getElementById("layout-tab" + number);
	var tabText = tab.children[0];
	var bodyText = document.getElementById("layout" + number).children[0];
	
	if (newName == null) {
		newName = prompt("Layout Name", bodyText.children[0].innerHTML);
	}

	if (newName != null) {

		tab.layoutName = newName;

		if (number == "1") {
			tabText.innerHTML = newName;
		}

		else {
			tabText.innerHTML = '<button class="close closeTab" onclick="removeLayout(\'' + number + '\')" type="button">×</button>' +
				newName;
		}

		bodyText.innerHTML = "<b>" + newName + '</b>&nbsp;<i class="fa fa-pencil" aria-hidden="true"></i>';

		if (!loading) {
			saveActiveLayout();
		}
	}
}

function setAppearanceName(number, newName, loading) {
	var tab = document.getElementById("appearance-tab" + number);
	var tabText = tab.children[0];
	var bodyText = document.getElementById("appearance" + number).children[0];

	if (newName == null) {
		newName = prompt("Appearance Name", bodyText.innerHTML.slice(3, -4));
	}

	if (newName != null) {

		tab.appearanceName = newName;

		if (number == "1") {
			tabText.innerHTML = newName;
		}

		else {
			tabText.innerHTML = '<button class="close closeTab" onclick="removeAppearance(\'' + number + '\')" type="button">×</button>' +
				newName;
		}

		bodyText.innerHTML = "<b>" + newName + '</b>&nbsp;<i class="fa fa-pencil" aria-hidden="true"></i>';

		if (!loading) {
			saveActiveAppearance();
		}
	}
}

function setActiveLayoutId(dbId) {
	document.getElementById("layout-tab" + activeLayout).dbId =
		dbId.toString();
}

function setActiveAppearanceId(dbId) {
	document.getElementById("appearance-tab" + activeAppearance).dbId =
		dbId.toString();
}

function addLayout(loading) {
	if (layoutCount >= tabLimit) {
		alert("Cannot have more than " + tabLimit.toString() + " layouts");
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
	clone.children[0].innerHTML = "<b>Layout " + lastLayout + '</b>&nbsp;<i class="fa fa-pencil" aria-hidden="true"></i>';
	clone.children[1].children[0].id = "image" + lastLayout;
	document.getElementById("layouts").appendChild(clone);

	var cloneTab = activeTab.cloneNode(true);
	cloneTab.id = "layout-tab" + lastLayout;
	cloneTab.setAttribute("onclick", "setActiveLayout('" + lastLayout + "')");
	var link = cloneTab.children[0];
	link.href = "#layout" + lastLayout;
	link.innerHTML = '<button class="close closeTab" onclick="removeLayout(\'' + lastLayout + '\')" type="button">×</button>Layout ' + lastLayout;
	document.getElementById("layout-tabs").insertBefore(cloneTab,
		document.getElementById("add-layout"));
	cloneTab.layoutName = "Layout " + lastLayout;

	activeLink.classList.remove("active");
	active.classList.remove("active");
	active.classList.remove("show");

	layoutCount += 1;

	if (!loading) {
		saveActiveLayout();
	}
}

function addAppearance(loading) {
	if (appearanceCount >= tabLimit) {
		alert("Cannot have more than " + tabLimit.toString() + " appearances");
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
	clone.children[0].innerHTML = "<b>Appearance " + lastAppearance + '</b>&nbsp;<i class="fa fa-pencil" aria-hidden="true"></i>';
	clone.children[1].innerHTML = "Appearance" + lastAppearance;
	document.getElementById("appearances").appendChild(clone);

	var cloneTab = activeTab.cloneNode(true);
	cloneTab.id = "appearance-tab" + lastAppearance;
	cloneTab.setAttribute("onclick", "setActiveAppearance('" + lastAppearance + "')");
	var link = cloneTab.children[0];
	link.href = "#appearance" + lastAppearance;
	link.innerHTML = '<button class="close closeTab" onclick="removeAppearance(\'' + lastAppearance + '\')" type="button">×</button>Appearance ' + lastAppearance;
	document.getElementById("appearance-tabs").insertBefore(cloneTab,
		document.getElementById("add-appearance"));
	cloneTab.appearanceName = "Appearance " + lastAppearance;

	activeLink.classList.remove("active");
	active.classList.remove("active");
	active.classList.remove("show");

	appearanceCount += 1;

	if (!loading) {
		saveActiveAppearance();
	}
}

function removeLayout(number) {
	removeLayoutFromDb(number);

	var element = document.getElementById("layout" + number);
	element.parentNode.removeChild(element);
	element = document.getElementById("layout-tab" + number);
	element.parentNode.removeChild(element);

	if (activeLayout == number) {
		activeLayout = "1";
		document.getElementById("layout1").classList.add("active");
		document.getElementById("layout1").classList.add("show");
		document.getElementById("layout-tab1").children[0].classList.add("active");
	}

	deletedLayout = number;
	layoutCount -= 1;
}

function removeAppearance(number) {
	removeAppearanceFromDb(number);

	var element = document.getElementById("appearance" + number);
	element.parentNode.removeChild(element);
	element = document.getElementById("appearance-tab" + number);
	element.parentNode.removeChild(element);

	if (activeAppearance == number) {
		activeAppearance = "1";
		document.getElementById("appearance1").classList.add("active");
		document.getElementById("appearance1").classList.add("show");
		document.getElementById("appearance-tab1").children[0].classList.add("active");
	}

	deletedAppearance = number;
	appearanceCount -= 1;
}

function reloadPage() {
	var url = new URL(window.location.href);
	var proj_id = url.searchParams.get("proj_id");
	window.location.replace("/projectinfo/?proj_id=" + proj_id);
}

function saveActiveLayout() {
	var img = document.getElementById("image" + activeLayout).getAttribute('src');
	var url = new URL(window.location.href);
	var proj_id = url.searchParams.get("proj_id");
	var tab = document.getElementById("layout-tab" + activeLayout);
	var layout_id = tab.dbId;
	var layout_name = tab.layoutName;
	var quoteData =
		JSON.stringify({image: img, layoutId: layout_id, name: layout_name});

	$.ajax({
      type: 'POST',
      url: "/saveDiagram/?proj_id=" + proj_id,
      data: quoteData,
	  contentType: "application/json;charset=UTF-8",
	  dataType: "json",
      success: function(result) {
		returndata = result;
		if (result["reload"]) {
			reloadPage();
		}
		else {
			setActiveLayoutId(result["quoteId"]);
		}
      },
      error: function(xhr, textStatus, error) {
		alert("Error");
		console.log(xhr.statusText);
		console.log(textStatus);
		console.log(error);
      }
  });

}

// TODO: fill
function saveActiveAppearance() {
	;
}

function removeLayoutFromDb(number) {
	var tab = document.getElementById("layout-tab" + number);
	var layout_id = tab.dbId;
	var quoteData = JSON.stringify({layoutId: layout_id});
	$.ajax({
		type: 'POST',
		url: "/removeLayout/?proj_id=" + proj_id,
		data: quoteData,
		contentType: "application/json;charset=UTF-8",
		dataType: "json",
		error: function(xhr, textStatus, error) {
			alert("Error");
			console.log(xhr.statusText);
			console.log(textStatus);
			console.log(error);
		}
	});
}

// TODO: fill
function removeAppearanceFromDb(number) {
	;
}

function loadLayout(layout, number) {
	document.getElementById("image" + number).src = layout.layout_info;
	setLayoutName(number, layout.layout_name, true);
	document.getElementById("layout-tab" + number).dbId = layout.layout_id;
}

function loadLayouts(layouts){
	loadLayout(layouts[0], "1");
	var currentLayout = 2;

	for(var i = 1; i < layouts.length; i++) {
		addLayout(true);
		loadLayout(layouts[i], currentLayout.toString());
		currentLayout++;
	}
}

function setProjectInfo(project){
	document.getElementById('project-name').innerHTML = project[0].project_name;
	document.getElementById('status').innerHTML = "■ " + project[0].status_name;
	document.getElementById('address').innerHTML = project[0].address;
	document.getElementById('start-date').innerHTML = project[0].start_date;
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
	document.getElementById('editproject').setAttribute('onclick', 'projectClicked('+proj_id+')')

	if (project[0].end_date != null) {
		document.getElementById('end_date').innerHTML = project[0].end_date;
	}
	var note = project[0].note;
	if (!(note == null || note.trim() == "")) {
		document.getElementById('savednote').innerHTML = project[0].note;
		document.getElementById('noteContainer').style.display = "block";
	}
}

function makePictures(pictures){
	$('#projectPictures').empty();
  pictures.forEach(function(picture) {
    var img = document.createElement('img');
    var final = document.createElement('a');

		img.src =  tbnPath + picture.thumbnail_name;
		img.alt =  picture.thumbnail_name + ' not found';
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
  var img = document.createElement('img');
  img.src =  tbnPath + 'No_picture_available.png';
  img.alt =  'No pictures available';
  img.height = '150';
  img.width = '150';
  pictureList.appendChild(img);
}

function projectClicked(id) {
	window.location.href= '/editprojectinfo?proj_id='+id
}

function editDiagram(image) {
	var initial = image.getAttribute('src');
	image.setAttribute('src', 'https://csahmad.github.io/drawio/war/images/ajax-loader.gif');
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
	iframe.setAttribute('src', 'https://csahmad.github.io/drawio/war/?embed=1&ui=atlas&spin=1&modified=unsavedChanges&proto=json');
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
					alert('Error ' + req.status);
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
      error: function(result) {
          showError();
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
				layouts = result[2];
				$('#companyNameNav').html(result[3]);
				loadLayouts(layouts);
      },
      error: function(result) {
          showError();
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
      error: function(result) {
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

//this runs after the html has loaded, all function calls should be in here
$(document).ready(function(){
	$("#pencil-button").attr('class', 'nav-item');
	pictureList = document.getElementById('projectPictures');
  proj_id = getParameterByName('proj_id');

  if(proj_id == null) {
    alert("Project does not exist.");
    window.location.href = '/projects/';
  }

	moreDetails();
	getProjects();
	getPics();
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
$('form').submit(function(e) {
  e.preventDefault();
  uploadPicture(e);
});

$('#imagepopup').on('show.bs.modal', function (e) {
  alert('hello')
});
