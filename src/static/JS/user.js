document.addEventListener('DOMContentLoaded', function () {
    const razonSelect = document.getElementById('razonSelect');
    const otroInput = document.getElementById('otroInput');

    // Mostrar u ocultar el input de "Especifica"
    razonSelect.addEventListener('change', function () {
        if (razonSelect.value === 'otros') {
            otroInput.style.display = 'block'; // Mostrar el input
        } else {
            otroInput.style.display = 'none'; // Ocultar el input
        }
    });

    // Asegurarse de que el valor correcto se envíe al servidor
    const form = document.querySelector('form');
    form.addEventListener('submit', function (event) {
        if (razonSelect.value === 'otros' && otroInput.value.trim() === '') {
            alert('Por favor, especifica la razón.');
            event.preventDefault(); // Evitar que el formulario se envíe
        } else if (razonSelect.value === 'otros') {
            // Si se selecciona "Otros", enviar el valor del input de "Especifica"
            razonSelect.value = otroInput.value;
        }
    });
});

// Función para obtener la fecha actual en formato YYYY-MM-DD
function getCurrentDate() {
    const now = new Date();
    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, '0'); // Meses van de 0 a 11
    const day = String(now.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
}

// Asignar la fecha actual al campo de fecha
document.getElementById('date').value = getCurrentDate();


document.getElementById('file').addEventListener('change', function (e) {
    const fileName = e.target.files[0].name;
    document.querySelector('.file-name').textContent = `Archivo seleccionado: ${fileName}`;
});

//autocompletador de estudiantes
document.addEventListener('DOMContentLoaded', () => {
    const gradSelect = document.getElementById('grad');
    const studentInput = document.getElementById('studentName');
    const datalist = document.getElementById('studentSuggestions');
    const parentId = document.getElementById('parentData').dataset.parentId;

    async function cargarEstudiantesPorGrado() {
        const grade = gradSelect.value;
        datalist.innerHTML = '';

        if (!grade) return;

        try {
            const response = await fetch(`/GESDE/get_students?grade=${encodeURIComponent(grade)}&parent_id=${parentId}`);
            
            const contentType = response.headers.get('content-type');
            if (!contentType || !contentType.includes('application/json')) {
                const text = await response.text();
                throw new Error(`Respuesta no JSON: ${text.substring(0, 100)}...`);
            }

            const students = await response.json();

            if (Array.isArray(students)) {
                students.forEach(name => {
                    const option = document.createElement('option');
                    option.value = name;
                    datalist.appendChild(option);
                });
            } else {
                console.error('La respuesta no es un array:', students);
            }
        } catch (error) {
            console.error('Error al cargar estudiantes:', error);
            const option = document.createElement('option');
            option.value = `Error: ${error.message}`;
            datalist.appendChild(option);
        }
    }

    gradSelect.addEventListener('change', cargarEstudiantesPorGrado);

    studentInput.addEventListener('focus', () => {
        if (gradSelect.value) {
            cargarEstudiantesPorGrado();
        }
    });
});


document.addEventListener('DOMContentLoaded', function() {
    fetch('/suggest_excuse')
        .then(response => response.json())
        .then(data => {
            if (data.suggestion) {
                // Asignar la sugerencia como placeholder en el input de descripción
                document.querySelector('input[name="specification"]').placeholder = data.suggestion;
            }
        })
        .catch(error => console.error('Error al obtener la sugerencia:', error));
});

//Home

document.addEventListener("DOMContentLoaded", function() {
    // Animación para el nombre (el span)
    const animatedName = document.getElementById("animatedName");
    if (animatedName) {
      const originalNameText = animatedName.textContent;
      animatedName.textContent = "";
      originalNameText.split("").forEach((char, index) => {
        const span = document.createElement("span");
        if (char === " ") {
          span.innerHTML = "&nbsp;";
        } else {
          span.textContent = char;
        }
        span.style.display = "inline-block";
        span.style.opacity = "0";
        span.style.animation = "fadeInLeft 0.5s ease-out " + (index * 0.1) + "s forwards";
        // (El nombre se muestra en verde según tu CSS para .container-lef h1 span)
        animatedName.appendChild(span);
      });
    }
  
    // Animación para el párrafo, con retraso adicional de 1 segundo
    const animatedP = document.getElementById("animatedP");
    if (animatedP) {
      const originalPText = animatedP.textContent;
      animatedP.textContent = "";
      originalPText.split("").forEach((char, index) => {
        const span = document.createElement("span");
        if (char === " ") {
          span.innerHTML = "&nbsp;";
        } else {
          span.textContent = char;
        }
        span.style.display = "inline-block";
        span.style.opacity = "0";
        span.style.animation = "fadeInLeft 0.5s ease-out " + ((index * 0.03) + 1) + "s forwards";
        // Forzamos el color del párrafo para cada span
        span.style.color = "#a2d2ff";
        animatedP.appendChild(span);
      });
    }
  });
  
//profile

function openEditProfile() {
    const container = document.getElementById('editProfileContainer');
    container.style.display = 'flex';
}

function closeEditProfile() {
    const container = document.getElementById('editProfileContainer');
    container.style.display = 'none';
}
