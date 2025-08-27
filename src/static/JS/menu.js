function toggleProfileBox() {
    var profileBox = document.getElementById('profileBox');

    if (profileBox.classList.contains('show')) {
        profileBox.classList.remove('show');
        profileBox.classList.add('hide');
        // Esperar a que termine la animación antes de ocultarlo completamente
        setTimeout(function () {
            profileBox.style.display = 'none';
        }, 500); // Duración igual a la transición en CSS (0.5s)
    } else {
        profileBox.style.display = 'block'; // Mostrar el cuadro antes de iniciar la animación
        setTimeout(function () {
            profileBox.classList.remove('hide');
            profileBox.classList.add('show');
        }, 10); // Permitir un pequeño retraso para que la transición funcione
    }
}

//menu-side
document.addEventListener('DOMContentLoaded', function () {
    const menuButton = document.getElementById('menuButton');
    const menuSidebar = document.getElementById('menuSidebar');

    function toggleMenu() {
        if (window.innerWidth <= 1200) {
            menuSidebar.classList.toggle('visible'); // Alterna la clase "visible"
        }
    }

    menuButton.addEventListener('click', toggleMenu);

    window.addEventListener('resize', function () {
        if (window.innerWidth > 1200) {
            menuSidebar.classList.remove('visible'); // Oculta el menú si la pantalla es grande
        }
    });
});

//profile


