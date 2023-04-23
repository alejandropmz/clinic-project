document.addEventListener("DOMContentLoaded", function () {
  const deleteButton = document.getElementById("delete-button");

  deleteButton.addEventListener("click", (e) => {
    if (!confirm("¿Estás seguro de querer eliminar el registro?")) {
      e.preventDefault();
      e.stopPropagation();
    }
  });
});

document.addEventListener("DOMContentLoaded", function () {
  const cancelButton = document.getElementById("cancel-button");
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
  const constIvaOutput = document.getElementById("const-iva-output");
  const totalCost = document.getElementById("total-cost");

  costInput.addEventListener("input", function (e) {
    if (e.target.value === "") {
      costOutput.value = "$" + 0;
      constIvaOutput.value = "$" + 0;
      totalCost.value = "$" + 0;
    } else {
      costOutput.value = "$" + parseInt(e.target.value).toLocaleString();
      constIvaOutput.value =
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
