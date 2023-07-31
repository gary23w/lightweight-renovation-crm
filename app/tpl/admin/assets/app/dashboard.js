$(document).ready(function () {
  $(".toast").toast({ delay: 2000 }); // auto hide after 2 seconds
  $(".toast").toast("show");
  setInterval(function () {
    $("#fab").addClass("shake");
    setTimeout(function () {
      $("#fab").removeClass("shake");
    }, 1000);
  }, 2000);

  $("#fab").click(function () {
    var btnLinksTop = $("#notificationsModal").offset().top;
    $("html, body").animate({ scrollTop: btnLinksTop }, "fast");
    $(".click-note").click();
  });
  if ($("#get-count").text() == 0) {
    $("#clear-note").hide();
    $("#fab").hide();
  }
});
