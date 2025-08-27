document.getElementById("filterSelect").addEventListener("change", function() {
    let gradoContainer = document.getElementById("gradoSelectContainer");

    if (this.value === "grados") {
        gradoContainer.classList.add("visible"); // Muestra el contenedor
    } else {
        gradoContainer.classList.remove("visible"); // Oculta el contenedor
    }
});document.addEventListener("DOMContentLoaded", function () {
    const container = document.querySelector(".container-change");
    const block = container.querySelector(".block");
    const flex = container.querySelector(".flex");
    const boxes = document.querySelectorAll(".excuses-received"); // Selecciona todos los elementos

    function toggleState(target) {
        if (target.classList.contains("block") && !container.classList.contains("active")) return;
        if (target.classList.contains("flex") && container.classList.contains("active")) return;
        
        container.classList.toggle("active");
    }

    function addCambio() {
        boxes.forEach(box => box.classList.add("cambio")); // Agregar clase a todos los elementos
    }

    function removeCambio() {
        boxes.forEach(box => box.classList.remove("cambio")); // Remover clase de todos los elementos
    }

    block.addEventListener("click", function () {
        toggleState(block);
        removeCambio();
    });

    flex.addEventListener("click", function () {
        toggleState(flex);
        addCambio();
    });
});

// Mostrar u ocultar los filtros según la selección
document.getElementById('filterSelect').addEventListener('change', function(event) {
    event.preventDefault();  // Evita la recarga de la página

    var filterValue = this.value;

    // Lógica para mostrar u ocultar el select de grados o fecha según el filtro seleccionado
    if (filterValue === 'grados') {
        document.getElementById('gradoSelectContainer').style.display = 'block';
        document.getElementById('fechaSelectContainer').style.display = 'none';
    } else if (filterValue === 'fecha') {
        document.getElementById('gradoSelectContainer').style.display = 'none';
        document.getElementById('fechaSelectContainer').style.display = 'block';
    } else {
        document.getElementById('gradoSelectContainer').style.display = 'none';
        document.getElementById('fechaSelectContainer').style.display = 'none';
    }

    // Aplicar el filtro
    applyFilter();
});
// Función para aplicar los filtros y cambiar la URL sin recargar
function applyFilter() {
    var filterType = document.getElementById('filterSelect').value;
    var filterValue = '';

    // Obtener el valor del filtro seleccionado
    if (filterType === 'grados') {
        filterValue = document.getElementById('gradoSelect').value;
    } else if (filterType === 'fecha') {
        filterValue = document.getElementById('fechaSelect').value;
    }

    // Crear la nueva URL con los parámetros de filtro
    var url = new URL(window.location.href);
    if (filterType && filterValue) {
        url.searchParams.set('filter_type', filterType);
        url.searchParams.set('filter_value', filterValue);
    } else {
        url.searchParams.delete('filter_type');
        url.searchParams.delete('filter_value');
    }

    // Actualizar la URL sin recargar la página
    window.history.pushState({}, '', url);

    // Opcional: Ejecutar la lógica del filtro si es necesario (puedes usar Ajax o actualizar el DOM aquí)
    // Por ejemplo, enviar la solicitud de los filtros al backend para recargar los datos
}

// Función para mostrar los filtros dependiendo del tipo seleccionado
function toggleFilterFields() {
    var filterValue = document.getElementById('filterSelect').value;

    if (filterValue === 'grados') {
        document.getElementById('gradoSelectContainer').style.display = 'block';
        document.getElementById('fechaSelectContainer').style.display = 'none';
    } else if (filterValue === 'fecha') {
        document.getElementById('gradoSelectContainer').style.display = 'none';
        document.getElementById('fechaSelectContainer').style.display = 'block';
    } else {
        document.getElementById('gradoSelectContainer').style.display = 'none';
        document.getElementById('fechaSelectContainer').style.display = 'none';
    }
}

// Detectar cambios en el filtro principal
document.getElementById('filterSelect').addEventListener('change', function () {
    toggleFilterFields();
    applyFilter(); // Llamar para actualizar la URL
});

// Detectar cambios en los valores de los filtros secundarios
document.getElementById('gradoSelect').addEventListener('change', applyFilter);
document.getElementById('fechaSelect').addEventListener('change', applyFilter);

// Llamar a la función para mostrar el filtro correcto al cargar la página
toggleFilterFields();


document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.querySelector('.sekeer input[type="text"]');
    const filterSelect = document.getElementById('filterSelect');
    const gradoSelectContainer = document.getElementById('gradoSelectContainer');
    const gradoSelect = document.getElementById('gradoSelect');
    const fechaSelectContainer = document.getElementById('fechaSelectContainer');
    const excuseCards = document.querySelectorAll('.excuses-received');

    // Mostrar select correspondiente según el filtro elegido
    filterSelect.addEventListener('change', () => {
        const value = filterSelect.value;
        gradoSelectContainer.style.display = value === 'grados' ? 'block' : 'none';
        fechaSelectContainer.style.display = value === 'fecha' ? 'block' : 'none';
    });

    // Buscar por texto
    searchInput.addEventListener('input', () => {
        const searchTerm = searchInput.value.toLowerCase();

        excuseCards.forEach(card => {
            const studentName = card.querySelector('.student h2').textContent.toLowerCase();
            const parentName = card.querySelector('.father p').textContent.toLowerCase();
            const reason = card.querySelector('.rease .info-ex p').textContent.toLowerCase();
            const grade = card.querySelectorAll('.date .info-ex p')[1].textContent.toLowerCase(); // ← 2da fecha es el grado

            if (
                studentName.includes(searchTerm) ||
                parentName.includes(searchTerm) ||
                reason.includes(searchTerm) ||
                grade.includes(searchTerm)
            ) {
                card.style.display = '';
            } else {
                card.style.display = 'none';
            }
        });
    });

    // Filtrar por grado
    const fechaSelect = document.getElementById('fechaSelect');

    // Filtrar por fecha
    fechaSelect.addEventListener('change', () => {
        const selectedDate = fechaSelect.value; // formato YYYY-MM-DD
        excuseCards.forEach(card => {
            const dateText = card.querySelectorAll('.date .info-ex p')[0].textContent.trim(); // ← 1er bloque date
            const [day, month, year] = dateText.split('-');
            const cardDate = `${year}-${month.padStart(2, '0')}-${day.padStart(2, '0')}`; // Formato igual al del input

            if (selectedDate === '' || selectedDate === cardDate) {
                card.style.display = '';
            } else {
                card.style.display = 'none';
            }
        });
    });

});

document.addEventListener('DOMContentLoaded', () => {
    const fechaSelect = document.getElementById('fechaSelect');
    
    // Obtener la fecha de hoy
    const today = new Date();
    const dd = String(today.getDate()).padStart(2, '0');
    const mm = String(today.getMonth() + 1).padStart(2, '0'); // Mes empieza desde 0
    const yyyy = today.getFullYear();

    // Formatear la fecha a YYYY-MM-DD
    const todayFormatted = `${yyyy}-${mm}-${dd}`;

    // Establecer la fecha de hoy en el input
    fechaSelect.value = todayFormatted;
});
