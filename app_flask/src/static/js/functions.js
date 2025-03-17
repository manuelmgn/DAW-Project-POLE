// Detectar coordenadas do navegador
export async function detectLocation() {
    return new Promise((resolve, reject) => {
        navigator.geolocation.getCurrentPosition(
            (position) => {
                const latitude = position.coords.latitude
                const longitude = position.coords.longitude
                resolve(`${latitude.toString()},${longitude.toString()}`)
            },
            (error) => {
                console.error(
                    'Produciuse un erro ao tentar obter a localización:',
                    error
                )
                switch (error.code) {
                    case error.PERMISSION_DENIED:
                        reject('Permiso denegado.')
                        break
                    case error.POSITION_UNAVAILABLE:
                        reject('Información da localización non dispoñíbel.')
                        break
                    case error.TIMEOUT:
                        reject('O tempo da petición para a localización expirou.')
                        break
                    case error.UNKNOWN_ERROR:
                        reject('Aconteceu un erro ao tentar detectar a localización.')
                        break
                }
            }
        )
    })
}

// Procura o nome dun lugar a partir das coordenadas e o escribe no campo pasado por parámetro
export async function writeName(coords, nameInput) {
    const url = `https://nominatim.openstreetmap.org/search?format=json&q=${coords}`
    const response = await fetch(url)
    const data = await response.json()

    if (data.length > 0) {
        const nombre = data[0].display_name // O usa data[0].name se está dispoñíbel
        nameInput.value = nombre
    }
}

//
export async function writeFromCoordinates(coordField, cityField) {
    detectLocation()
        .then(async (coords) => {
            coordField.value = coords
            writeName(coords, cityField)
        })
        .catch((error) => {
            console.error('Erro ao obter a localización:', error)
        })
}
