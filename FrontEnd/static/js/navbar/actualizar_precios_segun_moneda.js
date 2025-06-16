async function actualizarPrecios() {
    const tipoCambio = document.getElementById("tipoCambio").value;
    const precios = document.querySelectorAll(".precio");
    
    if (tipoCambio === "USD") {
        try{
            const respuesta = await fetch("http://127.0.0.1:5001/api/bancocentral/trimestre/ultimo-valor-dolar", {
                method:"GET"
            });
            const data = await respuesta.json()
            const tipoCambioMoneda = data["Valor Dolar"]

            precios.forEach(precio => {
                const valorOriginal = parseFloat(precio.getAttribute("data-valor"));
                const nuevoValor = (valorOriginal / tipoCambioMoneda).toFixed(2);
                precio.textContent ="$ " + nuevoValor + (tipoCambioMoneda === 1 ? " CLP" : " USD");
            });

        } catch (error) {
            console.error("Error al obtener tipo de cambio:", error);
            return;
        }
    } else {
        const tipoCambioMoneda = 1

        precios.forEach(precio => {
            const valorOriginal = parseFloat(precio.getAttribute("data-valor"));
            const nuevoValor = (valorOriginal * tipoCambioMoneda).toFixed(1);
            precio.textContent ="$ " + nuevoValor + (tipoCambioMoneda === 1 ? " CLP" : " USD");
        });
    }
}