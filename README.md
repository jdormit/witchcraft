# Witchcraft for Firefox

![Witchcraft](docs/title.png)

Think Greasemonkey for developers.

This is a Firefox fork of the [original Witchcraft](https://github.com/luciopaiva/witchcraft) Chrome extension. It removes Google Analytics and uses [native messaging](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/Native_messaging) rather than a local web server to load userscript files (this latter change was made because Firefox's stricter CSP disallows loading scripts over `http://`, even from localhost).

This fork won't work on Windows.

Witchcraft is a Firefox extension for loading custom Javascript and CSS directly from a folder in your file system, injecting them into pages that match their files names.

It works by matching every page domain against script file names available in the scripts folder. For instance, if one navigates to `www.google.com`, Witchcraft will try to load and run `google.com.js` and `google.com.css`.

For installation instructions for this fork, see below. For more information on how to use Witchcraft, head to Witchcraft's [home page](//luciopaiva.com/witchcraft).

## Installation
Witchcraft consists of two parts: the extension itself and the native host, used to load userscripts from the local filesystem.

To install the extension, first download the latest `.xpi` file from the [releases page](https://github.com/jdormit/witchcraft/releases). Open the Firefox addons page (`about:addons`), click on the little gear icon and select "Install Add-on from file". When prompted, select the `.xpi` file you downloaded and click through to install it.

To install the native host (a simple Python script), clone this repository and run the `native-host/install.py` script. This will install the native host manifest to the [appropriate directory](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/Native_manifests#manifest_location).

At this point you should be able to start adding scripts to the userscript directory (default: `~/witchcraft-scripts`.

## Development

Node.js is required, but just to run tests. I also use `nvm` to manage Node.js versions, but that's not required (just make sure your Node.js version is similar to the one `.nvmrc` currently points to). To install test dependencies:

    cd <project-folder>
    nvm install
    npm install

Then you're ready to run tests:

    npm test

## Credits
This is a fork of the [Google Chrome Witchcraft extension](https://github.com/luciopaiva/witchcraft) by [luciopaiva](//github.com/luciopaiva).

The original Witchcraft is a rendition of [defunkt](//github.com/defunkt)'s original extension, [dotjs](//github.com/defunkt/dotjs).

Thanks [arimus](//github.com/arimus) for the idea of using Web Server for Chrome.

The little witch and the witch hat icons were provided by [Freepik](//www.flaticon.com/authors/freepik).
