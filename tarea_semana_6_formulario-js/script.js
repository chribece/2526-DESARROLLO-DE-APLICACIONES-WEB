
// Selección de elementos
const form = document.getElementById('registroForm');
const inputNombre = document.getElementById('nombre');
const inputEmail = document.getElementById('email');
const inputPassword = document.getElementById('password');
const inputConfirm = document.getElementById('confirmPassword');
const inputEdad = document.getElementById('edad');
const btnEnviar = document.getElementById('btnEnviar');

// Utilidades de UI
function setValidity(input, isValid, message = '') {
  const group = input.closest('.form-group');
  const errorEl = group.querySelector('.error');

  if (isValid === null) {
    // Estado neutro (sin tocar o vacío)
    input.classList.remove('is-valid', 'is-invalid');
    input.setAttribute('aria-invalid', 'false');
    if (errorEl) errorEl.textContent = '';
    return;
  }

  if (isValid) {
    input.classList.add('is-valid');
    input.classList.remove('is-invalid');
    input.setAttribute('aria-invalid', 'false');
    if (errorEl) errorEl.textContent = '';
  } else {
    input.classList.add('is-invalid');
    input.classList.remove('is-valid');
    input.setAttribute('aria-invalid', 'true');
    if (errorEl) errorEl.textContent = message;
  }
}

function isFormValid() {
  return [inputNombre, inputEmail, inputPassword, inputConfirm, inputEdad]
    .every(el => el.classList.contains('is-valid'));
}

function updateSubmitState() {
  btnEnviar.disabled = !isFormValid();
}

// Reglas de validación
function validarNombre() {
  const value = inputNombre.value.trim();
  if (value.length === 0) return setValidity(inputNombre, null), false;
  const ok = value.length >= 3;
  setValidity(inputNombre, ok, 'El nombre debe tener al menos 3 caracteres.');
  return ok;
}

function validarEmail() {
  const value = inputEmail.value.trim();
  if (value.length === 0) return setValidity(inputEmail, null), false;
  // Regex simple y efectiva para formato general
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/i;
  const ok = emailRegex.test(value);
  setValidity(inputEmail, ok, 'Ingresa un correo con formato válido (ej.: usuario@dominio.com).');
  return ok;
}

function validarPassword() {
  const value = inputPassword.value;
  if (value.length === 0) return setValidity(inputPassword, null), false;

  const minLen = value.length >= 8;
  const hasDigit = /\d/.test(value);
  const hasSpecial = /[!@#$%^&*()_\-+=\[{\]};:'",.<>/?\\|`~]/.test(value);

  const ok = minLen && hasDigit && hasSpecial;
  let msg = '';
  if (!ok) {
    msg = 'La contraseña debe tener 8+ caracteres, incluir al menos un número y un carácter especial.';
  }
  setValidity(inputPassword, ok, msg);

  // Si cambia la contraseña, revalidamos confirmación
  if (inputConfirm.value.length > 0) validarConfirmPassword();

  return ok;
}

function validarConfirmPassword() {
  const value = inputConfirm.value;
  if (value.length === 0) return setValidity(inputConfirm, null), false;

  const ok = value === inputPassword.value && value.length > 0;
  setValidity(inputConfirm, ok, 'Las contraseñas no coinciden.');
  return ok;
}

function validarEdad() {
  const raw = inputEdad.value.trim();
  if (raw.length === 0) return setValidity(inputEdad, null), false;

  const num = Number(raw);
  // Acepta enteros, >= 18, y no NaN
  const ok = Number.isFinite(num) && Math.floor(num) === num && num >= 18;
  setValidity(inputEdad, ok, 'Debes ser mayor o igual a 18 años.');
  return ok;
}

// Listeners de validación en tiempo real
[inputNombre, inputEmail, inputPassword, inputConfirm, inputEdad].forEach((el) => {
  el.addEventListener('input', () => {
    switch (el) {
      case inputNombre: validarNombre(); break;
      case inputEmail: validarEmail(); break;
      case inputPassword: validarPassword(); break;
      case inputConfirm: validarConfirmPassword(); break;
      case inputEdad: validarEdad(); break;
    }
    updateSubmitState();
  });

  // También validamos al salir del campo
  el.addEventListener('blur', () => {
    switch (el) {
      case inputNombre: validarNombre(); break;
      case inputEmail: validarEmail(); break;
      case inputPassword: validarPassword(); break;
      case inputConfirm: validarConfirmPassword(); break;
      case inputEdad: validarEdad(); break;
    }
    updateSubmitState();
  });
});

// Envío del formulario
form.addEventListener('submit', (e) => {
  e.preventDefault(); // No recargar; solo mostramos confirmación

  // Valida todo por si hay campos sin tocar
  const v1 = validarNombre();
  const v2 = validarEmail();
  const v3 = validarPassword();
  const v4 = validarConfirmPassword();
  const v5 = validarEdad();

  updateSubmitState();

  if (v1 && v2 && v3 && v4 && v5) {
    alert('✅ ¡Formulario validado con éxito!'); // Puedes reemplazar por un modal/toast
    // Aquí podrías enviar datos (fetch/AJAX) si tuvieras un backend.
  } else {
    // Enfoca el primer campo inválido
    const firstInvalid = [inputNombre, inputEmail, inputPassword, inputConfirm, inputEdad]
      .find(el => !el.classList.contains('is-valid'));
    if (firstInvalid) firstInvalid.focus();
  }
});

// Reiniciar formulario: limpiamos estados
form.addEventListener('reset', () => {
  // Esperamos al reset nativo y luego limpiamos clases/errores
  setTimeout(() => {
    [inputNombre, inputEmail, inputPassword, inputConfirm, inputEdad].forEach((el) => {
      setValidity(el, null);
    });
    updateSubmitState();
  }, 0);
});
