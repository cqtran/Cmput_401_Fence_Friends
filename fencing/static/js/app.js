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
    limit: 5
});

// Instantiate the Bloodhound suggestion engine
var projects = new Bloodhound({
    datumTokenizer: function (datum) {
        return Bloodhound.tokenizers.whitespace(datum.value);
    },
    queryTokenizer: Bloodhound.tokenizers.whitespace,
    remote: {
        wildcard: '%QUERY',
        url: '/getProjectList?search=%QUERY',

        filter: function (projects) {
            console.log(projects);
            // Map the remote source JSON array to a JavaScript object array
            return $.map(projects, function (project) {
                return {
                    value: project.project_name,
                    proj_id: project.project_id,
                    address: project.cellphone,
                    status: project.status_name,
                };
            });
        }
    },
    limit: 5
});

// Initialize the Bloodhound suggestion engine
customers.initialize();
projects.initialize();

$('#search-bar .typeahead').typeahead({
    highlight: true
  },
  {
    name: 'customers',
    displayKey: 'value',
    source: customers.ttAdapter(),
    templates: {
        header: Handlebars.compile("<div class='container-fluid'><h3 class='text-green'>Customer</h3><hr class='mt-2'></div>"),
        suggestion: Handlebars.compile("<div class='container-fluid'><p><b>{{value}}</b> - Phone {{phone}} </p></div>")
    }
  },
  {
    name: 'projects',
    displayKey: 'value',
    source: projects.ttAdapter(),
    templates: {
        header: Handlebars.compile("<div class='container-fluid'><h3 class='text-green'>Projects</h3><hr class='mt-2'></div>"),
        suggestion: Handlebars.compile("<div class='container-fluid'><p><b>{{value}}</b> - Status - {{status}} - Address {{address}} </p></div>")
    }
  }).on('typeahead:selected', function(event, selection) {
  
  if(selection.hasOwnProperty('proj_id')){
    window.location.href= '/projectinfo?proj_id=' + selection.proj_id
  }
  else if(selection.hasOwnProperty('cust_id')){
    window.location.href= '/customerinfo?cust_id=' + selection.cust_id + '&status=All'
  }
});