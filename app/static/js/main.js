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

document.addEventListener("DOMContentLoaded", function () {
  const writtenNumbers = require("written-number");

  console.log(writtenNumbers(123));

  console.log(writtenNumbers.toWords(num));
});

document.addEventListener("DOMContentLoaded", function () {
  const sendBillButton = document.getElementById("send-bill-button");

  if (sendBillButton == null) {
    return "";
  }

  sendBillButton.addEventListener("click", function () {
    const dataClient = new FormData(
      document.getElementById("data-client-form")
    );
    const appointmentInfo = new FormData(
      document.getElementById("appointment-info-form")
    );
    const appoinmentPrices = new FormData(
      document.getElementById("prices-form")
    );

    const observations = new FormData(document.getElementById("observations"));

    fetch("/guardar_factura", {
      method: "POST",
      body: new URLSearchParams([
        ...dataClient,
        ...appointmentInfo,
        ...appoinmentPrices,
        ...observations,
      ]),
    })
      .then(function (response) {
        return response.json();
      })
      .then(function (data) {
        window.location.href = data.redirect_url;
      });
  });
});

document.addEventListener("DOMContentLoaded", function () {
  const changePaidButton = document.getElementById("change-paid-button");

  if (changePaidButton == null) {
    return "";
  }

  changePaidButton.addEventListener("click", (e) => {
    if (!confirm("¿Marcar la factura como paga?")) {
      e.preventDefault();
      e.stopPropagation();
    }
  });
});
