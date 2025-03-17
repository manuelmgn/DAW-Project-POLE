import { detectLocation, writeFromCoordinates } from './functions.js'
// =============================================================================
// FUNCIÓNS
// =============================================================================

// =============================================================================
// EXECUCIÓN (DOM CONTENT LOADED)
// =============================================================================
document.addEventListener('DOMContentLoaded', () => {
    // -------------------------------------------------------------------------
    // SELECIÓN DE CAMPOS
    // -------------------------------------------------------------------------
    const location = document.querySelector('#location')
    const coordinates = document.querySelector('#coordinates')

    writeFromCoordinates(coordinates, location)
})
