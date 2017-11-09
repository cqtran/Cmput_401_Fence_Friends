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