$(document).ready(function () {
  $(".toast").toast({ delay: 2000 }); // auto hide after 2 seconds
  $(".toast").toast("show");
  var deleteId;
  var table = $("#customerTable").DataTable({
    pageLength: 10,
    responsive: true,
    columnDefs: [
      { orderable: false, targets: 0 },
      { searchable: false, targets: [0, 1, 3, 5, 6, 7] },
    ],
    initComplete: function () {
      $("#mainTable").show();
      $(".pagination .paginate_button.page-item:nth-child(2) .page-link").text(
        "FIRST"
      );
      $(
        ".pagination .paginate_button.page-item:nth-last-child(2) .page-link"
      ).text("LAST");
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
          url: "/admin/delete_customer/" + deleteId,
          type: "POST",
          success: function (result) {
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
  $("#downloadButton").click(function (e) {
    e.preventDefault();
    var wb = XLSX.utils.table_to_book(
      document.getElementById("customerTable"),
      { sheet: "Sheet 1" }
    );
    var wbout = XLSX.write(wb, { bookType: "xlsx", type: "binary" });
    function s2ab(s) {
      var buf = new ArrayBuffer(s.length);
      var view = new Uint8Array(buf);
      for (var i = 0; i < s.length; i++) view[i] = s.charCodeAt(i) & 0xff;
      return buf;
    }
    saveAs(
      new Blob([s2ab(wbout)], { type: "application/octet-stream" }),
      "customers.xlsx"
    );
  });
});
