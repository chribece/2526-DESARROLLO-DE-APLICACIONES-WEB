/**
 * RECLUTAPRO - Sistema de Reclutamiento
 * Scripts de interactividad
 */

document.addEventListener('DOMContentLoaded', function() {
    
    // Animación de números en stats
    const animateNumbers = () => {
        const numbers = document.querySelectorAll('.stat-number');
        numbers.forEach(num => {
            const final = parseInt(num.textContent);
            if (!isNaN(final)) {
                let current = 0;
                const increment = final / 50;
                const timer = setInterval(() => {
                    current += increment;
                    if (current >= final) {
                        num.textContent = final;
                        clearInterval(timer);
                    } else {
                        num.textContent = Math.floor(current);
                    }
                }, 20);
            }
        });
    };

    // Ejecutar animación si estamos en el dashboard
    if (document.querySelector('.stat-number')) {
        setTimeout(animateNumbers, 300);
    }

    // Confirmaciones para eliminar
    document.querySelectorAll('.btn-delete').forEach(btn => {
        btn.addEventListener('click', (e) => {
            if (!confirm('¿Está seguro de eliminar este registro?')) {
                e.preventDefault();
            }
        });
    });

    // Tooltips de Bootstrap
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    console.log('🎯 ReclutaPro - Sistema cargado correctamente');
});