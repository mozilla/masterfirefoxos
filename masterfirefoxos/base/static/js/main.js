;(function() {

function languageChange(from){
    return function(event) {
	console.log('changing language from ' + from + ' to ' + event.target.value);
	window.location = window.location.href.replace(
	    from, event.target.value) + '?fromLang=' + from; // TODO: handle existing params
    }
}

function versionChange(from){
    return function(event) {
	console.log('changing version from ' + from + ' to ' + event.target.value);
	window.location = window.location.href.replace(
	    from, event.target.value) + '?fromVersion=' + from; // TODO: handle existing params
    }
}

var languageSelect = document.getElementById('language')
var selectedLanguage = languageSelect.options[languageSelect.selectedIndex].value
languageSelect.addEventListener('change', languageChange(selectedLanguage));

var versionSelect = document.getElementById('version')
var selectedVersion = versionSelect.options[versionSelect.selectedIndex].value
versionSelect.addEventListener('change', versionChange(selectedVersion));

})();
