//Agregar usuario
document.getElementById('asignarProfesorBtn').addEventListener('click', function () {
    document.getElementById('containerAddStudents').style.display = 'none';
    document.getElementById('containerAddGrade').style.display = 'block';
  });

document.getElementById('volverBtn').addEventListener('click', function () {
    document.getElementById('containerAddGrade').style.display = 'none';
    document.getElementById('containerAddStudents').style.display = 'block';
  });

//Buscador

function buscarUsuario() {
  let input = document.getElementById("search"); // Obtener el valor del input
  let filter = input.value.toUpperCase(); // Convertir a mayúsculas para hacer la búsqueda sin importar el caso
  let table = document.getElementById("usuariosTable"); // Obtener la tabla
  let tr = table.getElementsByTagName("tr"); // Obtener todas las filas de la tabla
  let tfoot = document.querySelector("tfoot"); // Obtener el tfoot
  let hasResults = false; // Para saber si hay resultados visibles

  // Iterar sobre todas las filas y ocultar las que no coincidan con la búsqueda
  for (let i = 1; i < tr.length - 1; i++) { // Excluimos la última fila (tfoot)
      let td = tr[i].getElementsByTagName("td"); // Obtener todas las celdas de la fila
      let found = false; // Variable para saber si encontramos una coincidencia

      // Recorremos todas las celdas de la fila
      for (let j = 1; j < td.length; j++) { // Empezamos desde 1 para no afectar la columna de acciones
          if (td[j]) {
              let textValue = td[j].textContent || td[j].innerText;
              if (textValue.toUpperCase().indexOf(filter) > -1) {
                  found = true;
                  hasResults = true;
                  break; // Si encontramos una coincidencia, salimos del ciclo
              }
          }
      }

      // Mostramos u ocultamos la fila dependiendo de si encontramos una coincidencia
      tr[i].style.display = found ? "" : "none";
  }

  // Asegurar que el tfoot siempre se mantenga visible
  tfoot.style.display = hasResults ? "" : "table-footer-group";
}
