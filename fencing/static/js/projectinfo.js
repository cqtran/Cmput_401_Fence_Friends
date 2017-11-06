function showSendingQuote() {
	var quoteButton = document.getElementById("sendQuoteButton");
	var materialListButton = document.getElementById("sendMaterialListButton");
	quoteButton.disabled = true;
	materialListButton.disabled = true;
	quoteButton.value = "Sending Quote...";
}

function showSendingMaterialList() {
	var quoteButton = document.getElementById("sendQuoteButton");
	var materialListButton = document.getElementById("sendMaterialListButton");
	quoteButton.disabled = true;
	materialListButton.disabled = true;
	materialListButton.value = "Sending Material List...";
}