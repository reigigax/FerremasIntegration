document.addEventListener("DOMContentLoaded", function () {
    const btnVaciarCarrito = document.getElementById("deleteCart");

    btnVaciarCarrito.addEventListener("submit", async function (event) {
        event.preventDefault();

        const confirmation = confirm("¿Estas seguro de que deseas de Vaciar el Carrito?")
        if (!confirmation) return;

        try {
            const response = await fetch( "http://127.0.0.1:5001/api/carrito/vaciar", {
                method: "DELETE"
            });
            const data = await response.json()

            if (response.ok) {
                alert(data.mensaje);
                location.reload();
            } else {
                alert("Error: " + data.error);
                console.error(data.descripcion_error);
            }
        } catch (error) {
            alert("Error al vaciar el carrito")
            console.error(error)
        }
    });
});