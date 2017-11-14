// Instantiate the Bloodhound suggestion engine
var customers = new Bloodhound({
    datumTokenizer: function (datum) {
        return Bloodhound.tokenizers.whitespace(datum.value);
    },
    queryTokenizer: Bloodhound.tokenizers.whitespace,
    remote: {
        wildcard: '%QUERY',
        url: '/getCustomerList?search=%QUERY',

        filter: function (customers) {
            console.log(customers);
            // Map the remote source JSON array to a JavaScript object array
            return $.map(customers, function (customer) {
                return {
                    value: customer.first_name,
                    cust_id: customer.customer_id,
                    phone: customer.cellphone,
                };
            });
        }
    },
    limit: 10
});

// Initialize the Bloodhound suggestion engine
customers.initialize();

$('#search-bar .typeahead').typeahead(null, {
    displayKey: 'value',
    source: customers.ttAdapter(),
    templates: {
        suggestion: Handlebars.compile("<p style='padding:6px'><b>{{value}}</b> - Phone {{phone}} </p>"),
        footer: Handlebars.compile("<b>Searched for '{{query}}'</b>")
    }
  }).on('typeahead:selected', function(event, selection) {
  
  // the second argument has the info you want
  window.location.href= '/customerinfo?cust_id=' + selection.cust_id + '&status=All'

});

//unknown if needed for duplicates
/*function getDupChecker(dupChecker) {
  if (!_.isFunction(dupChecker)) {
    dupChecker = dupChecker === false ? ignoreDups : standardDupChecker;
  }

  return dupChecker;

  function ignoreDups() { return false; }
  function standardDupChecker(a, b) { return a.value === b.value; }
}*/