# Using Selenium WebDriver to Test the TolaActivity UI

This document describes how to set up your system to test TolaActivity
front-end code. The tools of choice are:

* [Selenium WebDriver](http://www.seleniumhq.org/) for browser automation
* [Chrome](https://www.google.com/chrome/) and/or
  [Firefox](https://www.mozilla.org/firefox/) browsers
* [WebdriverIO](), a test automation framework for NodeJS that supports both
  synchronous and asynchronous JavaScript
* [Selenium Server](http://www.seleniumhq.org/) for remote browsers
  (think Saucelabs, BrowserStack, or TestBot), a WebdriverIO dependency
* [MochaJS test framework](https://mochajs.org/) with assorted plugins,
  particularly the [ChaiJS assertion library](http://chaijs.com/)
* [Allure](http://allure.qatools.ru/), a test reporter

If you're reading this, you've already probably cloned the repo. If you
haven't, do that, then come back here. Commands listed in this document
assume you're working from the testing directory, _test/js_ in the
TolaActivity repo, unless noted otherwise. If you are impatient, start
with the next section, "The Big Green Button<sup>©</sup>: Quickstart
guide for the impatient".  If you want to understand more about how
this thing works, start with the following section, "Manual installation
and testing".

## Runtime configuration files

The framework includes three WebdriverIO, or _WDIO_, runtime configuration
files that control which and/or how many tests get run. These are summary
descriptions; sections describing each option in detail follow.

- **wdio.auto.conf.js** -- Consider this the one-size-fits-all option. It runs
  all of the tests against all of the browsers all of the time. If you feel
  impatient, this is the config for you. Read "For the impatient" to get started.
- **wdio.chrome.conf.js** -- Runs all of the tests in the suite against the
  Chrome browser.
- **wdio.gecko.conf.js** -- RUns all of the tests in the suite against the
  Firefox browser.
- **wdio.headless.conf.js** -- This is an experimental option that runs the test
  framework using Chrome's headless mode. I know, right? I didn't know Chrome _had_
  a headless mode. This option executes all of the tests against the Chrome
  browser.
- **wdio.manual.conf.js** -- Runs all of the tests in the suite agsinst both the
  Chrome and the Firefox browsers.

## The Big Green Button<sup>©</sup>: Quickstart guide for the impatient

![](docs/big_green_button.jpg)

If you just want to run the tests, have a functional development system,
and have `node` and `npm` installed, the following sequence of steps and 
commands will get you going:

```
git clone https://github.com/mercycorps.org/TolaActivity.git
cd TolaActivity/test/js
[edit user config file as described below]
make install
./node_modules/.bin/wdio wdio.auto.conf.js
```

### Create the user config file
Copy the example user config file to _config.json_ (`cp
config-example.json config.json`) and edit _config.json_, changing
_username_, _password_, and _baseurl_ to suit your needs. In particular:

- _username_ and _password_ must correspond to your MercyCorps SSO login
- _baseurl_ points to the home page of the TolaActivity instance you
  are testing
- **Under no circumstances should this suite be run against the production
  TolaActivity server. It will create bad data, result in a lot of work to
  remove, and potentially result in losing known-good, live data.**

The last command, `./node_modules/.bin/wdio`, starts Selenium server,
which is a Java app. As a result, there might be a multi-second pause
while it starts. When web browsers start operating themselves on your
desktop, the tests have started. The last step, `wdio wdio.auto.conf.js`,
starts the WebDriverIO bits, the Selenium server, unconditionally runs
the complete test suite for each configured browser, shows the test
results, and then exits, terminating the server as it goes. The output
should resemble the following, hopefully without the test failures:

```
$ cd test/js
$ ./node_modules/.bin/wdio wdio.auto.conf.js 

․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․F․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․F․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․․

144 passing (396.40s)
140 skipped
2 failing

1) Program Indicators table should toggle table when a PI Indicators button is clicked:
expected true to equal false
running chrome
running firefox
AssertionError: expected true to equal false
    at Context.<anonymous> (/home/kwall/Work/TolaActivity/test/js/test/specs/indicators_table.js:51:14)
        at new Promise (<anonymous>)
            at new F (/home/kwall/Work/TolaActivity/test/js/node_modules/core-js/library/modules/_export.js:35:28)



========= Your concise report ========== 
chrome::undefined:latest
All went well !!
========= Your concise report ========== 
chrome::undefined:latest
All went well !!
[...]
========= Your concise report ========== 
chrome::undefined:latest
Test failed (1): 
Fail : Program Indicators table2 => should toggle table when a PI Indicators button is clicked
AssertionError : expected true to equal false
[...]
========= Your concise report ========== 
firefox::undefined:latest
All went well !!
========= Your concise report ========== 
firefox::undefined:latest
Test failed (1): 
Fail : Program Indicators table2 => should toggle table when a PI Indicators button is clicked
AssertionError : expected true to equal false
[...]
```

## Manual installation and testing

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
The current version (at the time of writing) is 2.34.
1. Download and install Firefox's Selenium browser driver,
[geckodriver](https://github.com/mozilla/geckodriver/releases).
Place it anywhere in your system $PATH. You can also keep it in
the testing directory of your local repo because it is gitignored.
The current version (at the time of writing) is 0.19.1.
1. Download [Selenium Server](https://goo.gl/hvDPsK) and place it
the testing directory. The current version (at the time of writing) is
3.9.1.
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
1. Edit `config.json` and change the _username_, _password_, and _baseurl_
values to suit your needs. In particular:
- _username_ and _password_ correspond to your MercyCorps SSO login
- _baseurl_ points to the home page of the TolaActivity instance you
  are testing
- **Under no circumstances should this suite be run against the production
  TolaActivity server. It will create bad data, result in a lot of work to
  remove, and potentially result in losing known-good, live data.**

```
$ cd test/js
$ cp config-example.json config.json
```

1. Edit `config.json` and change the `username`, `password`, and `baseurl`
values to suit your needs. In particular:
* `username` and `password` correspond to your MercyCorps SSO login
* `baseurl` points to the home page of the TolaActivity instance you
  are testing
1. Start the Seleniuim server (targeting the Firefox browser):

```
$ cd test/js
$ java -jar -Dwebdriver.gecko.driver=./geckodriver selenium-server-standalone-3.9.1.jar &> selenium-server.log &
```

1. Execute the test suite:

```
$ cd test/js
$ ./node_modules/.bin/wdio wdio.firefox.conf.js

------------------------------------------------------------------
[firefox #0-0] Session ID: db980c3deae94de17354e7000ee25288
[firefox #0-0] Spec: /Users/kwall/repos/TolaActivity/test/js/test/specs/dashboard.js
[firefox #0-0] Running: firefox
[firefox #0-0]
[firefox #0-0] TolaActivity Dashboard
[firefox #0-0]   ✓ should require unauthenticated users to login
[firefox #0-0]   ✓ should have a page header
[firefox #0-0]   ✓ should have a TolaActivity link
[...]
==================================================================
Number of specs: 6


72 passing (109.10s)
70 skipped
1 failing

1) Program Indicators table should toggle table when a PI Indicators button is clicked:
expected true to equal false
 running chrome
running firefox
AssertionError: expected true to equal false
    at Context.<anonymous> (/home/kwall/Work/TolaActivity/test/js/test/specs/indicators_table.js:51:14)
        at new Promise (<anonymous>)
            at new F (/home/kwall/Work/TolaActivity/test/js/node_modules/core-js/library/modules/_export    .js:35:28)
95 

```

## Don't want to run everything?
1. To run the tests in a single file, specify `--spec path/to/file`.
   For example, to run only the dashboard tests in auto mode, the command would be

```
$ ./node_modules/.bin/wdio wdio.auto.conf.js --spec test/specs/dashboard.js
```

1. You can also the the `--spec` argument as a crude regex and spec
filenames. For example, to run any test that contains _invalid_ in the
filename, this command would do it:

```
$ ./node_modules/.bin/wdio --spec invalid
```

## Looking for framework documentation?
To produce documentation for the test framework, the API is decorated with
JSDoc decorators, so it will produce JSDoc-compatible documentation from the
code itself. To do so, execute the command `make doc` at the top of the 
testing directory:

```
$ make doc
./node_modules/.bin/jsdoc --verbose \
  --package package.json \
  --recurse \
  --destination doc \
  --readme README.md \
  test/lib test/pages -R README.md
Parsing /home/kwall/Work/TolaActivity/test/js/test/lib/testutil.js ...
Parsing /home/kwall/Work/TolaActivity/test/js/test/pages/indicators.page.js ...
Parsing /home/kwall/Work/TolaActivity/test/js/test/pages/login.page.js ...
Generating output files...
Finished running in 0.15 seconds.
```

The resulting output is best viewed in your browser. To do so, open 
file:///path/to/your/repo/doc/index.html in your web browser. It will
end up looking something like the following image. **NOTE:** This is
_API_ documentation; the tests themselves are self-documenting.

![](doc/tola_test_doc_home.png)

## Helpful development practices

If you are a developer, this section is for you. It offers some suggestions
for simple coding proactices that can make the job of testing your GUI code
much, much simpler.

* First and foremost, the single best practice that helps QA testing
  the most is to **use either the _id_ or _name_ attribute on all UI
  elements which require, which _might_ require, or which you are
  even _thinking_ about requiring for user interaction.** These attributes
  make it easier to write tests quickly because they have to be unique
  per-page, so tests can rely on being able to access the page elements
  they need. They also make element queries fast, because such lookups
  are Selenium's happy path.

  [Semantic markup](https://en.wikipedia.org/wiki/Semantic_HTML) is
  arguably more correct, too, but the interest here is to create code
  and tests that are easy to maintain, not demonstrate adherence to best
  practices. Rather, the point is that using _id_ or _name_ reduces Selenium's
  code fragility several orders of magnitude. The people who come after
  us will thank us for using this small bit of semantic markup.

* Similarly, it is helpful for each page to have its own unique
  title. Again, this makes programmatic access to page elements much
  less complicated and reduces verifying that we've loaded the right
  page to a single short, fast expression. This is less impactful
  than using _id_ or _name_ attributes consistently, so if you can
  only do one of these, use _id_ or _name_ attributes consistently.
