document.addEventListener("DOMContentLoaded", function () {
    setTimeout(function () {
        let alerta = document.getElementById("alerta-exito");
        if (alerta) {
            alerta.style.transition = "opacity 0.5s ease";
            alerta.style.opacity = "0";
            setTimeout(() => alerta.remove(), 500); // Después de ocultarlo, lo elimina del DOM
        }
    }, 5000); // 5000 ms = 5 segundos (Cambia a 10000 para 10 segundos)
});
