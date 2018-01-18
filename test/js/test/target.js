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

// Test cases lifted from Github #21, #24, #30, #33, #35, #37, #42, #43
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
	test.it('should show Midline and endline targets form after Create targets clicked');
	test.it('should clear Midline and endline targets form after Remove all targets are clicked');
	test.it('should show Midline and endline target table');
	test.it('should require values in Midline target field');
	test.it('should require value in Endline target field');
	test.it('should not permit removing only midline or endline targets');
	test.it('should require removing both targets to remove either one');
	test.it('should permit only numeric values for LoP target');
	test.it('should reject non-numeric values for LoP target');
	test.it('should permit existing non-numeric values for LoP target');
	test.it('should require numeric value if non-numeric field is edited');
	test.it('should require the Life of Program (LoP) target');
	test.it('should require completed required target frequency sub-options before enabling Create targets button');
	test.it('should require name of first event when Target frequency is Event');
	test.it('should require providing number of events when Target frequency is Event');
	test.it('should permit adding up to 12 events');
	test.it('should inform user that only 12 events can be created at once');
	test.it('should create table of event-based targets when Create targets button is clicked');
	test.it('should have autocompletion in the Target frequency selection menu');
	test.it('should require selecting Target frequency');
	test.it('should have 8 options on Target frequency selection menu');
	test.it('should have Life of Program (LoP) target only');
	test.it('should have Midline and Endline target');
	test.it('should require value for Annual target when freq is annual');
	test.it('should require Semi-annual target when freq is semi-annual');
	test.it('should require Tri-annual target when freq is tri-annual');
	test.it('should require Quarterly target when freq is quarterly');
	test.it('should require Monthly target when freq is monthly');
	test.it('should require First target period when periodic indicators');
	test.it('should require Number of target periods when periodic indicators')
	test.it('should require only numeric value for Number of target periods');
	test.it('should default Number of target periods to 1');
	test.it('should prompt user if required field is empty');
	test.it('should require First event name if freq is Event');
	test.it('should require Number of events if freq is Event');
	test.it('should require only numeric value for Number of events');
	test.it('should default Number of events to 1');
	test.it('should limit Number of events between 1 and 12');
	test.it('should not permit edting saved targets except for LoP');
	test.it('should disable the Target frequency menu after changes saved');
	test.it('should enable only Remove all targets after targets saved');
	test.it('should test #25');
});
