document.addEventListener("DOMContentLoaded", function () {
    const forms = document.querySelectorAll(".addProductToCart");

    forms.forEach(form => {
        form.addEventListener("submit", async function (event) {
            event.preventDefault();

            const idInput = form.querySelector("input[name='carrito_id_producto']");
            const cantidadInput = form.querySelector("input[name='carrito_cantidad_producto']");

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

            try {
                const response = await fetch("http://127.0.0.1:5001/api/carrito/agregar-producto/"+idProducto, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        cantidad: parseInt(cantidadProducto)
                    }),
                });

                const data = await response.json()

                if (data["mensaje"] == "Cantidad para Agregar debe de ser mayor o igual a 1") {
                    alert(data["mensaje"])
                } else {
                    alert(data["mensaje"])
                    location.reload();
                }
            } catch (error) {
                alert("Error al agregar producto al carrito")
                console.error(error)
            }
        });
    });    
});