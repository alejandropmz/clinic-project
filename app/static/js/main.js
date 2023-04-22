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
