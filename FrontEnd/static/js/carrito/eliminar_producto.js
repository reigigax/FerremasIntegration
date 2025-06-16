document.addEventListener("DOMContentLoaded", function () {
    const forms = document.querySelectorAll(".deleteProduct");

    forms.forEach(form => {
        form.addEventListener("submit", async function (event) {
            event.preventDefault();

            const idInput = form.querySelector("input[name='carrito_id_producto']");
            const idProducto = idInput ? idInput.value : null;

            if (!idProducto) {
                alert("ID de producto no encontrado");
                return;
            }

            const confirmar = confirm("¿Estas seguro de ELIMINAR este producto del carrito?");
            if(!confirmar) return;

            try {
                const response = await fetch("http://127.0.0.1:5001/api/carrito/eliminar-producto/"+idProducto, {
                    method: "DELETE"
                });
                
                console.log(idProducto)
                const data = await response.json();

                if (response.ok) {
                    alert(data.mensaje);
                    location.reload();
                } else {
                    alert(data.mensaje);
                    console.error(data);
                }
            } catch (error) {
                console.error("No se pudo conectar al servidor:", error);
                alert("Error al eliminar el Producto");
            }
        });
    });
});