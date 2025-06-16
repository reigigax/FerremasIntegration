document.addEventListener("DOMContentLoaded", function () {
    const forms = document.querySelectorAll(".modifyProduct");

    forms.forEach(form =>{
        form.addEventListener("submit", async function (event) {
            event.preventDefault();

            const idInput = form.querySelector("input[name='carrito_id_producto']");
            const cantidadInput = form.querySelector("input[name='carrito_cantidad_producto']")
            
            const idProducto = idInput ? idInput.value : null;
            const cantidadProducto = cantidadInput ? cantidadInput.value : null;

            if (!idProducto) {
                alert("ID de producto no encontrado");
                return;
            }
            if (!cantidadProducto) {
                alert("Cantidad de producto no encontrado");
                return;
            }

            const confirmar = confirm("¿Estas seguro de MODIFICAR este producto del carrito?");
            if(!confirmar) {location.reload()};

            try {
                const response = await fetch("http://127.0.0.1:5001/api/carrito/modificar-producto/"+idProducto, {
                    method: "PUT",
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({cantidad: parseInt(cantidadProducto)})
                });

                const data = await response.json()

                if(response.ok) {
                    alert(data.mensaje);
                    location.reload();
                } else {
                    alert(data.mensaje);
                }
            } catch (error) {
                console.error("No se pudo conectar al servidor:", error);
                alert("Error al modificar el Producto");
            }
        });
    });
});