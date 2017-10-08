function fillCustomerInfo(name, email, phone, address) {

	document.getElementById("customerName").innerHTML = name;

	var innerHTML = [];

	if (email !== null) innerHTML.push(email);
	if (phone !== null) innerHTML.push(phone);
	if (address !== null) innerHTML.push(address);

	document.getElementById("customerInfo").innerHTML = innerHTML.join("<br>");
}

window.onload = function() {
	fillCustomerInfo("Jane Doe", "doe@email.com", "(555) 555-5555",
		"123 456 Avenue");
};