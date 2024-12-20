import { showOverlay, hideOverlay } from "./overlay.js";
import { upload } from "./upload.js";
import { deleteImage } from "./deleteImage.js";
import { getAutoComplete } from "./autocomplete.js";

//IMAGE SUBMISSION
var form = document.querySelector('form[method="POST"][action="/upload"]');

var fileInput = form.querySelector('input[type="file"]');

form.addEventListener('change', (event) => upload(1048576*4, fileInput, event));

//IMAGE DELETION
document.querySelectorAll('.delete-btn').forEach(function(button) {
  button.addEventListener('click', (event) => {deleteImage(event, button)});
});

//AUTOCOMPLETE WITH JQUERY AND FILTERING OF AUTOCOMPLETE 
$(document).ready(getAutoComplete());