document.addEventListener('DOMContentLoaded', async function () {
  const form = document.getElementById('edit-vacation-form');

  // Extract vacation ID from URL
  const pathParts = window.location.pathname.split('/').filter(Boolean);
  const vacationId = pathParts[pathParts.length - 2];

  const preview = document.getElementById("preview-image");
  const fileInput = document.getElementById("image-upload");
  const clickableArea = document.getElementById("image-click-area");

  // Open file selector when clicking image area
  if (clickableArea && fileInput) {
    clickableArea.addEventListener("click", () => {
      fileInput.click();
    });
  }

  // Preview selected image
  if (fileInput && preview) {
    fileInput.addEventListener("change", () => {
      const file = fileInput.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
          preview.src = e.target.result;
        };
        reader.readAsDataURL(file);
      }
    });
  }

  // CSRF helper
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let cookie of cookies) {
        cookie = cookie.trim();
        if (cookie.startsWith(name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
});
