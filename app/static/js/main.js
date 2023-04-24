document.addEventListener("DOMContentLoaded", function () {
  const deleteButton = document.getElementById("delete-button");
  if (deleteButton == null) {
    return "";
  }

  deleteButton.addEventListener("click", (e) => {
    if (!confirm("¿Estás seguro de querer eliminar el registro?")) {
      e.preventDefault();
      e.stopPropagation();
    }
  });
});

document.addEventListener("DOMContentLoaded", function () {
  const cancelButton = document.getElementById("cancel-button");
  if (cancelButton == null) {
    return "";
  }

  cancelButton.addEventListener("click", (e) => {
    if (!confirm("¿Estás seguro de querer cancelar la cita?")) {
      e.preventDefault();
      e.stopPropagation();
    }
  });
});

document.addEventListener("DOMContentLoaded", function () {
  const costInput = document.getElementById("cost-input");
  const costOutput = document.getElementById("cost-output");
  const costIvaOutput = document.getElementById("const-iva-output");
  const totalCost = document.getElementById("total-cost");

  if (costInput == null) {
    return "";
  }

  costInput.addEventListener("input", function (e) {
    if (e.target.value === "") {
      costOutput.value = "$" + 0;
      costIvaOutput.value = "$" + 0;
      totalCost.value = "$" + 0;
    } else {
      costOutput.value = "$" + parseInt(e.target.value).toLocaleString();
      costIvaOutput.value =
        "$" + (parseInt(e.target.value) * 0.19).toLocaleString();
      totalCost.value =
        "$" +
        (
          parseInt(e.target.value) +
          parseInt(e.target.value) * 0.19
        ).toLocaleString();
    }
  });
});

/* send forms data */

const sendBillButton = document.getElementById("send-bill-button");

sendBillButton.addEventListener("click", function () {
  const dataClient = new FormData(document.getElementById("data-client-form"));
  const prices = new FormData(document.getElementById("prices-form"));

  fetch("/cargar_factura", {
    method: "POST",
    body: new URLSearchParams([...dataClient, ...prices]),
  })
    .then(function (response) {
      return response.json();
    })
    .then(function (data) {
      window.location.href = data.redirect_url;
    });
});
