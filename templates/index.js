//OVERLAY MANAGEMENT ON UPLOAD
function showOverlay() {
    document.getElementById('overlay').style.display = 'block';
  }
function hideOverlay() {
    document.getElementById('overlay').style.display = 'hide';
  }

//IMAGE SUBMISSION
var form = document.querySelector('form[method="POST"][action="/upload"]');

var fileInput = form.querySelector('input[type="file"]');

form.addEventListener('change', function(event) {
  // Prevent the default form submission
  showOverlay();
  event.preventDefault();

  // Log the selected file to the console
  var file = fileInput.files[0];
  // Create a new FormData object
  var formData = new FormData();
  formData.append('file', file);

  // Use the fetch API to submit the form data
  fetch('/upload', {
    method: 'POST',
    body: formData,
    redirect: 'follow'
  })
  .then((response)=>{         
        if(response.redirected){
            window.location.href = response.url;
        }
      })   
  .catch(error => {
    console.error(error)
    alert('Image upload failed, please try again...')
    hideOverlay()
  });
});

//AUTOCOMPLETE WITH JQUERY AND FILTERING OF AUTOCOMPLETE SUGGESTIONS
  $(document).ready(function() {
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
});

