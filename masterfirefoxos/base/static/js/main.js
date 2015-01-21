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

function languageName(lang) {
    for (var i = 0; i < select['language'].options.length; i++) {
        var option = select['language'].options.item(i)
        if (lang === option.value) {
            return option.text
        }
    }
    return 'your selected language'
}

var fromLang = queryParam('from-lang');
if (fromLang) {
    var language = languageName(fromLang)
    var text = 'Documentation for Firefox OS ' + selected['version'].text +
        ' is not yet available in ' + language +
        ', so we redirected you to the English version.'

    var latestVersion = queryParam('latest-version');
    if (latestVersion) {
        text += ' The latest version available in ' + language + ' is ' +
            latestVersion.replace('-', '.');
    }
    document.getElementById('redirected-from-lang').appendChild(
        document.createTextNode(text));
}
})();
