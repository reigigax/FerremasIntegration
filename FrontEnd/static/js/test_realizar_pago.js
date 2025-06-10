document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("webpayForm");

    form.addEventListener("submit", async function (event) {
        event.preventDefault();

        const ordenCompra = document.getElementById("buy_order").value;
        const sesion = document.getElementById("session").value;
        const monto = document.getElementById("amount").value;

        try {
            const response = await fetch("http://127.0.0.1:5001/api/transaccion-webpay", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    orden_compra: ordenCompra,
                    sesion: sesion,
                    monto: parseFloat(monto)
                }),
            });
        
            const data = await response.json();

            if (data.url && data.token) {

                const formRedirect = document.createElement("form");
                formRedirect.method = "POST";
                formRedirect.action = data.url;

                const inputToken = document.createElement("input");
                inputToken.type = "hidden";
                inputToken.name = "token_ws";
                inputToken.value = data.token;

                formRedirect.appendChild(inputToken);
                document.body.appendChild(formRedirect);
                formRedirect.submit();
            } else {
                alert("No se pudo obtener URL de WebPay");
                console.error(data);
            }
        } catch (error) {
            alert("Error al realizar la transacción")
            console.error(error)
        }
    })
})