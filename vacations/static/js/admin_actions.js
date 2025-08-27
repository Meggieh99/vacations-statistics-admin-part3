console.log('admin_actions.js loaded!');

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

function showDeleteMessage() {
  const msgBox = document.getElementById('delete-message');
  console.log('showDeleteMessage() called');

  if (!msgBox) {
    console.warn('Element with id "delete-message" not found!');
    return;
  }

  msgBox.style.display = 'block';
  msgBox.style.opacity = '1';
  msgBox.style.transition = 'opacity 0.5s ease';

  setTimeout(() => {
    msgBox.style.opacity = '0';
    setTimeout(() => {
      msgBox.style.display = 'none';
    }, 500);
  }, 2000);
}

document.addEventListener('DOMContentLoaded', function () {
  const deleteButtons = document.querySelectorAll('.delete-btn');
  console.log('Found', deleteButtons.length, 'delete buttons');

  deleteButtons.forEach(button => {
    button.addEventListener('click', async function () {
      const vacationId = this.dataset.vacationId;
      console.log('Attempting to delete vacation ID:', vacationId);

      const confirmDelete = confirm('Are you sure you want to delete this vacation?');
      if (!confirmDelete) return;

      try {
        const response = await fetch(`/api/vacations/${vacationId}/delete/`, {
          method: 'DELETE',
          headers: {
            'X-CSRFToken': getCookie('csrftoken'),
          },
          credentials: 'include',
        });

        const contentType = response.headers.get('content-type');

        if (contentType && contentType.includes('application/json')) {
          responseData = await response.json();
          console.log('Response JSON:', responseData);
        }

        if (response.ok) {
          console.log('Vacation deleted successfully.');
        } else {
          console.warn('Server returned error status:', response.status);
        }

        const card = this.closest('.vacation-card');
        if (card) {
          card.style.transition = 'opacity 0.3s ease';
          card.style.opacity = 0;

          setTimeout(() => {
            card.remove();
            showDeleteMessage();
          }, 300);
        }

      } catch (err) {
        console.error('Deletion failed:', err);
        alert('Error: ' + err.message);
      }
    });
  });
});
