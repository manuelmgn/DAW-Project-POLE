// =============================================================================
// FUNCIÓNS XERAIS
// =============================================================================

// Función para validar unha coordenada
function checkCoord(coord) {
    const num = parseFloat(coord)
    return !isNaN(num) && isFinite(num)
}

// Función para validar un par de coordenadas
function checkCoordPair(coords) {
    if (!Array.isArray(coords) || coords.length !== 2) return false
    const lat = parseFloat(coords[0])
    const lng = parseFloat(coords[1])
    return (
        checkCoord(lat) &&
        checkCoord(lng) &&
        lat >= -90 &&
        lat <= 90 &&
        lng >= -180 &&
        lng <= 180
    )
}

// Función que devolve as cores correspondes a cada grao de intensidade
function getSeverityColor(severity) {
    const colors = {
        1: '#14e622',
        2: '#8ec200',
        3: '#bd9b00',
        4: '#db6900',
        5: '#e62214',
    }
    // Cor en caso de erro
    return colors[severity] || '#ffffff'
}

// =============================================================================
// FUNCIÓNS PRINCIPAIS
// =============================================================================

// Función para mostrar o mapa principal
function showLogsMaps(userLogsPropios) {
    // Percorre cada un dos logs
    userLogsPropios.forEach((log, index) => {
        // Verifica que existen localización e coordenadas
        if (!log.location || !log.location.coordinates) {
            console.warn('O rexistro non ten unhas coordenadas válidas:', log)
            return
        }

        // Valida as coordenadas
        if (!checkCoordPair(log.location.coordinates)) {
            console.warn('Coordenadas inválidas:', log.location.coordinates)
            return
        }

        // Crea os atributos do mapa
        let mapId = `map-${index + 1}`
        let coords = log.location.coordinates.map((coord) => parseFloat(coord))

        // Crea o mapa
        let map = L.map(mapId).setView(coords, 13)

        // Capa de fondo
        // Modo light: https://tiles.stadiamaps.com/tiles/alidade_smooth
        L.tileLayer(
            'https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}.png',
            {
                minZoom: 8,
                maxZoom: 18,
                attribution:
                    '&copy; <a href="https://www.stadiamaps.com/" target="_blank">Stadia Maps</a> &copy; <a href="https://openmaptiles.org/" target="_blank">OpenMapTiles</a> &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
                ext: 'png',
            }
        ).addTo(map)

        // Icono personalizado
        const markerIcon = L.divIcon({
            html: `<div style="background-color: ${getSeverityColor(
                log.severity
            )};
                                width: 1rem;
                                height: 1rem;
                                border-radius: 50%;
                                border: 2px solid white;
                                box-shadow: 0 0 6px rgba(0,0,0,0.5);">
                      </div>`,
            className: 'custom-marker',
            iconSize: [16, 16],
            iconAnchor: [8, 8],
        })

        // Marcadores
        L.marker(coords, { icon: markerIcon })
            .bindPopup(
                `
                    <strong>Lugar:</strong> ${log.timestamp.split('T')[0]}<br>
                    <strong>Hora:</strong> ${log.timestamp.split('T')[1]}<br>
                    <strong>Intensidade:</strong> ${log.severity}
                `
            )
            .addTo(map)
    })
}

function showGreapMap(userlogs) {
    const pointsMap = new Map()

    userlogs.forEach((log) => {
        if (
            !log.location ||
            !log.location.coordinates ||
            !checkCoordPair(log.location.coordinates)
        ) {
            console.warn('Rexistro inválido:', log)
            return
        }

        const coords = log.location.coordinates.map((coord) =>
            parseFloat(coord)
        )
        const key = coords.join(',')

        // Comprobamos que severity teña un valor válido
        const severity = Math.max(1, Math.min(5, parseInt(log.severity)))

        if (pointsMap.has(key)) {
            const existing = pointsMap.get(key)
            // Actualizamos o contador
            existing.severityCounts[severity] =
                (existing.severityCounts[severity] || 0) + 1
            pointsMap.set(key, {
                ...existing,
                coords: coords,
                totalCount: existing.totalCount + 1,
            })
        } else {
            const severityCounts = {}
            severityCounts[severity] = 1
            pointsMap.set(key, {
                coords: coords,
                severityCounts: severityCounts,
                totalCount: 1,
            })
        }
    })

    // Creamos un array de puntos para o mapa de calor
    const heatPoints = []
    pointsMap.forEach((point) => {
        Object.entries(point.severityCounts).forEach(([severity, count]) => {
            // Calculamos a proporción de puntos con esa severidade
            const proportion = count / point.totalCount
            heatPoints.push({
                lat: point.coords[0],
                lng: point.coords[1],
                severity: parseInt(severity),
                // Axustamos a intensidade en función da proporción
                intensity: proportion * 0.4,
            })
        })
    })

    // Verificación de puntos válidos
    if (heatPoints.length === 0) {
        console.warn('Non hai puntos válidos para mostrar no mapa')
        document.getElementById('map').innerHTML =
            'Non hai datos válidos para mostrar'
        throw new Error('Non hai puntos válidos para mostrar')
    }

    // Inicialización do mapa
    const bounds = L.latLngBounds(heatPoints.map((p) => [p.lat, p.lng]))
    const center = bounds.getCenter()

    const map = L.map('map').setView(
        center.lat && center.lng ? [center.lat, center.lng] : [42.8, -8.5],
        10
    )

    // Capa de mapa base
    L.tileLayer(
        'https://{s}.basemaps.cartocdn.com/light_nolabels/{z}/{x}/{y}{r}.png',
        {
            attribution:
                '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
            subdomains: 'abcd',
            maxZoom: 10,
            minZoom: 5,
        }
    ).addTo(map)

    // Capas do heatmap
    const severityColors = {
        1: '#00ff00', // Verde
        2: '#ffff00', // Amarelo
        3: '#ffa500', // Laranxa
        4: '#ff8c00', // Laranxa-vermello
        5: '#ff0000', // Vermello
    }

    // Agrupamos os puntos por intensidade
    const pointsBySeverity = heatPoints.reduce((acc, point) => {
        if (!acc[point.severity]) {
            acc[point.severity] = []
        }
        acc[point.severity].push([point.lat, point.lng, point.intensity])
        return acc
    }, {})

    // Crea unha capa de heatmap para cada nivel de intensidade
    Object.entries(pointsBySeverity).forEach(([severity, points]) => {
        const heat = L.heatLayer(points, {
            radius: 30,
            blur: 40,
            maxZoom: 8,
            minOpacity: 0.25,
            max: 1.0,
            gradient: {
                0.8: severityColors[severity],
                1.0: 'rgba(0,0,0,0)', // Transparente nos bordes
            },
        }).addTo(map)
    })

    // Zoom
    if (heatPoints.length > 0) {
        map.fitBounds(bounds, { padding: [50, 50] })
    }
}
