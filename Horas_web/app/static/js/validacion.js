document.addEventListener('DOMContentLoaded', () => {
    const hourInputs = document.querySelectorAll('.hour-input');

    hourInputs.forEach(input => {
        input.addEventListener('input', (e) => {
            let rawValue = e.target.value.replace(/[^\d]/g, ''); // Eliminar todo excepto números
            let formattedValue = '';

            // Limitar a 3 dígitos (para formato H:MM)
            if (rawValue.length > 3) rawValue = rawValue.slice(0, 3);

            // Formatear automáticamente
            if (rawValue.length === 1) {
                formattedValue = `${rawValue}:00`; // Ej: "2" → "2:00"
            } else if (rawValue.length >= 2) {
                const horas = rawValue[0];
                const minutos = rawValue.slice(1, 3).padEnd(2, '0'); // Rellenar con ceros
                formattedValue = `${horas}:${minutos}`;
            }

            // Actualizar el valor y asegurar máximo 4 caracteres
            e.target.value = formattedValue.slice(0, 4);
        });

        // Validación al perder el foco
        input.addEventListener('blur', (e) => {
            const value = e.target.value;
            const regex = /^\d:[0-5]\d$/;

            if (!regex.test(value)) {
                e.target.setCustomValidity('Formato inválido. Ejemplo: 2:30');
                e.target.reportValidity();
            } else {
                e.target.setCustomValidity('');
            }
        });
    });
});