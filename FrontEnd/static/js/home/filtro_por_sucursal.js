function filtrarPorSucursal() {
    const sucursalSeleccionada = document.getElementById("filtroSucursal").value;
    const productos = document.querySelectorAll(".producto");
    const contenedor = document.getElementById("contenedorProductos");
    const mensaje = document.getElementById("mensajeSeleccion");

    if (!sucursalSeleccionada || sucursalSeleccionada === "todas") {
        contenedor.classList.add("d-none");
        mensaje.classList.remove("d-none");
        productos.forEach((p) => p.classList.add("d-none"));
        return;
    }

    mensaje.classList.add("d-none");
    contenedor.classList.remove("d-none");

    productos.forEach((producto) => {
        const sucursal = producto.getAttribute("data-sucursal");
        producto.classList.toggle("d-none", sucursal !== sucursalSeleccionada);
    });
}
