.. This Source Code Form is subject to the terms of the Mozilla Public
.. License, v. 2.0. If a copy of the MPL was not distributed with this
.. file, You can obtain one at http://mozilla.org/MPL/2.0/.


===============
Quiz
===============

A quiz is a collection of questions where each question consists of the following:

1. A question.
2. Text to display when the answer is wrong or right.
3. A list of possible answers where one or more is correct.


To create a question:

1. Select **Quiz Question** from the dropdown.
2. Populate the 4 rich text areas:
    1. Question Text
    2. Correct Answer Text
    3. Partially Correct Answer Text
    4. Incorrect Answer Text
3. Select **Quiz Answer** from the dropdown.
    1. Populate the copy for the answer.
    2. Check **Correct** if this is a correct answer.

.. Note::
    You repeat the above for each question and answer set. The CMS assumes all answers are attached
    to a question until another question is reached. This means the order of items in the CMS is
    used to determine which answers go with which questions.
