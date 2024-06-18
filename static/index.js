  //OVERLAY MANAGEMENT ON UPLOAD AND DELETE
function showOverlay(element_id) {
    document.getElementById(element_id).style.display = 'block';
  }
function hideOverlay(element_id) {
    document.getElementById(element_id).style.display = 'hide';
  }

//IMAGE SUBMISSION
var form = document.querySelector('form[method="POST"][action="/upload"]');

var fileInput = form.querySelector('input[type="file"]');

form.addEventListener('change', function(event) {
  var max_file_size = 1048576*4
  event.preventDefault();

  var file = fileInput.files[0];
  if (file.size > max_file_size){
    alert('File too big. Please upload a file <5MB')
  }
  else{
    showOverlay("overlay-upload");
    var formData = new FormData();
    formData.append('file', file);

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
      hideOverlay("overlay-upload")
    });
  }
});

document.querySelectorAll('.delete-btn').forEach(function(button) {
  button.addEventListener('click', 
  function(event){
    event.preventDefault();
    showOverlay("overlay-delete");

    let image_id = this.getAttribute('image_id')
    let url = this.getAttribute('url')

    fetch(url, {
      method: 'POST', 
      headers: {
       'Content-Type': 'application/json'
    }
    })
    .then((response) =>{ 
      if(response.redirected){
              window.location.href = response.url;
          }
      }
    )
    .catch((error) => {
      console.error('Error:', error);
      hideOverlay("overlay-delete")
    });
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