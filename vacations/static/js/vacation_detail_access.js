document.addEventListener("DOMContentLoaded", function () {
  const detailButtons = document.querySelectorAll(".details-btn");
  const userId = document.body.dataset.userId;

  detailButtons.forEach(button => {
    button.addEventListener("click", function (e) {
      e.preventDefault();  //to prevent form submission
      const vacationId = this.dataset.vacationId;

      if (!userId) {
        alert("You must be logged in to view vacation details.");
        window.location.href = "/login/form/";
        return;
      }

      window.location.href = `/vacations/${vacationId}/details/`;
    });
  });
});
