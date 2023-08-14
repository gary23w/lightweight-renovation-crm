$(document).ready(function () {
  $(".toast").toast({ delay: 2000 }); // auto hide after 2 seconds
  $(".toast").toast("show");
  var deleteId;
  var table = $("#customerTable").DataTable({
    pageLength: 5,
    responsive: true,
    columnDefs: [{ orderable: false, targets: 0 }],
    initComplete: function (settings, json) {
      $("#mainTable").show();
      // Move click event into initComplete
      $("#customerTable tbody").on("click", "tr", function () {
        var data = table.row(this).data();
        deleteId = data[0];
        var html = "";
        for (var i = 0; i < data.length; i++) {
          html +=
            "<p><b>" +
            $("#customerTable th").eq(i).text() +
            ": </b>" +
            data[i] +
            "</p>";
        }
        $("#customerModal .modal-body").html(html);
        $("#customerModal").modal("show");
      });
      $("#deleteButton").click(function () {
        $.ajax({
          url: "/admin/delete_mail_promo_user/" + deleteId,
          type: "POST",
          success: function (result) {
            //{message: 'deleted'}
            if (result.message == "deleted") {
              $("#customerTable tbody tr").each(function () {
                var rowId = $(this).find("td:first").text(); // Assuming the ID is in the first column (td)
                if (rowId == deleteId) {
                  $(this).remove();
                  $("#customerModal").modal("hide");
                  return false;
                }
              });
            }
          },
        });
      });
    },
  });
  let url = "/static/templates/promo.one.gary";
  let templateOne = {};
  $.ajax({
    url: url,
    method: "GET",
    success: function (data) {
      templateOne.name = "Promo One";
      templateOne.html = data;
    },
  });
  function templateOneAdd() {
    if ($("#emailBody").val() != "") {
      $("#emailBody").val("");
    }
    $("#emailBody").val(templateOne.html);
  }

  function alert_modal(
    alert_title,
    alert_body,
    alert_button,
    alert_cancel,
    alert_color
  ) {
    var alert_modal = document.createElement("div");
    alert_modal.setAttribute("class", "modal fade");
    alert_modal.setAttribute("id", "alert_modal");
    alert_modal.setAttribute("tabindex", "-1");
    alert_modal.setAttribute("role", "dialog");
    alert_modal.setAttribute("aria-labelledby", "alert_modal_label");
    alert_modal.setAttribute("aria-hidden", "true");
    var alert_modal_dialog = document.createElement("div");
    alert_modal_dialog.setAttribute("class", "modal-dialog");
    alert_modal_dialog.setAttribute("role", "document");
    var alert_modal_content = document.createElement("div");
    alert_modal_content.setAttribute("class", "modal-content");
    var alert_modal_header = document.createElement("div");
    alert_modal_header.setAttribute(
      "class",
      "modal-header bg-" + alert_color + " text-white"
    );
    var alert_modal_header_title = document.createElement("h5");
    alert_modal_header_title.setAttribute("class", "modal-title");
    alert_modal_header_title.setAttribute("id", "alert_modal_label");
    alert_modal_header_title.innerHTML = alert_title;
    var alert_modal_header_button = document.createElement("button");
    alert_modal_header_button.setAttribute("type", "button");
    alert_modal_header_button.setAttribute("class", "close");
    alert_modal_header_button.setAttribute("data-dismiss", "modal");
    alert_modal_header_button.setAttribute("aria-label", "Close");
    var alert_modal_header_button_span = document.createElement("span");
    alert_modal_header_button_span.setAttribute("aria-hidden", "true");
    alert_modal_header_button_span.innerHTML = "&times;";
    alert_modal_header_button.appendChild(alert_modal_header_button_span);
    alert_modal_header.appendChild(alert_modal_header_title);
    alert_modal_header.appendChild(alert_modal_header_button);
    var alert_modal_body = document.createElement("div");
    alert_modal_body.setAttribute("class", "modal-body");
    alert_modal_body.innerHTML = alert_body;
    var alert_modal_footer = document.createElement("div");
    alert_modal_footer.setAttribute("class", "modal-footer");
    var alert_modal_footer_button = document.createElement("button");
    alert_modal_footer_button.setAttribute("type", "button");
    alert_modal_footer_button.setAttribute(
      "class",
      "doTemplate btn btn-" + alert_color
    );
    alert_modal_footer_button.setAttribute("data-dismiss", "modal");
    alert_modal_footer_button.innerHTML = alert_button;
    var alert_modal_footer_cancel = document.createElement("button");
    alert_modal_footer_cancel.setAttribute("type", "button");
    alert_modal_footer_cancel.setAttribute("class", "btn btn-secondary");
    alert_modal_footer_cancel.setAttribute("data-dismiss", "modal");
    alert_modal_footer_cancel.innerHTML = alert_cancel;
    alert_modal_footer.appendChild(alert_modal_footer_cancel);
    alert_modal_footer.appendChild(alert_modal_footer_button);
    alert_modal_content.appendChild(alert_modal_header);
    alert_modal_content.appendChild(alert_modal_body);
    alert_modal_content.appendChild(alert_modal_footer);
    alert_modal_dialog.appendChild(alert_modal_content);
    alert_modal.appendChild(alert_modal_dialog);
    document.body.appendChild(alert_modal);
    $("#alert_modal").modal("show");
    //execute function
    $(".doTemplate").click(function () {
      templateOneAdd();
    });
  }
  $("#templateAdd").click(function () {
    // display an alert box warning the user that this will empty the textarea
    alert_title = "Warning";
    alert_body = "This will empty the textarea. Are you sure?";
    alert_button = "Yes, I'm sure";
    alert_cancel = "Cancel";
    alert_color = "primary";
    alert_function = "templateOneAdd()";
    alert_modal(
      alert_title,
      alert_body,
      alert_button,
      alert_cancel,
      alert_color,
      alert_function
    );
  });
});
