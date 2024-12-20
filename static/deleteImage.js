import { showOverlay, hideOverlay } from './overlay.js';

// DELETE BUTTON HANDLING
export function deleteImage(event, button){
  event.preventDefault();

  // BRING UP OVERLAY TO PREVENT USER INTERACTION
  showOverlay("overlay-delete");

  let url = button.getAttribute('url')

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
}
