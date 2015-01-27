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


function nextElementSiblingMatching(element, selector) {
    while (element && element.nextElementSibling &&
           !element.nextElementSibling.matches(selector)) {
        element = element.nextElementSibling;
    }
    if (element && element.nextElementSibling &&
            element.nextElementSibling.matches(selector)) {
        return element.nextElementSibling;
    }
}

function previousElementSiblingMatching(element, selector) {
    while (element && element.previousElementSibling &&
           !element.previousElementSibling.matches(selector)) {
        element = element.previousElementSibling;
    }
    if (element && element.previousElementSibling &&
            element.previousElementSibling.matches(selector)) {
        return element.previousElementSibling;
    }
}

function lastContiguousElementSiblingMatching(element, selector) {
    while (element && element.nextElementSibling &&
           element.nextElementSibling.matches(selector)) {
        element = element.nextElementSibling;
    }
    if (element && element.matches(selector)) {
        return element;
    }
}

function lastContiguousAnswer(element) {
    return lastContiguousElementSiblingMatching(
        nextElementSiblingMatching(element, '.quiz-answer'), '.quiz-answer');
}

function isCorrect(answer) {
    var input = answer.children[0]; // TODO: better selector
    if (answer.matches('.correct')) {
	return input.checked;
    }
    return !input.checked;
}

function showFeedback(submitElement) {
    var correct = 0, incorrect = 0;
    var question = previousElementSiblingMatching(
        submitElement.parentElement, '.quiz-question');

    var correctFeedback = nextElementSiblingMatching(
	question, '.correct-feedback')
    var incorrectFeedback = nextElementSiblingMatching(
	question, '.incorrect-feedback')
    var partlyFeedback = nextElementSiblingMatching(
	question, '.partly-correct-feedback')
   
    var answer = nextElementSiblingMatching(question, '.quiz-answer');
    while (answer && answer.matches('.quiz-answer')) {
	if (isCorrect(answer)) {
	    correct++;
	} else {
	    incorrect++;
	}
	answer = answer.nextElementSibling;
    }
    if (correct) {
	if (incorrect) {
	    partlyFeedback.style.display = 'block';
	    correctFeedback.style.display = 'none';
	    incorrectFeedback.style.display = 'none';
	} else {
	    correctFeedback.style.display = 'block';
	    incorrectFeedback.style.display = 'none';
	    partlyFeedback.style.display = 'none';
	}
    } else {
	incorrectFeedback.style.display = 'block';
	correctFeedback.style.display = 'none';
	partlyFeedback.style.display = 'none';
    }
}

function addSubmitToEachLastAnswer() {
    var answer = document.querySelector('.quiz-answer');
    while (answer) {
        answer = lastContiguousAnswer(answer);
        if (answer) {
            var submit = answer.appendChild(document.createElement('div'));
            submit.appendChild(document.createTextNode('Submit'));
            submit.classList.add('quiz-submit');
            submit.addEventListener('click', function(event) {
                showFeedback(event.target);
            });
        }
    }
}

addSubmitToEachLastAnswer();
})();
