;(function() {

function selectChangeLocation(id) {
    var select = document.getElementById(id);
    var selected = select.options[select.selectedIndex].value
    select.addEventListener('change', function(event) {
	window.location = window.location.href.replace(selected, event.target.value);
    });
}

selectChangeLocation('language');
selectChangeLocation('version');
})();
