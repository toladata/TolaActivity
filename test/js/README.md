# Using MochaJS and Selenium WebDriver to Test the TolaActivity UI

This document describes how to set up your system to test TolaActivity
using the Selenium WebDriver, Javascript, the MochaJS test framework,
the ChaiJS plugin for MochaJS, and the Chrome and/or Firefox browsers.

## Install Things
First, download and install all the bits you'll need. These include
NodeJS, Firefox, Chrome, Mocha, and Chai. If you are already using
NPM, you can use it to install mocha and chai, but do not use the
NPM-packaged Chrome or Firefox webdrivers because they might not be
current.

1. Install the latest versions of the
[Chrome](ttps://www.google.com/chrome/browser/) and
[Firefox](https://www.mozilla.org/download) browsers.
1. Download [Selenium language
bindings](http://www.seleniumhq.org/download/) for the language(s)
you want to use. We're interested in the JavaScript bindings in
this document; there are also bindings for Python, Java, Ruby, and C#.

1. Download and install Chrome's Selenium browser driver,
[ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver).
Place it anywhere in your system $PATH. You can also keep it in
the top-level of your local repo because it is gitignored.
1. Download and install Firefox's Selenium browser driver,
[geckodriver](https://github.com/mozilla/geckodriver/releases).
Place it anywhere in your system $PATH. You can also keep it in
the top-level of your local repo because it is gitignored.
1. Install [NodeJS](https://nodjs.org) so you can use the
[Node Package Manager](https://www.npmjos.com), or _npm_ to install
other JavaScript packages.
1. Finally, use `npm` to install the JavaScript language bindings
for Selenium, the Mocha test framework, the Chai plugin for
Mocha, and WebDriverIO:

```
$ npm install selenium-webdriver mocha chai webdriverio
[...]
```

## Validate the Installation
1. Edit the config.json file in the top-level of the TolaActivity repo.
Change the `username`, `password`, `baseurl`, and `browser` values to
suit your taste, taste. In particular,
    - `username` and `password` correspond to your MercyCorps SSO login
    - `baseurl` points to the home page of the TolaActivity instance
    you are testing
    - `browser_name` sets the BUT (_b_rowser _u_nder _t_est), and should
    be either `chrome` or `firefox`.
1. From the top of the TolaActivity repo, setup the JS environment for
the test suite:

```
$ cd test/js
$ npm install
[...]
```
1. Execute the test suite. **Note the bare `--`**. They tell `npm`
to ignore the following arguments and pass them through to Mocha,
the underlying test framework.

```
$ npm test -- --no-timeouts

> @ test /home/kwall/Work/TolaActivity/test/js
> mocha "--no-timeouts"

  TolaActivity Dashboard
    ✓ should require login authentication (2886ms)
    ✓ should have home page link (940ms)
    ✓ should have page header
    ✓ should have a TolaActivity link (854ms)
    ✓ should have a Country Dashboard dropdown (218ms)

    [...output deleted...]

    - should default Number of events to 1
    - should limit Number of events between 1 and 12
    - should not permit edting saved targets except for LoP
    - should disable the Target frequency menu after changes saved
    - should enable only Remove all targets after targets saved


  28 passing (27s)
  94 pending
```
1. Rejoice!

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

* Similarly, it would be helpful for each page to have its own unique title.
  Again, this makes programmatic access to page elements much less complicated
  and reduces verifying that we've loaded the right page to a single short,
  fast expression. This is less impactful than using _id_ or _name_ attributes
  consistently, so if you can only do of these, use _id_ or _name_ attributes
  consistently.

* Is there a naming convention at work in the structural and semantic
  markup? I'm curious there is a pattern to the naming that test code
  can exploit.
