# Using Selenium WebDriver to Test the TolaActivity UI

This document describes how to set up your system to test TolaActivity
front-end code. The tools of choice are:

* Selenium WebDriver for browser automation
* Selenium Server for remote browsers (think Saucelabs, BrowserStack,
  or TestBot)
* WebdriverIO, a test automation framework for NodeJS with support
  for synchronous or asynchronous JavaScript
* MochaJS test framework with assorted plugins, particularly the Chai
  JS assertion library
* Chrome and/or Firefox browsers

If you're reading this, you've already probably cloned the repo. If you
haven't, do that, then come back here. Commands listed in this document
assume you're working from the testing directory, `test/js` in the
TolaActivity repo, unless noted otherwise.

## Install Things
First, download and install all the bits you'll need. These include
NodeJS, Firefox, Chrome, Selenium, Mocha, and Chai. If you are already
using NPM, you can use it to install mocha and chai, but do not use
the NPM-packaged Chrome or Firefox webdrivers because they might not
be current.

1. Install the latest versions of the
[Chrome](https://www.google.com/chrome/browser) and
[Firefox](https://www.mozilla.org/download) browsers.
1. Download and install Chrome's Selenium browser driver,
[ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver).
Place it anywhere in your system $PATH. You may also keep it in
the testing directory of your local repo because it is gitignored.
1. Download and install Firefox's Selenium browser driver,
[geckodriver](https://github.com/mozilla/geckodriver/releases).
Place it anywhere in your system $PATH. You can also keep it in
the testing directory of your local repo because it is gitignored.
1. Download [Selenium Server](https://goo.gl/hvDPsK) and place it
the testing directory.
1. Install [NodeJS](https://nodjs.org) so you can use the
[Node Package Manager](https://www.npmjos.com), `npm`,  to install
other JavaScript packages.
1. Finally, use `npm` to install all of the JavaScript language 
bindings for Selenium, the Mocha test framework, the Chai plugin for
Mocha, and WebDriverIO, and all of the other assorted dependencies
bits:

```
$ npm install 
[...]
```

## Validate the Installation
1. Make a copy the config-example.json file in the testing directory
   of the TolaActivity repo:

```
$ cd test/js
$ cp config-example.json config.json
```

Edit `config.json` and change the `username`, `password`, `baseurl`,
and `browser` values to suit your taste, taste. In particular:
* `username` and `password` correspond to your MercyCorps SSO login
* `baseurl` points to the home page of the TolaActivity instance
  you are testing
1. Start the Seleniuim server:

```
$ cd test/js
$ java -jar -Dwebdriver.firefox.driver=./geckodriver selenium-server-standalone-3.8.1.jar &> selenium-server.log &
```

1. Execute the test suite:

```
$ cd test/js
$ ./node_modules/.bin/wdio

------------------------------------------------------------------
[chrome #0-0] Session ID: db980c3deae94de17354e7000ee25288
[chrome #0-0] Spec: /Users/kwall/repos/TolaActivity/test/js/test/specs/dashboard.js
[chrome #0-0] Running: chrome
[chrome #0-0]
[chrome #0-0] TolaActivity Dashboard
[chrome #0-0]   ✓ should require unauthenticated users to login
[chrome #0-0]   ✓ should have a page header
[chrome #0-0]   ✓ should have a TolaActivity link

    [...output deleted...]

==================================================================
Number of specs: 6


35 passing (42.80s)
164 skipped
```

1. To run the tests in a single file, specify `--spec path/to/file`.
   For example, to run only the dashboard tests, the command would be

```
$ ./node_modules/.bin/wdio --spec test/specs/dashboard.js
```

## Helpful development practices

If you are a developer, this section is for you. It offers some suggestions
for simple coding conventions that can make the job of testing your GUI code
much, much simpler.

* First and foremost, the single best practice that helps QA testing
  the most is to **use either the _id_ or _name_ attribute on all UI
  elements which require, which _might_ require, or which you are
  even _thinking_ about requiring for user interaction.** These attributes
  make it easier to write tests quickly because thee have to be unique
  per-page, so tests can rely on being able to access the page elements
  they need. They also make element queries fast, because such lookups
  are Selenium's happy path.

  Semantic markup is arguably more correct, too, but the interest here
  is to create code and tests that are easy to maintain, not demonstrate
  adherence to standards. The key point is that using _id_ or _name_
  reduces Selenium's code fragility several orders of magnitude. The
  people who come after us will thank us for using this small bit of
  semantic markup.

* Similarly, it is helpful for each page to have its own unique
  title. Again, this makes programmatic access to page elements much
  less complicated and reduces verifying that we've loaded the right
  page to a single short, fast expression. This is less impactful
  than using _id_ or _name_ attributes consistently, so if you can
  only do one of these, use _id_ or _name_ attributes consistently.
