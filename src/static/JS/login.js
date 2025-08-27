

function togglePassword() {
    const passwordInput = document.getElementById('passwordInput');
    const passwordIcon = document.getElementById('passwordIcon');

    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        passwordIcon.src = '/static/ASSETS/IMG/Login/iconLogin/eye-slash-svgrepo-com.svg'; // Cambiar a "ocultar"
        passwordIcon.alt = 'Ocultar contraseña';
    } else {
        passwordInput.type = 'password';
        passwordIcon.src = '/static/ASSETS/IMG/Login/iconLogin/eye-svgrepo-com.svg'; // Cambiar a "mostrar"
        passwordIcon.alt = 'Mostrar contraseña';
    }
}
