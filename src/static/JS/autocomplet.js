function formatIDCard(input) {
    let value = input.value.replace(/[^0-9]/g, ''); // Elimina caracteres no numéricos
    if (value.length > 3 && value.length <= 10) {
        input.value = value.substring(0, 3) + '-' + value.substring(3, 10) + (value.length > 10 ? '-' + value.substring(10, 11) : '');
    } else if (value.length > 10) {
        input.value = value.substring(0, 3) + '-' + value.substring(3, 10) + '-' + value.substring(10, 11);
    } else {
        input.value = value; // Mantén los números ingresados si son menores a 3
    }
}

function formatPhoneNumber(input) {
    let numbers = input.value.replace(/\D/g, '');
    let formatted = '';
    if (numbers.length > 0) {
        formatted = '(' + numbers.substring(0, 3);
    }
    if (numbers.length > 3) {
        formatted += ')-' + numbers.substring(3, 6);
    }
    if (numbers.length > 6) {
        formatted += '-' + numbers.substring(6, 10);
    }
    input.value = formatted;
}

function generatePassword(length = 10) {
    const chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()";
    let password = "";
    for (let i = 0; i < length; i++) {
        password += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    document.getElementById("passwordField").value = password;
}