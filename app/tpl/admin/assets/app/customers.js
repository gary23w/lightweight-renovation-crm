$(document).ready(function () {
  initializeToasts();
  initializeDataTable();
  handleDownloadButtonClick();
});

function initializeToasts() {
  $(".toast").toast({ delay: 2000 }); // Auto-hide after 2 seconds
  $(".toast").toast("show");
}

function initializeDataTable() {
  var deleteId;
  var table = $("#customerTable").DataTable({
    pageLength: 10,
    responsive: true,
    columnDefs: [
      { orderable: false, targets: 0 },
      { searchable: false, targets: [0, 1, 3, 5, 6, 7] },
    ],
    initComplete: function () {
      initializeCustomerTableInteraction(table, deleteId);
    },
  });
}

function initializeCustomerTableInteraction(table, deleteId) {
  $("#mainTable").show();
  $("#customerTable tbody").on("click", "tr", function () {
    handleTableRowClick(table, this, deleteId);
  });

  $("#deleteButton").click(function () {
    handleDeleteButtonClick(deleteId);
  });
}

function handleTableRowClick(table, row, deleteId) {
  var data = table.row(row).data();
  deleteId = data[0];
  var html = createDetailsHtml(data);
  $("#customerModal .modal-body").html(html);
  $("#customerModal").modal("show");
}

function createDetailsHtml(data) {
  var html = "";
  for (var i = 0; i < data.length; i++) {
    html +=
      "<p><b>" +
      $("#customerTable th").eq(i).text() +
      ": </b>" +
      data[i] +
      "</p>";
  }
  return html;
}

function handleDeleteButtonClick(deleteId) {
  $.ajax({
    url: "/admin/delete_customer/" + deleteId,
    type: "POST",
    success: function (result) {
      if (result.message === "deleted") {
        removeDeletedRow(deleteId);
      }
    },
  });
}

function removeDeletedRow(deleteId) {
  $("#customerTable tbody tr").each(function () {
    var rowId = $(this).find("td:first").text(); // Assuming the ID is in the first column (td)
    if (rowId === deleteId) {
      $(this).remove();
      $("#customerModal").modal("hide");
      return false;
    }
  });
}

function handleDownloadButtonClick() {
  $("#downloadButton").click(function (e) {
    e.preventDefault();
    downloadCustomerTableAsExcel();
  });
}

function downloadCustomerTableAsExcel() {
  var wb = XLSX.utils.table_to_book(document.getElementById("customerTable"), {
    sheet: "Sheet 1",
  });
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
}
