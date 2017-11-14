// Instantiate the Bloodhound suggestion engine
var movies = new Bloodhound({
  datumTokenizer: function(datum) {
    return Bloodhound.tokenizers.whitespace(datum.value);
  },
  queryTokenizer: Bloodhound.tokenizers.whitespace,
  remote: {
    wildcard: '%QUERY',
    url: 'http://api.themoviedb.org/3/search/movie?query=%QUERY&api_key=f22e6ce68f5e5002e71c20bcba477e7d',
    transform: function(response) {
      // Map the remote source JSON array to a JavaScript object array
      return $.map(response.results, function(movie) {
        return {
          value: movie.original_title
        };
      });
    }
  }
});

// Instantiate the Typeahead UI
$('#custom-templates .typeahead').typeahead(null, {
  name: 'best-pictures',
  display: 'value',
  source: bestPictures,
  templates: {
    empty: [
      '<div class="empty-message">',
        'unable to find any Best Picture winners that match the current query',
      '</div>'
    ].join('\n'),
    suggestion: Handlebars.compile('<div><strong>{{value}}</strong> – {{year}}</div>')
  }
});