;(function() {

var select = {}
var selected = {};

function selectChangeLocation(id) {
    select[id] = document.getElementById(id);
    selected[id] = select[id].options[select[id].selectedIndex]
    select[id].addEventListener('change', function(event) {
        window.location = window.location.href.replace(
            selected[id].value, event.target.value).split('?')[0];
    });
}

selectChangeLocation('language');
selectChangeLocation('version');

function queryParam(param) {
    match = RegExp(param + '=([a-z0-9\-\.]+)').exec(location.search)
    return match && match[1]
}

var fromLang = queryParam('from-lang');
if (fromLang) {
    var doc_not_found_message = document.getElementById('doc-not-found-message-' + fromLang);
    doc_not_found_message.innerHTML = doc_not_found_message.innerHTML.replace('{version}', selected['version'].text);
    doc_not_found_message.style.display = 'block';

    var latestVersion = queryParam('latest-version');
    if (latestVersion) {
      var latest_version_message = document.getElementById('latest-version-message-' + fromLang);
      latest_version_message.innerHTML = latest_version_message.innerHTML.replace('{version}', latestVersion);
      latest_version_message.style.display = 'block';
    }
}


})();
