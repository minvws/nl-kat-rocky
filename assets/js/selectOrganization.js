
var selected_organization = document.getElementById('select-organization')
var active_organization = selected_organization.value

function changeNavigationUrl() {
    selected_organization = selected_organization.value
    var url = window.location.toString()
    window.location = url.replace(active_organization, selected_organization)
}

selected_organization.addEventListener("change", changeNavigationUrl)