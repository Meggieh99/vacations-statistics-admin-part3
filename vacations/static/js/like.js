document.addEventListener('DOMContentLoaded', function () {
    const buttons = document.querySelectorAll('.like-btn');

    buttons.forEach(button => {
        button.addEventListener('click', async function () {
            const vacationId = this.dataset.vacationId;
            const liked = this.dataset.liked === 'true';
            const url = liked
                ? `/api/vacations/${vacationId}/unlike/`
                : `/api/vacations/${vacationId}/like/`;

            const csrftoken = getCookie('csrftoken');

            try {
                const response = await fetch(url, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrftoken
                    },
                    credentials: 'include'
                });

                if (response.ok) {
                    location.reload(); // Reload to update like count/state
                } else {
                    const errorData = await response.json();

                  const errorMessage = errorData.error?.toLowerCase() || "";
                  if (errorMessage.includes("not authenticated") || errorMessage.includes("credentials")) {
                     alert("Please log in to like vacations.");
                  } else {
                     alert(`Error: ${errorData.error || "Unknown error"}`);
                  }


                    // Redirect to login form page after alert
                    window.location.href = "/login/form/";
                }
            } catch (error) {
                console.error('Error during like action:', error);
                alert("An unexpected error occurred. Please try again later.");
            }
        });
    });
});

/**
 * Helper function to get a cookie value by name.
 * 
 * @param {string} name - Name of the cookie to retrieve
 * @returns {string|null} The cookie value or null if not found
 */
function getCookie(name) {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.startsWith(name + '=')) {
            return decodeURIComponent(cookie.substring(name.length + 1));
        }
    }
    return null;
}
