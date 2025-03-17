function toggleFillIcon(link, icon, ruta, iconNormal, iconFill) {
    // Cambiar o icono na páxina correspondente
    if (window.location.pathname === ruta) {
        icon.classList.remove(iconNormal)
        icon.classList.add(iconFill)
    }

    // Cambiar o icono ao pasar o cursor
    link.addEventListener('mouseover', function () {
        icon.classList.remove(iconNormal)
        icon.classList.add(iconFill)
    })

    link.addEventListener('mouseout', function () {
        if (window.location.pathname !== ruta) {
            icon.classList.remove(iconFill)
            icon.classList.add(iconNormal)
        }
    })
}

document.addEventListener('DOMContentLoaded', function () {
    const homeLink = document.getElementById('home-link')
    const homeIcon = document.getElementById('home-icon')
    const mapLink = document.getElementById('map-link')
    const mapIcon = document.getElementById('map-icon')
    const forecastLink = document.getElementById('forecast-link')
    const forecastIcon = document.getElementById('forecast-icon')
    const userlogLink = document.getElementById('userlog-link')
    const userlogIcon = document.getElementById('userlog-icon')
    const profileLink = document.getElementById('profile-link')
    const profileIcon = document.getElementById('profile-icon')

    toggleFillIcon(homeLink, homeIcon, '/', 'bi-house', 'bi-house-fill')
    toggleFillIcon(
        mapLink,
        mapIcon,
        '/profile',
        'bi-compass',
        'bi-compass-fill'
    )
    toggleFillIcon(
        forecastLink,
        forecastIcon,
        '/forecast',
        'bi-cloud-sun',
        'bi-cloud-sun-fill'
    )
    toggleFillIcon(
        profileLink,
        profileIcon,
        '/user',
        'bi-person',
        'bi-person-fill'
    )
    toggleFillIcon(
        userlogLink,
        userlogIcon,
        '/userlogs/new',
        'bi-pencil',
        'bi-pencil-fill'
    )
})
