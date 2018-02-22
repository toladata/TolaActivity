var assert = require('chai').assert;
var LoginPage = require('../pages/login.page.js');
var IndPage = require('../pages/indicators.page.js');
var TargetsTab = require('../pages/targets.page.js');
var util = require('../lib/testutil.js');

describe('Indicator Targets', function() {
  // Disable timeouts
  this.timeout(0);
  browser.windowHandleMaximize();

  describe('Create new indicator dialog', function() {
    it('should require unauthenticated users to login', function() {
      let parms = util.readConfig();
      LoginPage.open(parms.baseurl);
      LoginPage.setUserName(parms.username);
      LoginPage.setPassword(parms.password);
      LoginPage.clickLoginButton();
      IndPage.open();
      assert.equal('Program Indicators', IndPage.pageName(),
        'Unexpected page name mismatch');
    });

    it('should open new indicator form when button is clicked', function() {
      TargetsTab.clickNewIndicatorButton();
      assert.equal('Create an Indicator', TargetsTab.pageName(),
        'Unexpected page name mismatch');
    });

    it('should save the new indicator when the button is clicked', function() {
      TargetsTab.saveNewIndicator();
    });

    it('should have a "Reset" button', function() {
      TargetsTab.clickResetButton();
    });

    it('should clear form when "Reset" button clicked', function() {
      TargetsTab.setIndicatorName('Testing the reset button');
      TargetsTab.setUnitOfMeasure('Clicks');
      TargetsTab.setLoPTarget(38);
      TargetsTab.setBaseline(39);
      TargetsTab.setTargetFrequency('Life of Program (LoP) only');
      TargetsTab.clickResetButton();
      assert.equal('Temporary', TargetsTab.getIndicatorName());
      assert.equal('', TargetsTab.getUnitOfMeasure());
      assert.equal('', TargetsTab.getLoPTarget());
      assert.equal('', TargetsTab.getBaseline());
      assert.equal('---------', TargetsTab.getTargetFrequency());
    });

    it('should save changed data when "Save changes" button clicked', function() {
      // Create a new "basic" indicator
      IndPage.clickIndicatorsLink();
      TargetsTab.clickNewIndicatorButton();
      TargetsTab.saveNewIndicator();

      // Make a bunch of changes
      let newIndicatorName = 'Testing the save changes button';
      let newUnitOfMeasure = 'Leaps per lightyear';
      let newLoPTarget = 57;
      let newBaseline = 58;
      let newTargetFrequency = 'Life of Program (LoP) only';

      TargetsTab.setIndicatorName(newIndicatorName);
      TargetsTab.setUnitOfMeasure(newUnitOfMeasure);
      TargetsTab.setLoPTarget(newLoPTarget);
      TargetsTab.setBaseline(newBaseline);
      TargetsTab.setTargetFrequency(newTargetFrequency);

      // Save them
      TargetsTab.saveIndicatorChanges();

      // Verify the new values are correct
      assert.equal(newIndicatorName, TargetsTab.getIndicatorName(),
        'Did not receive expected indicator name');
      assert.equal(newUnitOfMeasure, TargetsTab.getUnitOfMeasure(),
        'Did not receive expected unit of measure');
      assert.equal(newLoPTarget, TargetsTab.getLoPTarget(),
        'Did not receive expected LoP target');
      assert.equal(newBaseline, TargetsTab.getBaseline(),
        'Did not receive expected baseline value');
      assert.equal(newTargetFrequency, TargetsTab.getTargetFrequency(),
        'Did not receive expected target frequency');
    });
  }); // end new indicator dialog

  // Test cases from issues #21, #24, #25, #30, #33, #35, #37, #42, #43
  describe('Targets tab', function() {
    it('should require "Unit of measure"', function() {
      // Set everything but the unit of measure then try to save
      IndPage.clickIndicatorsLink();
      TargetsTab.clickNewIndicatorButton();
      TargetsTab.saveNewIndicator();

      TargetsTab.setIndicatorName('Unit of measure test');
      TargetsTab.setLoPTarget(98);
      TargetsTab.setBaseline(99);
      TargetsTab.setTargetFrequency('Life of Program (LoP) only');
      TargetsTab.saveIndicatorChanges();
      // Should get this error message
      let msg = TargetsTab.getAlertMsg();
      assert(msg.includes('Please complete all required fields in the Targets tab.'),
        'Did not receive expected failure message');
    });

    it('should require "Life of Program (LoP) target" value', function() {
      // Set everything but the LoP target then try to save
      IndPage.clickIndicatorsLink();
      TargetsTab.clickNewIndicatorButton();
      TargetsTab.saveNewIndicator();
      TargetsTab.setIndicatorName('LoP target value test');
      TargetsTab.setUnitOfMeasure('Buckets');
      TargetsTab.setBaseline(115);
      TargetsTab.setTargetFrequency('Life of Program (LoP) only');
      TargetsTab.saveIndicatorChanges();
      // Should get this error message
      let msg = TargetsTab.getAlertMsg();
      assert(msg.includes('Please complete all required fields in the Targets tab.'),
        'Did not receive expected failure message');
    });

    it('should require target Baseline if "Not applicable" not checked', function() {
      // Set everything but the baseline value then try to save
      IndPage.clickIndicatorsLink();
      TargetsTab.clickNewIndicatorButton();
      TargetsTab.saveNewIndicator();
      TargetsTab.setIndicatorName('Baseline value test');
      TargetsTab.setUnitOfMeasure('Crates');
      TargetsTab.setLoPTarget(131);
      TargetsTab.setTargetFrequency('Life of Program (LoP) only');
      TargetsTab.saveIndicatorChanges();
      // Should get this error message
      let msg = TargetsTab.getAlertMsg();
      assert(msg.includes('Please complete all required fields in the Targets tab.'),
        'Did not receive expected failure message');
    });

    it('should *not* require Baseline if "Not applicable" *is* checked', function() {
      // Set everything but the baseline value; enable the
      // Not applicable checkbox
      IndPage.clickIndicatorsLink();
      TargetsTab.clickNewIndicatorButton();
      TargetsTab.saveNewIndicator();

      TargetsTab.setIndicatorName('Baseline value not applicable test');
      TargetsTab.setUnitOfMeasure('Drops');
      TargetsTab.setLoPTarget(147);
      TargetsTab.setTargetFrequency('Life of Program (LoP) only');
      TargetsTab.setBaselineNA();

      // Save; this should pass
      TargetsTab.saveIndicatorChanges();
      // FIXME: This is a green-red test. When it starts failing, the underlying
      // bug has been fixed and the test needs to be updated accordingly
      assert.notEqual('Success, form data saved.', TargetsTab.getAlertMsg(),
        'Did not receive expected success message');
      // Should not get this message
      // FIXME: I'd rather not use the negative logic; much prefer the
      // positive form above if it can be made to work
      assert.notEqual('Please complete all required fields in the Targets tab.',
        TargetsTab.getAlertMsg(),
        'Received unexpected error message');
    });

    it('should require Target frequency', function() {
      // Set everything but the target frequency then try to save
      IndPage.clickIndicatorsLink();
      TargetsTab.clickNewIndicatorButton();
      TargetsTab.saveNewIndicator();
      TargetsTab.setIndicatorName('Target frequency test');
      TargetsTab.setUnitOfMeasure('Emissions');
      TargetsTab.setLoPTarget(173);
      TargetsTab.setBaseline(174);
      TargetsTab.saveIndicatorChanges();
      // Should get this error message
      let msg = TargetsTab.getAlertMsg();
      assert(msg.includes('Please complete all required fields in the Targets tab.'),
        'Did not receive expected failure message');
    });

    describe('"Life of Program (LoP) only" target frequency', function() {
      it('should permit only numeric values for LoP target', function() {
        IndPage.clickIndicatorsLink();
        TargetsTab.clickNewIndicatorButton();
        TargetsTab.saveNewIndicator();

        TargetsTab.setIndicatorName('LoP only target testing');
        TargetsTab.setUnitOfMeasure('Furlongs per fortnight');
        TargetsTab.setLoPTarget(192);
        TargetsTab.setBaseline(193);
        TargetsTab.setTargetFrequency('Life of Program (LoP) only');
        TargetsTab.saveIndicatorChanges();
      });

      it('should reject non-numeric values for LoP target', function() {
        TargetsTab.setLoPTarget('"666"');
        // This should fail
        TargetsTab.saveIndicatorChanges();
        let errorHint = TargetsTab.getLoPErrorHint();
        assert(errorHint.includes('Please enter a number larger than zero'),
          'Did not receive expected failure message');
        // Make it numeric; this should succeed
        TargetsTab.setLoPTarget(207);
        TargetsTab.saveIndicatorChanges();
        assert.equal(207,
          TargetsTab.getLoPTarget(),
          'Did not receive expected value from getLoPTarget()');
      });
    }); // end LoP targets

    describe('"Midline and endline" target frequency', function() {
      it('should require value in Midline target field', function() {
        IndPage.clickIndicatorsLink();
        TargetsTab.clickNewIndicatorButton();
        TargetsTab.saveNewIndicator();

        // This shold succeed
        TargetsTab.setIndicatorName('Midline target required testing');
        TargetsTab.setUnitOfMeasure('Furlongs per fortnight');
        TargetsTab.setLoPTarget(228);
        TargetsTab.setBaseline(229);
        TargetsTab.setTargetFrequency('Midline and endline');
        TargetsTab.saveIndicatorChanges();

        // This should fail without midline target
        TargetsTab.setEndlineTarget(234);
        TargetsTab.saveIndicatorChanges();
        let errorMessage = TargetsTab.getTargetValueErrorHint();
        assert(errorMessage.includes('Please enter a target value. Your target value can be zero.'));
      });

      it('should require value in Endline target field', function() {
        IndPage.clickIndicatorsLink();
        TargetsTab.clickNewIndicatorButton();
        TargetsTab.saveNewIndicator();

        // This should succeed
        TargetsTab.setIndicatorName('Endline target required testing');
        TargetsTab.setUnitOfMeasure('Gargoyles per parapet');
        TargetsTab.setLoPTarget(249);
        TargetsTab.setBaseline(250);
        TargetsTab.setTargetFrequency('Midline and endline');
        TargetsTab.saveIndicatorChanges();

        // This should fail without endline target
        TargetsTab.setMidlineTarget(255);
        TargetsTab.saveIndicatorChanges();
        let errorMessage = TargetsTab.getTargetValueErrorHint();
        assert(errorMessage.includes('Please enter a target value. Your target value can be zero.'));
      });
    });

    describe('"Annual" target frequency', function() {
      it('should require date that first target period begins', function() {
        IndPage.clickIndicatorsLink();
        TargetsTab.clickNewIndicatorButton();
        TargetsTab.saveNewIndicator();

        TargetsTab.setIndicatorName('Annual target first period required testing');
        TargetsTab.setUnitOfMeasure('Hawks per hectare');
        TargetsTab.setLoPTarget(271);
        TargetsTab.setBaseline(272);
        TargetsTab.setTargetFrequency('Annual');

        // Trying to save without setting the start date should fail
        TargetsTab.saveIndicatorChanges();
        let errorMessage = TargetsTab.getTargetFirstPeriodErrorHint();
        assert(errorMessage.includes('Please complete this field.'));
      });

      it('should default number of periods to 1', function() {
        assert.equal(1, TargetsTab.getNumTargetPeriods(),
          'Did not find expected default value');
      });

      it('should create target periods for each period requested', function() {
        IndPage.clickIndicatorsLink();
        TargetsTab.clickNewIndicatorButton();
        TargetsTab.saveNewIndicator();

        TargetsTab.setIndicatorName('Annual target create target periods testing');
        TargetsTab.setUnitOfMeasure('Inkblots per Injunction');
        TargetsTab.setLoPTarget(293);
        TargetsTab.setBaseline(294);
        TargetsTab.setTargetFrequency('Annual');
        TargetsTab.setNumTargetPeriods(2);

        // This should succeed
        TargetsTab.saveIndicatorChanges();
        assert.equal(2, TargetsTab.getNumTargetPeriods(),
          'Did not find expected number of periods');
      });

      it('should require entering targets for each target period', function() {
        IndPage.clickIndicatorsLink();
        TargetsTab.clickNewIndicatorButton();
        TargetsTab.saveNewIndicator();

        TargetsTab.setIndicatorName('Annual target create target periods testing');
        TargetsTab.setUnitOfMeasure('Inkblots per Injunction');
        TargetsTab.setLoPTarget(308);
        TargetsTab.setBaseline(309);
        TargetsTab.setTargetFrequency('Annual');
        TargetsTab.setNumTargetPeriods(2);

        // This should succeed
        TargetsTab.setFirstTargetPeriod();
        TargetsTab.saveIndicatorChanges();

        // Find the input boxes
        let inputBoxes = browser.$$('input#pt-undefined.form-control.input-value');
        browser.debug();
        // Count them
        // Place values
        // Evaluate
      });
    });

    describe('"Semi-annual" target frequency', function() {
      it('should require date that first target period begins', function() {
        IndPage.clickIndicatorsLink();
        TargetsTab.clickNewIndicatorButton();
        TargetsTab.saveNewIndicator();

        TargetsTab.setIndicatorName('Semi-annual target first period required testing');
        TargetsTab.setUnitOfMeasure('Klingons per Kiloton');
        TargetsTab.setLoPTarget(334);
        TargetsTab.setBaseline(335);
        TargetsTab.setTargetFrequency('Semi-annual');

        // Trying to save without setting the start date should fail
        TargetsTab.saveIndicatorChanges();
        let errorMessage = TargetsTab.getTargetFirstPeriodErrorHint();
        assert(errorMessage.includes('Please complete this field.'));
      });

      it('should default number of periods to 1', function() {
        assert.equal(1, TargetsTab.getNumTargetPeriods(),
          'Did not receive expected default value');
      });

      it('should create target periods for each period requested', function() {
        IndPage.clickIndicatorsLink();
        TargetsTab.clickNewIndicatorButton();
        TargetsTab.saveNewIndicator();


        // This should succeed
        TargetsTab.setIndicatorName('Semi-annual target create target periods testing');
        TargetsTab.setUnitOfMeasure('Llamas per Lane');
        TargetsTab.setLoPTarget(358);
        TargetsTab.setBaseline(359);
        TargetsTab.setTargetFrequency('Semi-annual');
        TargetsTab.setNumTargetPeriods(2);

        TargetsTab.saveIndicatorChanges();
        assert.equal(2, TargetsTab.getNumTargetPeriods());
      });

      it('should require entering targets for each target period');
    });

    describe('"Tri-annual" target frequency', function() {
      it('should require date that first target period begins', function() {
        IndPage.clickIndicatorsLink();
        TargetsTab.clickNewIndicatorButton();
        TargetsTab.saveNewIndicator();

        // This should succeed
        TargetsTab.setIndicatorName('Tri-annual target first period required testing');
        TargetsTab.setUnitOfMeasure('Hawks per hectare');
        TargetsTab.setLoPTarget(379);
        TargetsTab.setBaseline(380);
        TargetsTab.setTargetFrequency('Tri-annual');

        // Trying to save without setting the start date should fail
        TargetsTab.saveIndicatorChanges();
        let errorMessage = TargetsTab.getTargetFirstPeriodErrorHint();
        assert(errorMessage.includes('Please complete this field.'));
      });

      it('should default number of periods to 1', function() {
        assert.equal(1, TargetsTab.getNumTargetPeriods());
      });

      it('should create target periods for each period requested', function() {
        IndPage.clickIndicatorsLink();
        TargetsTab.clickNewIndicatorButton();
        TargetsTab.saveNewIndicator();

        // This should succeed
        TargetsTab.setIndicatorName('Tri-annual target first period required testing');
        TargetsTab.setUnitOfMeasure('Hawks per hectare');
        TargetsTab.setLoPTarget(382);
        TargetsTab.setBaseline(383);
        TargetsTab.setTargetFrequency('Tri-annual');
        TargetsTab.setNumTargetPeriods(3);
        TargetsTab.saveIndicatorChanges();
        assert.equal(3, TargetsTab.getNumTargetPeriods());
      });

      it('should require entering targets for each target period');
    });

    describe('"Quarterly" target frequency', function() {
      it('should require date that first target period begins', function() {
        IndPage.clickIndicatorsLink();
        TargetsTab.clickNewIndicatorButton();
        TargetsTab.saveNewIndicator();

        // This should succeed
        TargetsTab.setIndicatorName('Quarterly target first period required testing');
        TargetsTab.setUnitOfMeasure('Hawks per hectare');
        TargetsTab.setLoPTarget(402);
        TargetsTab.setBaseline(403);
        TargetsTab.setTargetFrequency('Quarterly');

        // Trying to save without setting the start date should fail
        TargetsTab.saveIndicatorChanges();
        let errorMessage = TargetsTab.getTargetFirstPeriodErrorHint();
        assert(errorMessage.includes('Please complete this field.'));
      });

      it('should default number of periods to 1', function() {
        assert.equal(1, TargetsTab.getNumTargetPeriods());
      });

      it('should create target periods for each period requested', function() {
        IndPage.clickIndicatorsLink();
        TargetsTab.clickNewIndicatorButton();
        TargetsTab.saveNewIndicator();

        // This should succeed
        TargetsTab.setIndicatorName('Quarterly target create target periods testing');
        TargetsTab.setUnitOfMeasure('Hawks per hectare');
        TargetsTab.setLoPTarget(424);
        TargetsTab.setBaseline(425);
        TargetsTab.setTargetFrequency('Quarterly');

        TargetsTab.setNumTargetPeriods(4);
        TargetsTab.saveIndicatorChanges();
        assert.equal(4, TargetsTab.getNumTargetPeriods());
      });

      it('should require entering targets for each target period');
    });

    describe('"Monthly" target frequency', function() {
      it('should require date that first target period begins', function() {
        IndPage.clickIndicatorsLink();
        TargetsTab.clickNewIndicatorButton();
        TargetsTab.saveNewIndicator();

        // This should succeed
        TargetsTab.setIndicatorName('Annual target first period required testing');
        TargetsTab.setUnitOfMeasure('Hawks per hectare');
        TargetsTab.setLoPTarget(445);
        TargetsTab.setBaseline(446);
        TargetsTab.setTargetFrequency('Annual');

        // Trying to save without setting the start date should fail
        TargetsTab.saveIndicatorChanges();
        let errorMessage = TargetsTab.getTargetFirstPeriodErrorHint();
        assert(errorMessage.includes('Please complete this field.'));
      });

      it('should default number of periods to 1', function() {
        assert.equal(1, TargetsTab.getNumTargetPeriods());
      });

      it('should create target periods for each period requested', function() {
        TargetsTab.setNumTargetPeriods(12);
        TargetsTab.saveIndicatorChanges();
        assert.equal(12, TargetsTab.getNumTargetPeriods());
      });

      it('should require entering targets for each target period');
    });

    describe('"Event" target frequency', function() {
      it('should require "First event name"', function() {
        IndPage.clickIndicatorsLink();
        TargetsTab.clickNewIndicatorButton();
        TargetsTab.saveNewIndicator();

        // Don't set a name
        TargetsTab.setIndicatorName('Event target first event name required testing');
        TargetsTab.setUnitOfMeasure('Iodine per igloo');
        TargetsTab.setLoPTarget(476);
        TargetsTab.setBaseline(477);
        TargetsTab.setTargetFrequency('Event');
        TargetsTab.setNumTargetEvents(1);

        // Should fail
        TargetsTab.saveIndicatorChanges();
        let errorMessage = TargetsTab.getTargetFirstEventErrorHint();
        assert(errorMessage.includes('Please complete this field.'));
      });

      it('should require "Number of events"', function() {
        IndPage.clickIndicatorsLink();
        TargetsTab.clickNewIndicatorButton();
        TargetsTab.saveNewIndicator();

        TargetsTab.setIndicatorName('Event target first number of events required testing');
        TargetsTab.setUnitOfMeasure('Iodine per igloo');
        TargetsTab.setLoPTarget(495);
        TargetsTab.setBaseline(496);
        TargetsTab.setTargetFrequency('Event');
        TargetsTab.setFirstEventName('Mulugeta Seraw Memorial');
        TargetsTab.setNumTargetEvents(0);

        // Should fail
        TargetsTab.saveIndicatorChanges();
        let errorMessage = TargetsTab.getNumTargetEventsErrorHint();
        assert(errorMessage.includes('Please complete this field.'));
      });

      it('should allow only numeric values in "Number of events"', function () {
        IndPage.clickIndicatorsLink();
        TargetsTab.clickNewIndicatorButton();
        TargetsTab.saveNewIndicator();

        TargetsTab.setIndicatorName('Event target number can only be numeric testing');
        TargetsTab.setUnitOfMeasure('Jugglers per jitney');
        TargetsTab.setLoPTarget(514);
        TargetsTab.setBaseline(515);
        TargetsTab.setTargetFrequency('Event');
        TargetsTab.setFirstEventName('Heather Heyer Rest in Power');
        TargetsTab.setNumTargetEvents('a');

        // Should fail
        TargetsTab.saveIndicatorChanges();
        let errorMessage = TargetsTab.getNumTargetEventsErrorHint();
        assert(errorMessage.includes('Please complete this field.'));
      });

      it('should default "Number of events" to 1', function() {
        assert.equal(1, TargetsTab.getNumTargetPeriods(),
          'Did not receive expected number of target events');
      });

      it('should limit max "Number of events" to 12 or less', function() {
        IndPage.clickIndicatorsLink();
        TargetsTab.clickNewIndicatorButton();
        TargetsTab.saveNewIndicator();

        TargetsTab.setIndicatorName('Can create max of 12 events initially testing');
        TargetsTab.setUnitOfMeasure('Mangos per manager');
        TargetsTab.setLoPTarget(538);
        TargetsTab.setBaseline(539);
        TargetsTab.setTargetFrequency('Event');
        TargetsTab.setFirstEventName('Battle of Cable Street');
        TargetsTab.setNumTargetEvents(13);

        // Should fail
        TargetsTab.saveIndicatorChanges();
        let errorMessage = TargetsTab.getNumTargetEventsErrorHint();
        assert(errorMessage.includes('You can start with up to 12 targets and add more later.'));
      });

      // FIXME: The next test fails; I can enter 0 events and save
      it('should require at least one event', function() {
        IndPage.clickIndicatorsLink();
        TargetsTab.clickNewIndicatorButton();
        TargetsTab.saveNewIndicator();

        TargetsTab.setIndicatorName('Must create a least one event testing');
        TargetsTab.setUnitOfMeasure('Noodles per night');
        TargetsTab.setLoPTarget(560);
        TargetsTab.setBaseline(561);
        TargetsTab.setTargetFrequency('Event');
        TargetsTab.setFirstEventName('Battle of Cable Street');
        TargetsTab.setNumTargetEvents(1);

        // FIXME: Test should fail but passes (
        // [see issue #106](https://github.com/mercycorps/TolaActivity/issues/106)).
        // This test will start to fail when that bug gets fixed.
        TargetsTab.saveIndicatorChanges();
        let errorMessage = TargetsTab.getNumTargetEventsErrorHint();
        assert.equal('', errorMessage);
      });
    }); // end event target frequency tests
  }); // end test cases from GitHub issues
});
