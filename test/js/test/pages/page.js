/**
 * Base page object
 * @module Page
 */
'use strict';

class Page {
    constructor() {
    }
    open(path) {
        browser.url(path);
    }
}
module.exports = Page;
