// Array de productos iniciales
let productos = [
    {
        id: 1,
        nombre: "PUNTA LADO CAJA KASHIMA CHEVROLET AVEO 1.4 CHEVROLET AVEO EMOTION 1.6",
        precio: 41.26,
        descripcion: "PUNTA LADO CAJA AVEO 1.4 2005 2019 L14 SD AVEO EMOTION 1.6 2005 2019 L44 SD"
    },
    {
        id: 2,
        nombre: "BATERIA LBN1R 600 BORNE POSITIVO LADO DERECHO ACDELCO CHEVROLET SPARK GT 1.2 CHEVROLET BEAT",
        precio: 135.65,
        descripcion: "Mouse inalámbrico con tecnología de precisión, batería de larga duración"
    },
    {
        id: 3,
        nombre: "LUBRICANTE ACEITE SAE 85W140 GL-5",
        precio: 180.71,
        descripcion: "LUBRICANTE ACEITE SAE 85W140 GL-5"
    }
 
];

// Función para renderizar la lista de productos
function renderizarProductos() {
    const container = document.getElementById('productContainer');
    
    if (productos.length === 0) {
        container.innerHTML = '<div class="empty-state"><p>No hay productos aún. ¡Agrega uno para comenzar!</p></div>';
        return;
    }

    const template = productos.map(producto => `
        <li class="product-item">
            <div class="product-name">${producto.nombre}</div>
            <div class="product-price">$${producto.precio.toFixed(2)}</div>
            <div class="product-description">${producto.descripcion}</div>
            <div class="product-id">ID: ${producto.id}</div>
        </li>
    `).join('');

    container.innerHTML = `<ul class="product-list">${template}</ul>`;
}

// Función para agregar un nuevo producto
function agregarProducto() {
    const nombre = document.getElementById('productName').value.trim();
    const precio = parseFloat(document.getElementById('productPrice').value);
    const descripcion = document.getElementById('productDescription').value.trim();

    // Validaciones
    if (!nombre) {
        alert('Por favor ingresa el nombre del producto');
        return;
    }
    if (isNaN(precio) || precio < 0) {
        alert('Por favor ingresa un precio válido');
        return;
    }
    if (!descripcion) {
        alert('Por favor ingresa una descripción');
        return;
    }

    // Crear nuevo producto
    const nuevoProducto = {
        id: productos.length > 0 ? Math.max(...productos.map(p => p.id)) + 1 : 1,
        nombre: nombre,
        precio: precio,
        descripcion: descripcion
    };

    // Agregar a la lista
    productos.push(nuevoProducto);

    // Limpiar formulario
    document.getElementById('productName').value = '';
    document.getElementById('productPrice').value = '';
    document.getElementById('productDescription').value = '';

    // Enfocar el primer campo
    document.getElementById('productName').focus();

    // Renderizar nuevamente
    renderizarProductos();
}

// Permitir agregar producto con Enter en el campo de nombre
document.getElementById('productName').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        document.getElementById('productPrice').focus();
    }
});

// Permitir agregar producto con Ctrl+Enter en la descripción
document.getElementById('productDescription').addEventListener('keypress', function(e) {
    if (e.key === 'Enter' && e.ctrlKey) {
        agregarProducto();
    }
});

// Renderizar al cargar la página
renderizarProductos();