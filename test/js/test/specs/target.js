var assert = require('chai').assert;
var LoginPage = require('../pages/login.page.js');
var IndPage = require('../pages/indicators.page.js');
var util = require('../lib/testutil.js');
    
describe('Indicators Targets', function() {
  it('should require unauthenticated users to login', function() {
    let parms = util.readConfig();
    LoginPage.open(parms.baseurl);
    LoginPage.setUserName(parms.username);
    LoginPage.setPassword(parms.password);
    LoginPage.clickLoginButton();
  });
}); // end indicators targets

describe('Create new indicator dialog', function() {
  it('should require selecting program from the "Program" dropdown');
  it('should accept no value for "Sector"');
  it('should accept any value for "Sector"');
  it('should require "Program Objective"');
  it('should require "Country Strategic Objection"');
  it('should have a "Save changes" button');
  it('should have a "Reset" button');
  it('should have a "Help" button');
  it('should open the "Targets" tab when clicked');	
  it('should clear form when "Reset" button clicked');
  it('should save data when "Save changes" button clicked');
}); // end new indicator dialog

// Test cases from Github #21, #24, #25, #30, #33, #35, #37, #42, #43
describe('Targets tab', function() {
  it('should require "Unit of measure"');
  it('should require "Life of Program (LoP) target" value');
  it('should not require Rationale for target');
  it('should require Baseline for target unless "Not applicable" checked');
  it('should clear form when Reset button clicked');
  it('should save data when Save changes button clicked');

  describe('Target frequency', function() {
    it('should be a required selection');
    it('should require selecting Target frequency');
    it('should have 8 options on Target frequency selection menu');

    let unit = 'Buckets';
    let name = '===> Delete Me! <===';
    let lopTarget = 20;
    let baseline = false;
    describe('"Life of Program (LoP) only" target frequency', function() {
      IndPage.createNewProgramIndicator(unit, name, lopTarget, baseline, 'lopOnly');
      it('should permit only numeric values for LoP target');
      it('should reject non-numeric values for LoP target');
      it('should permit non-numeric values only in legacy data for LoP target');
      it('should require numeric value for LoP target if non-numeric field in legacy data is modified');
    });

    describe('"Midline and endline" target frequency', function() {
      IndPage.createNewProgramIndicator(unit, name, lopTarget, baseline=false, 'midEndLine');
      it('should show Midline and endline targets form after clicking Create targets button');
      it('should clear Midline and endline targets form after clicking Remove all targets button');
      it('should show Midline and endline target table');
      it('should require value in Midline target field');
      it('should require value in Endline target field');
      it('should not permit removing only midline or endline targets');
      it('should require removing both targets to remove either one');
      it('should require Midline target if freq is midline and endline')
      it('should require Endline target if freq is midline and endline')
    });

    describe('"Annual" target frequency', function() {
      IndPage.createNewProgramIndicator(unit, name, lopTarget, baseline=false, 'Annual');
      it('should require value for Annual target if freq is annual');
    });

    describe('"Semi-annual" target frequency', function() {
      IndPage.createNewProgramIndicator(unit, name, lopTarget, baseline=false, 'Semi-annual');
      it('should require Semi-annual target if freq is semi-annual');
    });

    describe('"Tri-annual" target frequency', function() {
      IndPage.createNewProgramIndicator(unit, name, lopTarget, baseline=false, 'Tri-annual');
      it('should require Tri-annual target if freq is tri-annual');
    });

    describe('"Quarterly" target frequency', function() {
      IndPage.createNewProgramIndicator(unit, name, lopTarget, baseline=false, 'Quarterly');
      it('should require Quarterly target if freq is quarterly');
    });

    describe('"Monthly" target frequency', function() {
      IndPage.createNewProgramIndicator(unit, name, lopTarget, baseline=false, 'Monthly');
      it('should require Monthly target if freq is monthly');
    });

    describe('"Event" target frequency', function() {
      IndPage.createNewProgramIndicator(unit, name, lopTarget, baseline=false, frequency);
      it('should require name of first event if Target frequency is Event');
      it('should require number of events if Target frequency is Event');
      it('should require at least one event if Target frequency is Event');
      it('should permit adding up to 12 events if Target frequency is Event');
      it('should inform user that only 12 events can be created at once');
      it('should create table of event-based targets when Create targets button is clicked');
      it('should require First event name if freq is Event');
      it('should require Number of events if freq is Event');
      it('should require only numeric value for Number of events');
      it('should default Number of events to 1');
      it('should limit Number of events between 1 and 12');
    });
  });

  it('should have Create targets button');
  it('should have Remove all targets button');
  it('should require completed required target frequency sub-options before enabling Create targets button');
  it('should enable type-to-search in the Target frequency selection menu');

  it('should require First target period if using periodic indicators');
  it('should require Number of target periods if using periodic indicators')
  it('should require only numeric value for Number of target periods');
  it('should default Number of target periods to 1');
  it('should prompt user if any required field is empty');
  it('should not permit edting saved targets except for LoP');
  it('should disable Target frequency menu after changes saved');
  it('should enable only Remove all targets after target saved');
  it('should not see Target frequency sub-options after target saved');
  it('should require only numeric values for target values');
  it('should require all target fields be filled or save nothing');
  it('should update target sums when targets entered and saved');
}); // end test cases from GitHub issues
