function agregarAlCarrito(event, id_producto) {
    event.preventDefault();

    const form = event.target;
    const cantidad = form.querySelector(
        'input[name="carrito_cantidad_producto"]'
    ).value;

    fetch(`http://127.0.0.1:5001/api/carrito/agregar-producto/${id_producto}`, {
        method: "POST",
        headers: {
        "Content-Type": "application/json",
        },
        body: JSON.stringify({ cantidad: cantidad }),
    })
        .then((res) => res.json())
        .then((data) => {
        if (data.mensaje && data.mensaje.includes("Satisfactoriamente")) {
            alert("✅ Producto agregado al carrito");
            window.location.href = "/carrito";
        } else {
            alert("❌ " + (data.mensaje || "Error al agregar"));
        }
        })
        .catch((err) => {
        console.error(err);
        alert("❌ Error de conexión con el servidor");
        });

    return false;
}
