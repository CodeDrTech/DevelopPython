document.addEventListener('DOMContentLoaded', () => {
    const hourInputs = document.querySelectorAll('.hour-input');

    hourInputs.forEach(input => {
        input.addEventListener('input', (e) => {
            let value = e.target.value;

            // Eliminar caracteres no numéricos y permitir el caracter ":"
            value = value.replace(/[^0-9:]/g, '');

            // Limitar la longitud máxima a 4 caracteres
            if (value.length > 4) {
                value = value.slice(0, 4);
            }

            // Formatear como 0:00
            if (value.length > 1 && value.indexOf(':') === -1) {
                value = value.slice(0, 1) + ':' + value.slice(1);
            }

            e.target.value = value;
        });

        input.addEventListener('blur', (e) => {
            const value = e.target.value;

            // Validar formato cuando se pierda el foco
            const regex = /^[0-9]:[0-5][0-9]$/;
            if (!regex.test(value)) {
                e.target.setCustomValidity("El formato debe ser 0:00.");
            } else {
                e.target.setCustomValidity("");
            }
        });
    });
});