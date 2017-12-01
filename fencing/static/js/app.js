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
                    address: project.address,
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
        header: Handlebars.compile("<div class='container-fluid'><h3 class='text-grey'>Customer</h3><hr class='mt-2'></div>"),
        suggestion: Handlebars.compile("\
        {{#if phone}}\
            <div class='container-fluid'><p>{{value}}<span class='no-highlight'> - Phone {{phone}} </span></p></div>\
        {{else}}\
            <div class='container-fluid'><p>{{value}} </p></div>\
        {{/if}}")
    }
  },
  {
    name: 'projects',
    displayKey: 'value',
    source: projects.ttAdapter(),
    templates: {
        header: Handlebars.compile("<div class='container-fluid'><h3 class='text-grey'>Projects</h3><hr class='mt-2'></div>"),
        suggestion: Handlebars.compile("\
        {{#if address}}\
            <div class='container-fluid'><p class='top-bot-pad'>{{value}}<span class='no-highlight'> - Status - {{status}} - Address {{address}} </span></p></div>\
        {{else}}\
            <div class='container-fluid'><p class='top-bot-pad'>{{value}}<span class='no-highlight'> - Status - {{status}} </span></p></div>\
        {{/if}}")
    }
  }).on('typeahead:selected', function(event, selection) {
  
  if(selection.hasOwnProperty('proj_id')){
    window.location.href= '/projectinfo?proj_id=' + selection.proj_id
  }
  else if(selection.hasOwnProperty('cust_id')){
    window.location.href= '/customerinfo?cust_id=' + selection.cust_id + '&status=All'
  }
});

function getParameterByName(name, url) {
    if (!url) url = window.location.href;
    name = name.replace(/[\[\]]/g, "\\$&");
    var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, " "));
}

function getStatus(){
//get details
  $.ajax({
      type: 'GET',
      url: '/getStatusList/',
      success: function(result) {
        dealStatuses(result);
      }
  });
}

function dealStatuses(statuses){
  statuses.forEach(function(status) {
    $('select[name=status]').append('<option value="' + status.status_name + '">' + status.status_name + '</option>');
  });
  $('.selectpicker').selectpicker('refresh'); 
}

function focusSearch() {
  if($(window).width() < 768){
    $('#companyNameNav').addClass('small-hide');
    $('#companyLink').removeAttr('href');
    $('#search-div').addClass('col-9');
    $('#search-icon-span').removeClass('search-icon').addClass('search-icon-green');
    $('#search-bar').removeClass('remove');
  }

  document.getElementById("search-typeahead").focus();
}

function collapseSearch() {
  $('#search-div').removeClass('col-9');
  $('#search-bar').addClass('remove');
  $('#search-icon-span').removeClass('search-icon-green').addClass('search-icon');
  $('#companyNameNav').removeClass('small-hide');
  $('#companyLink').attr('href', '/');
}