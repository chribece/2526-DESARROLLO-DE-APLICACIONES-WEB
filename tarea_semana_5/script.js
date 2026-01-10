// Seleccionar elementos del DOM
const imageInput = document.getElementById('imageInput');
const addBtn = document.getElementById('addBtn');
const deleteBtn = document.getElementById('deleteBtn');
const gallery = document.getElementById('gallery');
const infoText = document.getElementById('infoText');
const errorMsg = document.getElementById('errorMsg');

// Variable para almacenar la imagen seleccionada
let selectedImage = null;

// ===== EVENTOS PRINCIPALES =====

// Agregar imagen al presionar el botón "Agregar Imagen"
addBtn.addEventListener('click', addImage);

// Agregar imagen al presionar la tecla Enter
imageInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
        addImage();
    }
});

// Eliminar imagen seleccionada
deleteBtn.addEventListener('click', deleteImage);

// Limpiar mensaje de error cuando el usuario empieza a escribir
imageInput.addEventListener('input', () => {
    errorMsg.textContent = '';
});

// ===== FUNCIONES PRINCIPALES =====

/**
 * Agrega una nueva imagen a la galería
 */
function addImage() {
    const url = imageInput.value.trim();
    
    // Validar que la URL no esté vacía
    if (!url) {
        showError('Por favor ingresa una URL');
        return;
    }

    // Validar que sea una URL válida
    if (!isValidUrl(url)) {
        showError('Por favor ingresa una URL válida (debe comenzar con http:// o https://)');
        return;
    }

    // Crear una imagen temporal para validar que carga correctamente
    const img = new Image();
    
    img.onload = () => {
        // La imagen cargó correctamente, crear el elemento en la galería
        const galleryItem = document.createElement('div');
        galleryItem.className = 'gallery-item';

        const imgElement = document.createElement('img');
        imgElement.src = url;
        imgElement.alt = 'Imagen de galería';

        galleryItem.appendChild(imgElement);

        // Agregar evento de click para seleccionar la imagen
        galleryItem.addEventListener('click', () => selectImage(galleryItem));

        // Eliminar el mensaje de galería vacía si existe
        const emptyMsg = gallery.querySelector('.empty-message');
        if (emptyMsg) {
            emptyMsg.remove();
        }

        // Agregar la imagen a la galería
        gallery.appendChild(galleryItem);
        
        // Limpiar el campo de entrada
        imageInput.value = '';
        errorMsg.textContent = '';
        
        // Actualizar la información
        updateInfoText();
        
        // Enfocar nuevamente el input
        imageInput.focus();
    };

    img.onerror = () => {
        showError('No se pudo cargar la imagen. Verifica que la URL sea correcta');
    };

    // Iniciar la carga de la imagen
    img.src = url;
}

/**
 * Selecciona una imagen y deselecciona las demás
 * @param {HTMLElement} element - El elemento de la galería a seleccionar
 */
function selectImage(element) {
    // Deseleccionar la imagen anterior si existe
    if (selectedImage) {
        selectedImage.classList.remove('selected');
    }

    // Seleccionar la nueva imagen
    selectedImage = element;
    selectedImage.classList.add('selected');
    
    // Habilitar el botón de eliminar
    deleteBtn.disabled = false;
    
    // Actualizar el texto informativo
    updateInfoText();
}

/**
 * Elimina la imagen seleccionada de la galería
 */
function deleteImage() {
    if (selectedImage) {
        // Eliminar el elemento del DOM
        selectedImage.remove();
        selectedImage = null;
        
        // Deshabilitar el botón de eliminar
        deleteBtn.disabled = true;
        
        // Actualizar la información
        updateInfoText();

        // Si no hay más imágenes, mostrar el mensaje de galería vacía
        if (gallery.children.length === 0) {
            const emptyMsg = document.createElement('div');
            emptyMsg.className = 'empty-message';
            emptyMsg.textContent = 'La galería está vacía. ¡Agrega una imagen para comenzar!';
            gallery.appendChild(emptyMsg);
        }
    }
}

/**
 * Actualiza el texto informativo según el estado de la galería
 */
function updateInfoText() {
    const imageCount = gallery.querySelectorAll('img').length;
    
    if (imageCount === 0) {
        infoText.textContent = 'Pega una URL de imagen y presiona Agregar o Enter';
    } else if (selectedImage) {
        infoText.textContent = `${imageCount} imagen(es) en la galería • Haz clic en otra imagen para cambiar la selección`;
    } else {
        infoText.textContent = `${imageCount} imagen(es) en la galería • Haz clic en una imagen para seleccionarla`;
    }
}

// ===== FUNCIONES DE VALIDACIÓN =====

/**
 * Valida que una cadena sea una URL válida
 * @param {string} string - La URL a validar
 * @returns {boolean} - True si es una URL válida, False en caso contrario
 */
function isValidUrl(string) {
    try {
        const url = new URL(string);
        return string.startsWith('http://') || string.startsWith('https://');
    } catch (_) {
        return false;
    }
}

/**
 * Muestra un mensaje de error al usuario
 * @param {string} message - El mensaje de error a mostrar
 */
function showError(message) {
    errorMsg.textContent = message;
}

// ===== INICIALIZACIÓN =====

// Enfocar el input al cargar la página
imageInput.focus();