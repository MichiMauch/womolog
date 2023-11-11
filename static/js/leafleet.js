document.addEventListener('DOMContentLoaded', function () {
    var mapElement = document.getElementById('mapid');

    // Prüfe, ob das Element Koordinaten für mehrere Marker hat
    var markersData = mapElement.getAttribute('data-markers');
    var map, initialLat, initialLng;

    if (markersData) {
        // Es gibt mehrere Marker
        var markers = JSON.parse(markersData);

        // Überprüfe, ob das erste Marker-Objekt gültig ist, um die Karte zu zentrieren
        if (markers.length > 0 && markers[0].latitude && markers[0].longitude) {
            initialLat = parseFloat(markers[0].latitude);
            initialLng = parseFloat(markers[0].longitude);
        } else {
            console.error("Invalid initial marker coordinates");
            return;
        }
    } else {
        // Nur ein einzelner Marker vorhanden
        var latitude = parseFloat(mapElement.getAttribute('data-latitude'));
        var longitude = parseFloat(mapElement.getAttribute('data-longitude'));
        if (!isNaN(latitude) && !isNaN(longitude)) {
            initialLat = latitude;
            initialLng = longitude;
        } else {
            console.error("Invalid marker coordinates");
            return;
        }
    }
    var map = L.map('mapid', {
        fullscreenControl: true, // Aktiviert die Vollbild-Steuerung
        // OPTIONAL: Verwenden Sie Ihre eigenen Vollbild-Button-Optionen
        fullscreenControlOptions: {
            position: 'topleft'
        }
    }).setView([initialLat, initialLng], 13);
    // Initialisiere die Karte mit den Koordinaten des ersten Markers oder des einzelnen Markers
    // map = L.map('mapid').setView([initialLat, initialLng], 13);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    if (markersData) {
        // Füge alle Marker hinzu
        markers.forEach(function (markerData) {
            var markerLat = parseFloat(markerData.latitude);
            var markerLng = parseFloat(markerData.longitude);
            var url = markerData.url; // URL aus den Marker-Daten holen
            if (!isNaN(markerLat) && !isNaN(markerLng)) {
                var markerIconUrl = markerData.marker_icon;
                var customIcon = L.icon({
                    iconUrl: markerIconUrl,
                    iconSize: [32, 32],
                    iconAnchor: [16, 32],
                    popupAnchor: [0, -32]
                });

                L.marker([markerLat, markerLng], { icon: customIcon })
                    .addTo(map)
                    .bindPopup('<a href="' + url + '" target="_blank">' + markerData.name + '</a>');


            }
        });
    } else {
        // Füge den einzelnen Marker hinzu
        var markerIconUrl = mapElement.getAttribute('data-marker-icon');
        var customIcon = L.icon({
            iconUrl: markerIconUrl,
            iconSize: [32, 32],
            iconAnchor: [16, 32],
            popupAnchor: [0, -32]
        });

        L.marker([initialLat, initialLng], { icon: customIcon }).addTo(map);
    }
});
