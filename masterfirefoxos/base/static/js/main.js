;(function() {

function selectChangeLocation(id) {
    var select = document.getElementById(id);
    var selected = select.options[select.selectedIndex];
    select.addEventListener('change', function(event) {
        window.location = window.location.pathname.replace(
            selected.value, event.target.value);
    });
}

selectChangeLocation('language');
selectChangeLocation('version');
})();
