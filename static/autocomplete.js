// AUTOCOMPLETE WITH JQUERY AND FILTERING OF AUTOCOMPLETE SUGGESTIONS
export function getAutoComplete() {
  $("#search").autocomplete({
    source: function(request, response) {
      var matcher = new RegExp("^" + $.ui.autocomplete.escapeRegex(request.term), "i");
      fetch("/autocomplete", {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        },
      })
      .then(response => response.json())
      .then(data => {
        response(data.filter(item => matcher.test(item)));
      })
      .catch(error => console.error('Error:', error));
    }
  });
}
