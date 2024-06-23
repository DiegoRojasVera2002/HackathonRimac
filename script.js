let map;
let markers = [];
let circle;

function initMap() {
    // Inicializar el mapa
    map = new google.maps.Map(document.getElementById('map'), {
        center: { lat: -12.0464, lng: -77.0428 }, // Centro inicial del mapa (Lima, Perú)
        zoom: 12 // Zoom inicial del mapa
    });

    // Cargar y mostrar las ubicaciones desde el JSON local
    fetch('locations.json')
        .then(response => response.json())
        .then(locations => {
            locations.forEach(location => {
                addMarker(location);
            });
        })
        .catch(error => console.error('Error fetching locations:', error));

    // Obtener y mostrar la ubicación en tiempo real
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(position => {
            const userLocation = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
            };

            // Mostrar marcador para la ubicación en tiempo real
            const userMarker = new google.maps.Marker({
                position: userLocation,
                map: map,
                title: 'Tu Ubicación',
                icon: {
                    url: 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png'
                }
            });

            // Dibujar un círculo de 1 kilómetro alrededor de la ubicación en tiempo real
            circle = new google.maps.Circle({
                strokeColor: '#FF0000',
                strokeOpacity: 0.8,
                strokeWeight: 2,
                fillColor: '#FF0000',
                fillOpacity: 0.35,
                map: map,
                center: userLocation,
                radius: 1000 // Radio en metros (1 kilómetro)
            });

            // Centrar el mapa en la ubicación en tiempo real
            map.setCenter(userLocation);
        }, error => {
            console.error('Error getting user location:', error);
        });
    } else {
        console.error('Geolocation is not supported by this browser.');
    }
}

function addMarker(location) {
    const marker = new google.maps.Marker({
        position: { lat: location.latitud, lng: location.longitud },
        map: map,
        title: location.descripcion,
        icon: {
            url: 'http://maps.google.com/mapfiles/ms/icons/red-dot.png' // Marcador rojo
        }
    });

    // Dibujar un círculo de 250 metros alrededor del marcador
    const circle = new google.maps.Circle({
        strokeColor: '#800080', // Color violeta
        strokeOpacity: 0.8,
        strokeWeight: 2,
        fillColor: '#800080',
        fillOpacity: 0.35,
        map: map,
        center: { lat: location.latitud, lng: location.longitud },
        radius: 250 // Radio en metros (250 metros)
    });

    markers.push(marker); // Agregar marcador al array de marcadores
}

// Función para agregar una nueva ubicación con un marcador naranja y un círculo amarillo
function addNewLocation(lat, lng) {
    const newLocation = {
        latitud: lat,
        longitud: lng,
        descripcion: 'Nueva Ubicación' // Descripción opcional para el título del marcador
    };

    addNewMarker(newLocation); // Llama a la función addMarker con la nueva ubicación
}

// Función para agregar un marcador y círculo según la ubicación proporcionada
function addNewMarker(location) {
    // Marcador naranja
    const marker = new google.maps.Marker({
        position: { lat: location.latitud, lng: location.longitud },
        map: map,
        title: location.descripcion, // Usa la descripción como título del marcador
        icon: {
            url: 'http://maps.google.com/mapfiles/ms/icons/orange-dot.png' // Icono naranja
        }
    });

    // Círculo amarillo de 1 kilómetro de radio
    const circle = new google.maps.Circle({
        strokeColor: '#FFFF00', // Color amarillo
        strokeOpacity: 0.8,
        strokeWeight: 2,
        fillColor: '#FFFF00',
        fillOpacity: 0.35,
        map: map,
        center: { lat: location.latitud, lng: location.longitud },
        radius: 1000 // Radio en metros (1 kilómetro)
    });

    markers.push(marker); // Agregar marcador al array de marcadores
}
