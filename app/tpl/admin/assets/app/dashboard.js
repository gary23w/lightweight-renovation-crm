$(document).ready(function () {
  initializeToasts();
  applyShakeAnimation();
  handleFloatingActionButtonClick();
  handleAddCustomerButtonClick();
  hideElementsIfNoNotifications();
});

function initializeToasts() {
  $(".toast").toast({ delay: 2000 }); // Auto-hide after 2 seconds
  $(".toast").toast("show");
}

function applyShakeAnimation() {
  setInterval(function () {
    $("#fab").addClass("shake");
    setTimeout(function () {
      $("#fab").removeClass("shake");
    }, 1000);
  }, 2000);
}

function handleFloatingActionButtonClick() {
  $("#fab").click(function () {
    var btnLinksTop = $("#notificationsModal").offset().top;
    $("html, body").animate({ scrollTop: btnLinksTop }, "fast");
    $(".click-note").click();
  });
}

function handleAddCustomerButtonClick() {
  $(".add-customer-btn").click(function () {
    if ($(window).width() < 768) {
      $(".navbar-collapse").removeClass("show");
    }
  });
}

function hideElementsIfNoNotifications() {
  if ($("#get-count").text() === "0") {
    $("#clear-note").hide();
    $("#fab").hide();
  }
}
