$(function () {
  $(".job-box").sortable({
    containment: "parent",
    cursor: "move",
    opacity: 0.65,
  });
  $("#downloadCurrentJobs").click(function () {
    window.location.href = "/admin/download_jobs";
  });
  var sortDescending = true;
  var cards = null; // Store detached cards here
  if ($(".job-box").children().length == 0) {
    $("#sortJobsButton").hide();
  }

  $("#sortJobsButton").click(function () {
    sortJobs();
    sortDescending = !sortDescending;
  });

  function sortJobs() {
    var container = $(".job-box");

    if (!cards) {
      // If cards are not already detached
      cards = container.find(".job-case").detach();
    }

    cards.sort(function (a, b) {
      var dateA = new Date(
        $(a).find(".base-data li[data-date-complex]").data("date-complex")
      );
      var dateB = new Date(
        $(b).find(".base-data li[data-date-complex]").data("date-complex")
      );

      // Reverse the sort if needed
      return sortDescending ? dateB - dateA : dateA - dateB;
    });
    // empty container
    container.empty();
    container.append(cards);
  }
});
