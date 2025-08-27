window.onload = () => {
    // Cargar gráfico de excusas (pastel)
    fetch('/GESDE/chart/excusas')
        .then(response => response.json())
        .then(json => {
            const ctx = document.getElementById('excusasChart').getContext('2d');
            new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: json.labels,
                    datasets: [{
                        label: 'Total de excusas',
                        data: json.data,
                        backgroundColor: [
                            'rgba(0, 139, 252, 0.6)', 
                            'rgba(0, 201, 0, 0.6)', 
                            'rgba(255, 0, 0, 0.6)'
                        ],
                        borderColor: [
                            'rgba(0, 139, 252, 0.6)', 
                            'rgba(0, 201, 0, 0.6)', 
                            'rgba(255, 0, 0, 0.6)'
                        ],
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            display: false
                        }
                    }
                }
            });
        })
        .catch(err => console.error('Error cargando gráfico de excusas:', err));

    // Cargar gráfico de usuarios (barras)
    fetch('/GESDE/chart/usuarios')
        .then(response => response.json())
        .then(json => {
            const ctx = document.getElementById('usuariosChart').getContext('2d');
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: json.labels,
                    datasets: [{
                        label: 'Totales por categoría',
                        data: json.data,
                        backgroundColor: [
                            '#28a745',
                            '#dc3545',
                            '#17a2b8',
                            '#17a2b8',
                            '#ffc107',
                            '#218838',
                            '#ffc107'
                        ],
                        borderColor: '#333',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: {
                            display: false
                        }
                    },
                    plugins: {
                        legend: {
                            display: false
                        }
                    }
                }
            });
        })
        .catch(err => console.error('Error cargando gráfico de usuarios:', err));
};

document.addEventListener("DOMContentLoaded", function () {
    const toggleButton = document.getElementById('notificationToggle');
    const messageContainer = document.getElementById('containerMessages');
    const contentWrapper = document.getElementById('contentWrapper');
    const closeButton = document.querySelector('.close-btn');
  
    toggleButton.addEventListener('click', function () {
      contentWrapper.classList.add('fade-out');
      contentWrapper.addEventListener('animationend', () => {
        contentWrapper.style.display = 'flex';
        contentWrapper.classList.remove('fade-out');
  
        messageContainer.style.display = 'block';
        messageContainer.classList.add('fade-in');
      }, { once: true });
    });
  
    closeButton.addEventListener('click', function () {
      messageContainer.classList.add('fade-out');
      messageContainer.addEventListener('animationend', () => {
        messageContainer.style.display = 'none';
        messageContainer.classList.remove('fade-out');
  
        contentWrapper.style.display = 'flex';
        contentWrapper.classList.add('fade-in');
      }, { once: true });
    });
  });
  