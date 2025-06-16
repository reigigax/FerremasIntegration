function filtrarPorSucursal() {
    const sucursalSeleccionada = document.getElementById("filtroSucursal").value;
    const productos = document.querySelectorAll(".producto");

    productos.forEach(producto => {
        const sucursal = producto.getAttribute("data-sucursal");

        if (sucursalSeleccionada === "todas" || sucursal === sucursalSeleccionada) {
            producto.style.display = "block";
        } else {
            producto.style.display = "none";
        }
    });
}