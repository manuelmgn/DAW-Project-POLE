// =============================================================================
// FUNCIÓNS
// =============================================================================

// =============================================================================
// DOM CONTENT LOADED
// =============================================================================

document.addEventListener('DOMContentLoaded', function () {
    // -------------------------------------------------------------------------
    // SELECCIÓNS
    // -------------------------------------------------------------------------
    const inputLocation = document.querySelector('#location')
    const divSuxestions = document.querySelector('#suggestions')
    const coordinatesInput = document.getElementById('coordinates')
    const userDeleteButton = document.querySelector('#user-delete')

    // -------------------------------------------------------------------------
    // REXISTRO -   LOCALIZACIÓN
    // -------------------------------------------------------------------------

    // Aquí encontramos melloras propostas por @MarcoMagán. Manteño os seus comentarios (en castellano) para mellor comprensión.
    
    inputLocation.addEventListener('click', () => {
        inputLocation.value = ''
        coordinatesInput.value = ''
    })

    let debounceTimer //Timer para retrasar consulta
    let isFetching = false //Bandera para evitar múltiples solicitudes

    inputLocation.addEventListener('input', function () {
        const query = this.value

        clearTimeout(debounceTimer) // Limpiar temporizador previo
        debounceTimer = setTimeout(() => {
            //Lanzar con retraso
            if (query.length > 2 && !isFetching) {
                // Solo buscar si hay más de 2 caracteres y no se estaba buscando
                isFetching = true // Marcar como buscando
                fetch(
                    `https://nominatim.openstreetmap.org/search?format=json&q=${query}`
                )
                    .then((response) => response.json())
                    .then((data) => {
                        divSuxestions.innerHTML = '' // Limpar sugerencias
                        if (data.length > 0) {
                            divSuxestions.style.display = 'block'
                            data.forEach((location) => {
                                const suggestionDiv =
                                    document.createElement('div')
                                suggestionDiv.className = 'suggestion'
                                suggestionDiv.textContent =
                                    location.display_name

                                // Ao facer clic na suxestión, garda as coordenadas
                                suggestionDiv.addEventListener(
                                    'click',
                                    function () {
                                        inputLocation.value =
                                            location.display_name
                                        coordinatesInput.value = JSON.stringify(
                                            [location.lat, location.lon]
                                        )
                                        divSuxestions.style.display = 'none' // Oculta suxestións
                                    }
                                )

                                divSuxestions.appendChild(suggestionDiv)
                            })
                        } else {
                            divSuxestions.style.display = 'none' // Ocultar se non hai resultados
                        }
                    })
                    .catch((error) => {
                        console.error('Error fetching data:', error)
                    })
                    .finally(() => {
                        isFetching = false // Restablecer bandera
                    })
            } else {
                divSuxestions.style.display = 'none' // Ocultar se hai menos de 3 caracteres
            }
        }, 300) // Tempo de atraso da petición
    })

    // Ocultar suxestions ao facer clic fóra do contedor
    document.addEventListener('click', function (event) {
        if (
            !divSuxestions.contains(event.target) &&
            event.target !== inputLocation
        ) {
            divSuxestions.style.display = 'none'
        }
    })

    // -------------------------------------------------------------------------
    // ADVERTENCIA BORRAR USUARIO
    // -------------------------------------------------------------------------

    userDeleteButton.addEventListener(
        'click',
        (event) => {
            confirmation = confirm(
                'Eliminar o perfil implica perder todos os teus rexistros. Esta opción non é reversíbel.\n😥 De verdade queres continuar?'
            )

            if (!confirmation) {
                event.preventDefault()
            }
        },
        false
    )
})
