/* This Source Code Form is subject to the terms of the Mozilla Public
* License, v. 2.0. If a copy of the MPL was not distributed with this
* file, You can obtain one at http://mozilla.org/MPL/2.0/. */

;(function() {
    'use strict';

    // Add class to reflect javascript availability for CSS
    document.documentElement.className = document.documentElement.className.replace(/\bno-js\b/, 'js');

    // A container for text strings to use in scripts
    var strings = document.getElementById('strings');

    // override clicks on the hamburger menu icon
    var menu_icon = document.querySelector('.menu-icon');
    if (menu_icon) {
        menu_icon.onclick = function() {
            return false;
        };
    }

    // for the language and version switcher
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

    // get the next sibling element
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

    // get the previous sibling element
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

    // find the last sibling element in a matched set
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

    // determine if the selected answer is correct
    // (tip: you can totally cheat by viewing source!)
    function isCorrect(answer) {
        var input = answer.querySelector('input');
        if (answer.matches('.correct')) {
            return input.checked;
        }
        return !input.checked;
    }

    // show the appropriate feedback for the selected answer
    function showFeedback(submitElement) {
        var correct = 0, incorrect = 0;
        var question = previousElementSiblingMatching(submitElement.parentElement, '.quiz-question');
        var correctFeedback = nextElementSiblingMatching(question, '.feedback-correct');
        var incorrectFeedback = nextElementSiblingMatching(question, '.feedback-incorrect');
        var partlyFeedback = nextElementSiblingMatching(question, '.feedback-partial');
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

    // add a submit button after the last answer
    function addSubmitToEachLastAnswer() {
        var answer = document.querySelector('.quiz-answer');

        while (answer) {
            answer = lastContiguousAnswer(answer);
            if (answer) {
                var submit = document.createElement('p');
                submit.classList.add('quiz-submit');
                var submitBtn = submit.appendChild(document.createElement('button'));
                submitBtn.appendChild(document.createTextNode(strings.dataset.submit));
                answer.parentNode.insertBefore(submit, answer.nextSibling);
                submitBtn.addEventListener('click', function(event) {
                    showFeedback(event.target);
                });
            }
        }
    }
    addSubmitToEachLastAnswer();
})();
