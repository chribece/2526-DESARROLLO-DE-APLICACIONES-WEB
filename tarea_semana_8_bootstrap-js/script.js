document.addEventListener('DOMContentLoaded', function() {
    
    // ===== VALIDACIÓN DEL FORMULARIO =====
    const form = document.getElementById('contactForm');
    const btnEnviar = document.getElementById('btnEnviar');
    const btnText = btnEnviar.querySelector('.btn-text');
    const btnLoading = btnEnviar.querySelector('.btn-loading');
    
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Obtener valores
        const nombre = document.getElementById('nombre').value.trim();
        const email = document.getElementById('email').value.trim();
        const mensaje = document.getElementById('mensaje').value.trim();
        
        let valido = true;
        
        // Validar nombre (mín 3 caracteres)
        if (nombre.length < 3) {
            document.getElementById('nombre').classList.add('is-invalid');
            valido = false;
        } else {
            document.getElementById('nombre').classList.remove('is-invalid');
            document.getElementById('nombre').classList.add('is-valid');
        }
        
        // Validar email
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
            document.getElementById('email').classList.add('is-invalid');
            valido = false;
        } else {
            document.getElementById('email').classList.remove('is-invalid');
            document.getElementById('email').classList.add('is-valid');
        }
        
        // Validar mensaje (mín 10 caracteres)
        if (mensaje.length < 10) {
            document.getElementById('mensaje').classList.add('is-invalid');
            valido = false;
        } else {
            document.getElementById('mensaje').classList.remove('is-invalid');
            document.getElementById('mensaje').classList.add('is-valid');
        }
        
        // Si es válido, enviar
        if (valido) {
            // Mostrar loading
            btnText.classList.add('d-none');
            btnLoading.classList.remove('d-none');
            btnEnviar.disabled = true;
            
            // Simular envío
            setTimeout(function() {
                // Alerta de éxito con Bootstrap
                alert('¡Mensaje enviado! Gracias por contactarnos. Te responderemos en menos de 24 horas.');
                
                // Resetear formulario
                form.reset();
                document.querySelectorAll('.is-valid').forEach(el => el.classList.remove('is-valid'));
                
                // Restaurar botón
                btnText.classList.remove('d-none');
                btnLoading.classList.add('d-none');
                btnEnviar.disabled = false;
            }, 2000);
        }
    });
    
    // Limpiar error al escribir
    ['nombre', 'email', 'mensaje'].forEach(id => {
        document.getElementById(id).addEventListener('input', function() {
            this.classList.remove('is-invalid');
        });
    });
    
    // ===== SMOOTH SCROLL =====
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const destino = document.querySelector(this.getAttribute('href'));
            if (destino) {
                // Cerrar menú móvil si está abierto
                const navbarCollapse = document.querySelector('.navbar-collapse');
                if (navbarCollapse.classList.contains('show')) {
                    navbarCollapse.classList.remove('show');
                }
                
                // Scroll suave
                destino.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
});