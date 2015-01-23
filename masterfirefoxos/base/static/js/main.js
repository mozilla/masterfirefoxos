;(function() {

function selectChangeLocation(id) {
    select = document.getElementById(id);
    selected = select.options[select.selectedIndex]
    select.addEventListener('change', function(event) {
        window.location = window.location.href.replace(
            selected.value, event.target.value).split('?')[0];
    });
}

selectChangeLocation('language');
selectChangeLocation('version');
})();
