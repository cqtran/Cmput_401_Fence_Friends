function focusSearch() {
	document.getElementById("search-typeahead").focus();
}

function expandSearch() {
	document.getElementById("search-bar").classList.remove("collapsed-search");
	document.getElementById("search-bar").classList.add("expanded-search");
}

function collapseSearch() {
	document.getElementById("search-bar").classList.remove("expanded-search");
	document.getElementById("search-bar").classList.add("collapsed-search");
}