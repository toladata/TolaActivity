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
for Selenium, the Mocha test framework, and the Chai plugin for
Mocha:

```
$ npm install selenium-webdriver mocha chai
[...]
```

## Validate the Installation
1. Edit the config.json file in the top-level of the TolaActivity. Change
the `username`, `password`, `baseurl`, and `browser` values to suit your
taste. In particular,
    - `username` and `password` correspond to your MercyCorps SSO login
    - `baseurl` points to the home page of the TolaActivity instance
    you are testing
    - `browser_name` sets the SUT, and should be either `chrome` or
    `firefox`.
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
    ✓ should have a Filter by Program link (249ms)
    ✓ should have a Workflow dropdown (245ms)
    ✓ should have a Form Library dropdown (468ms)
    ✓ should have a Reports link (218ms)
    ✓ should have a Profile link (242ms)
    ✓ should have a Bookmarks link (237ms)
    Indicator Evidence panel
      - should be present on dashboard
    Strategic Objectives panel
      - should be present on dashboard
    Sites panel
      - should be present on dashboard
      - should show map of country selected in Country Dashboard dropdown
      - should be able to zoom in on the map
      - should be able to zoom out on the map
      - should display data points on the Sites map
    Program Projects by Status panel
      - should be present on dashboard
      - should have a project status chart
    Indicators performance panel
      - should be present on dashboard
      - should have a KPI status chart

  TolaActivity Indicators Page
    ✓ should require login authentiction (2796ms)
    ✓ should exist (5454ms)
    - should highlight PIs with no evidence
    - should disable Indicators button if program has no indicators
    - should be able to sort table by clicking a column header
    Programs dropdown
      ✓ should be present on page (232ms)
      - should have at least one entry
      - should default to showing all programs
      - should be able to filter PIs by Program
      - should be able to filter Programs by PI
      - should have same item count as Programs table
      - should have same items as Programs table
    Indicators dropdown
      ✓ should be present on page (465ms)
      - should have at least one entry
      - should default to showing all PIs for a program
      - should be able to select any/all list items
    Indicator Type dropdown
      ✓ should be present on page (217ms)
      - should have at least one entry
      - should default to showing all Indicator Types for a program
      - should be able to filter the resultset by Indicator Type

  TolaActivity invalid password login
    ✓ should have a Username field
    ✓ should have a Password field
    ✓ should have a Log In button (308ms)
    ✓ should deny access if password is invalid

  TolaActivity invalid username login
    ✓ should have a Username field
    ✓ should have a Password field
    ✓ should have a Log In button (294ms)
    ✓ should deny access if username is invalid

  TolaActivity Login screen
    ✓ should require user to authenticate
    ✓ should have a login field
    ✓ should have a password field
    ✓ should have a Log In button (2957ms)

  Indicators Targets
    - should open to Summary tab
    - should be able to select Midline and endline option
    - should open Create new indicator dialog when New Indicator button is clicked
    - should save a record and open the Indicator edit page
    - should clear form when Reset button clicked
    - should save data when Save changes screen clicked

  Create new indicator dialog
    - should require selecting program from the Program dropdown
    - should accept no value for Sector
    - should accept any value for Sector
    - should require Program Objective
    - should require Country Strategic Objection
    - should have a Save changes button
    - should have a Reset button
    - should have a Help button
    - should open the Targets tab when clicked
    - should clear form when Reset button clicked
    - should save data when Save changes screen clicked

  Targets tab
    - should require Unit of measure
    - should require Life of Program (LoP) target
    - should require Rationale for target
    - should require Baseline for target
    - should require Target frequency
    - should clear form when Reset button clicked
    - should save data when Save changes button clicked
    - should have Create targets button
    - should have Remove all targets button
    - should show Midline and endline targets form after Create targets clicked
    - should clear Midline and endline targets form after Remove all targets are clicked
    - should show Midline and endline target table
    - should require values in Midline target field
    - should require value in Endline target field
    - should not permit removing only midline or endline targets
    - should require removing both targets to remove either one
    - should permit only numeric values for LoP target
    - should reject non-numeric values for LoP target
    - should permit existing non-numeric values for LoP target
    - should require numeric value if non-numeric field is edited
    - should require the Life of Program (LoP) target
    - should require completed required target frequency sub-options before enabling Create targets button
    - should require name of first event when Target frequency is Event
    - should require providing number of events when Target frequency is Event
    - should permit adding up to 12 events
    - should inform user that only 12 events can be created at once
    - should create table of event-based targets when Create targets button is clicked
    - should have autocompletion in the Target frequency selection menu
    - should require selecting Target frequency
    - should have 8 options on Target frequency selection menu
    - should have Life of Program (LoP) target only
    - should have Midline and Endline target
    - should require value for Annual target when freq is annual
    - should require Semi-annual target when freq is semi-annual
    - should require Tri-annual target when freq is tri-annual
    - should require Quarterly target when freq is quarterly
    - should require Monthly target when freq is monthly
    - should require First target period when periodic indicators
    - should require Number of target periods when periodic indicators
    - should require only numeric value for Number of target periods
    - should default Number of target periods to 1
    - should prompt user if required field is empty
    - should require First event name if freq is Event
    - should require Number of events if freq is Event
    - should require only numeric value for Number of events
    - should default Number of events to 1
    - should limit Number of events between 1 and 12
    - should not permit edting saved targets except for LoP
    - should disable the Target frequency menu after changes saved
    - should enable only Remove all targets after targets saved
    - should test #25


  28 passing (27s)
  94 pending
```
1. Rejoice!

