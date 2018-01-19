'use strict';
var webdriver = require('selenium-webdriver');
var until = require('selenium-webdriver').until;
var test = require('selenium-webdriver/testing');
var assert = require('chai').assert;
var expect = require('chai').should;
var fs = require('fs');
let el;

function readConfig() {
  let data = fs.readFileSync('config.json');
  return JSON.parse(data);
};

async function newTolaSession(parms) {
  driver = new webdriver.Builder()
  .forBrowser(parms.browser)
  .build();
  await driver.get(parms.baseurl);
  el = await driver.getTitle();
  assert.equal(el, 'Mercy Corps Sign-On', el);
}

async function newTolaLogin(parms) {
    el = await driver.findElement({name: 'login'});
    await el.sendKeys(parms.username);

    el = await driver.findElement({name: 'password'});
    await el.sendKeys(parms.password);

    el = await driver.findElement({className: 'inputsub'})
    await el.click();
}

test.describe('Indicators Targets', function() {
	test.it('should open to Summary tab');
	test.it('should be able to select Midline and endline option');
	test.it('should open Create new indicator dialog when New Indicator button is clicked');
  test.it('should save a record and open the Indicator edit page');
	test.it('should clear form when Reset button clicked');
	test.it('should save data when Save changes screen clicked');
});

test.describe('Create new indicator dialog', function() {
	test.it('should require selecting program from the Program dropdown');
	test.it('should accept no value for Sector');
	test.it('should accept any value for Sector');
	test.it('should require Program Objective');
	test.it('should require Country Strategic Objection');
	test.it('should have a Save changes button');
	test.it('should have a Reset button');
	test.it('should have a Help button');
	test.it('should open the Targets tab when clicked');	
	test.it('should clear form when Reset button clicked');
	test.it('should save data when Save changes screen clicked');
});

// Test cases from Github #21, #24, #25, #30, #33, #35, #37, #42, #43
test.describe('Targets tab', function() {
	test.it('should require Unit of measure');
	test.it('should require Life of Program (LoP) target');
	test.it('should require Rationale for target');
	test.it('should require Baseline for target');
	test.it('should require Target frequency');
	test.it('should clear form when Reset button clicked');
	test.it('should save data when Save changes button clicked');
	test.it('should have Create targets button');
	test.it('should have Remove all targets button');
	test.it('should show Midline and endline targets form after clicking Create targets button');
	test.it('should clear Midline and endline targets form after clicking Remove all targets button');
	test.it('should show Midline and endline target table');
	test.it('should require value in Midline target field');
	test.it('should require value in Endline target field');
	test.it('should not permit removing only midline or endline targets');
	test.it('should require removing both targets to remove either one');

	test.it('should permit only numeric values for LoP target');
	test.it('should reject non-numeric values for LoP target');
	test.it('should permit non-numeric values only in legacy data for LoP target');
	test.it('should require numeric value for LoP target if non-numeric field in legacy data is modified');
	test.it('should require the Life of Program (LoP) target');

	test.it('should require completed required target frequency sub-options before enabling Create targets button');
	test.it('should require name of first event if Target frequency is Event');
	test.it('should require number of events if Target frequency is Event');
  test.it('should require at least one event if Target frequency is Event');
	test.it('should permit adding up to 12 events if Target frequency is Event');
	test.it('should inform user that only 12 events can be created at once');
	test.it('should create table of event-based targets when Create targets button is clicked');
	test.it('should enable type-to-search in the Target frequency selection menu');
	test.it('should require selecting Target frequency');
	test.it('should have 8 options on Target frequency selection menu');
	test.it('should have Life of Program (LoP) target only');
	test.it('should require Midline target if freq is midline and endline')
	test.it('should require Endline target if freq is midline and endline')
	test.it('should require value for Annual target if freq is annual');
	test.it('should require Semi-annual target if freq is semi-annual');
	test.it('should require Tri-annual target if freq is tri-annual');
	test.it('should require Quarterly target if freq is quarterly');
	test.it('should require Monthly target if freq is monthly');
	test.it('should require First target period if using periodic indicators');
	test.it('should require Number of target periods if using periodic indicators')
	test.it('should require only numeric value for Number of target periods');
	test.it('should default Number of target periods to 1');
	test.it('should prompt user if any required field is empty');
	test.it('should require First event name if freq is Event');
	test.it('should require Number of events if freq is Event');
	test.it('should require only numeric value for Number of events');
	test.it('should default Number of events to 1');
	test.it('should limit Number of events between 1 and 12');
	test.it('should not permit edting saved targets except for LoP');
	test.it('should disable Target frequency menu after changes saved');
	test.it('should enable only Remove all targets after target saved');
  test.it('should not see Target frequency sub-options after target saved');
  test.it('should require only numeric values for target values');
  test.it('should prompt user to complete form if any required target fields are left empty');
  test.it('should require all target fields be filled or save nothing');
  test.it('should update target sums when targets entered and saved');
});
