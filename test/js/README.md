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
1. Install [NodeJS](https://nodjs.org) so you can use (the 
[Node Package Manager](https://www.npmjos.com)) to install other 
JavaScript packages.
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

  TolaActivity Test Suite
    Login Screen
      ✓ should require user to authenticate
      ✓ should have a login field (47ms)
      ✓ should have a password field
      ✓ should have a Log In button (2294ms)
      - should not permit access if username is invalid
      - should not permit access if password is invalid
    Tola-Activity Dashboard
      ✓ should have a page title
      ✓ should have a TolaActivity link (923ms)
      ✓ should have a Workflow link (90ms)
      ✓ should have a Form Library link (39ms)
      ✓ should have a Reports link
      - should have a Profile link
      ✓ should have a Bookmarks link
      ✓ should have a Country Dashboard link
      ✓ should have a Filter by Program link
      Indicator Evidence panel
        - should have an Indicator evidence table
      Strategic Objectives panel
        - should have a Strategic Objectives table
      Sites panel
        - should have a Site map
        - should show map of country selected in Country Dashboard dropdown
        - should be able to zoom in on the map
        - should be able to zoom out on the map
        - should display data points on the Sites map
      Program Projects by Status panel
        - should have a project status chart
      Indicators performance panel
        - should have a KPI status chart
    Program Indicators page
      - should highlight indicators with no evidence
      - should increase indicator count for a given program after adding a new indicator
      - should decrease indicator count for a given program after deleting an indicator
      - should be able to toggle table expansion by clicking the Indicators button
      - should disable the Indicators button if a given program has no indicators
      - should be able to sort table by clicking a column header
      - should be able to view an indicator by clicking its name in the Indicator Name column
      - should not be able to edit an indicator by clicking its name in the Indicator Name column
      - should be able to edit an indicator by clicking the Edit button on its table row
      - should be able to view indicator evidence by clicking the indicator's Data button
      - should have data evidence count button match evidence count in the evidence table
      - should increase data evidence count when evidence added from a program indicator
      - should decrease data evidence count when evidence deleted from a program indicator
      - should be able to delete an indicator by clicking its Delete button
      - should reduce the indicator count for each indicator deleted
      - should have a Programs dropdown
      - should have an Indicators dropdown
      - should have an Indicator Type dropdown
      Programs dropdown
        - should have at least one entry
        - should default to showing all programs
        - should be able to select a program and see only the corresponding Indicators
        - should be able to select a program and see only the corresponding Indicator Types
      Indicators dropdown
        - should default to showing all Indicators for a given program
        - should be able to filter the resultset by Indicator
        - should only show programs that use a selected Indicator
      Indicator Type dropdown
        - should default to showing all Indicator Types for a given program
        - should be able to filter the resultset by Indicator Type
        - should only show programs that use a selected Indicator Type
      Program Indicators list
        - should open the Create an Indicator form when New Indicator button is clicked
        - should open the Grid/Print Report page when button is clicked
        - should highlight invalid data
        - should return to previous screen if Cancel button clicked
        - should clear form when Clear button clicked
        - should close the delete dialog by pressing the Esc key
        - should have a Cancel button that returns to the previous screen
        - should identify required fields as such
        - should not permit read-only fields to be edited
        - should have a Grid/Print Report button
        - should open a report page when the Grid/Print Report button is clicked
        Create an Indicator form
          - should show context-sensitve help by clicking Form Help/Guidance button
          - should have an Indicator Service Templates dropdown
          - should have a Custom entry in the Indicator Service Templates dropdown
          - should have a Service Indicator dropdown
          - should have a Country dropdown
          - should have a Program dropdown
          - should have a Save button
          - should validate input data after clicking Save button and before committing it
          - should not save unvalidated input data
          - should highlight invalid input data
          - should save data after validating it
          - should open Indicator detail form after clicking Save button
          - should have a Cancel button
          - should reset and close form when Cancel button clicked
          - should return to previous screen when Cancel button clicked
          - should have a Reset button to reset form
          - should have a Summary tab
          - should have a Performance tab
          - should hnve a Targets tab
          - should have a Data Acquisition tab
          - should have a Analysis and Reporting tab
          - should have an Approval tab
          - should have a Help link
          - should have a Save Changes button
          - should have a Reset button
          - should have a Cancel button
          - should trigger cancel action by pressing Escape key
          - should validate input data after clicking Save Changes button
          - should validate input data before committing it
          - should restore form to pre-edit state when Reset button is clicked
          Indicator creation detail form
            - should confirm indicator created
            Summary tab
              - should have Program field matching input data
            Performance tab
              - should have a Performance tab
            Targets tab
              - should have a Targets tab
            Data Acquisition tab
              - should have a Data Acquisition tab
            Analysis and Reporting tab
              - should have an Analysis and Reporting tab
            Approval tab
              - should have an Approval tab
        Grid/Print Report page
          - should have an Export All button
          - should export all report entries when Export All button is clicked
        Indicator evidence dropdown
          - should toggle indicator's evidence dropdown by clicking its Data button
          - should have the same row count as evidence count on Data button
          - should be able to edit evidence line item by clicking its Edit button
          - should be able to edit evidence line item by clicking its Indicator Name
          - should open Collected Data form when editing evidence line item
          - should be able to delete evidence line item by clicking its Delete button
          - should be able to add evidence line item by clicking the New Data button
          - should open blank Collected Data form when the New Data button is clicked
        Collected Data form
          - should require required fields
          - should not require optional fields
          - should have a Save button
          - should validate input data after Save button clicked
          - should validate input data before committing
          - should not save invalid input data
          - should highlight invalid input data
          - should have a Reset button
          - should clear the form by clicking the Reset button
          - should restore the form defaults by clicking the Reset button
          - should pull data from Tola Tables by clicking the Import Evidence From Tola Tables link
          - should open the Indicator edit form by clicking the Add a Disaggregation link
          - should only accept numerica values in the disaggregations Actuals fields
          - should have a cancel button
          - should be able to close the firm by clicking the Cancel button


  12 passing (4s)
  113 pending
```
1. Rejoice!

