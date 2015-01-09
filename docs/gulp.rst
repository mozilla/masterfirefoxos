.. This Source Code Form is subject to the terms of the Mozilla Public
.. License, v. 2.0. If a copy of the MPL was not distributed with this
.. file, You can obtain one at http://mozilla.org/MPL/2.0/.

.. _gulp:

===========
Using Gulp
===========

Introduction
------------
Gulp is used to compile the stylus files into CSS.


Pre-Requisites
--------------

* `Node <http://nodejs.org/>`_
* `NPM <https://npmjs.org/>`_


Installation
------------
If not installed already, install gulp globally. You may need to run this command using sudo::

    npm install -g gulp

Install the project specific node modules::

    npm install


Tasks
-----

Compile all stylus files to css::

    gulp compress

Watch stylus directory, compile to css on change::

    gulp watch
