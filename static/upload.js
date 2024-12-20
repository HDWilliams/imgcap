import { showOverlay, hideOverlay } from './overlay.js';

// IMAGE SUBMISSION
export function upload(max_file_size, fileInput, event) {
  event.preventDefault();

  //CHECK FILE SIZE
  var file = fileInput.files[0];
  if (file.size > max_file_size){
    alert('File too big. Please upload a file <5MB')
  }
  else{
    //SHOW OVERLAY TO PREVENT USER INTERACTION, START UPLOAD
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
}
