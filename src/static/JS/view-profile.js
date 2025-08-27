document.addEventListener('DOMContentLoaded', function() {
    // Manejar clic en los botones de ver perfil
    document.addEventListener('click', function(e) {
        const verBtn = e.target.closest('.ver-perfil-btn') || 
                       (e.target.classList.contains('see') && e.target.closest('a'));
        
        if (verBtn) {
            const userId = verBtn.dataset.userid || verBtn.closest('tr').querySelector('td:nth-child(2)').textContent;
            fetchUserProfile(userId);
        }
    });

    // Cerrar el modal
    document.querySelector('.close-btn').addEventListener('click', function() {
        document.querySelector('.contain-view-profile').style.display = 'none';
    });
});

function fetchUserProfile(userId) {
    fetch(`/GESDE/get_user_profile/${userId}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Error: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.error) {
                alert(data.error);
                return;
            }
            populateProfileModal(data);
            document.querySelector('.contain-view-profile').style.display = 'flex';
        })
        .catch(error => {
            console.error('Error al cargar perfil:', error);
            alert('Error al cargar el perfil del usuario');
        });
}

function populateProfileModal(userData) {
    // Llenar los campos del modal
    document.querySelector('.img-view h2').textContent = userData.nombre;
    document.querySelector('.text-img p').textContent = userData.rol;
    
    // Información principal
    const col1 = document.querySelector('.colum-view:nth-child(1)');
    col1.querySelector('.info-item:nth-child(1) p').textContent = userData.nombre;
    col1.querySelector('.info-item:nth-child(2) p').textContent = `ID-${userData.id}`;
    col1.querySelector('.info-item:nth-child(3) p').textContent = userData.cedula;
    col1.querySelector('.info-item:nth-child(4) p').textContent = userData.telefono;
    
    // Información secundaria (sin excusas)
    const col2 = document.querySelector('.colum-view:nth-child(2)');
    col2.querySelector('.info-item:nth-child(1) p').textContent = userData.ultima_actividad;
    col2.querySelector('.info-item:nth-child(2) p').textContent = userData.estado;
    
    // Opcional: Ocultar o eliminar el campo de excusas si existe en el HTML
    const excusasItem = col2.querySelector('.info-item:nth-child(3)');
    if (excusasItem && excusasItem.querySelector('h3').textContent.includes('Excusas')) {
        excusasItem.style.display = 'none';
    }
}