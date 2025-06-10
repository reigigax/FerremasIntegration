document.getElementById("searchForm").addEventListener("submit", async function (event) {
    event.preventDefault();
    const id = document.getElementById("id_product").value;

    try {
        const response = await fetch("http://127.0.0.1:5001/api/obtener-producto-id/" + id);
        const data = await response.json();

        const resultadoDiv = document.getElementById("resultado");
        if (data.producto) {
            resultadoDiv.innerHTML = `${data.producto.id_producto}
                        ${data.producto.codigo_producto}
                        ${data.producto.marca_producto}
                        ${data.producto.nombre_producto}
                        ${data.producto.categoria_producto}
                        ${data.producto.stock}
                        ${data.producto.sucursal}
                        ${data.producto.valor}`;
        } else {
            resultadoDiv.innerHTML = `<p style="color:red;">${data.mensaje || data.mensaje_error}</p>`;}
    } catch (error) {
        document.getElementById("resultado").innerHTML = `<p style="color:red;">Error al buscar producto</p>`;
        console.error(error);
    }
});