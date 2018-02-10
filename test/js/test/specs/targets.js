var assert = require('chai').assert;
var expect = require('chai').expect;
var LoginPage = require('../pages/login.page.js');
var IndPage = require('../pages/indicators.page.js');
var TargetsTab = require('../pages/targets.page.js');
var util = require('../lib/testutil.js');

describe('Indicator Targets', function() {
  // Disable timeouts
  this.timeout(0);

  describe('Create new indicator dialog', function() {
    it('should require unauthenticated users to login', function() {
      let parms = util.readConfig();
      LoginPage.open(parms.baseurl);
      LoginPage.setUserName(parms.username);
      LoginPage.setPassword(parms.password);
      LoginPage.clickLoginButton();
      IndPage.open();
      assert.equal('Program Indicators', IndPage.pageName());
    });

    it('should open new indicator form when button is clicked', function() {
      TargetsTab.clickNewIndicatorButton();
      assert.equal('Create an Indicator', TargetsTab.pageName());
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
      assert.equal('', TargetsTab.getTargetFrequency());
    });

    it('should save data when "Save changes" button clicked', function() {
      TargetsTab.setIndicatorName('Testing the save changes button');
      TargetsTab.setUnitOfMeasure('Dashes');
      TargetsTab.setLoPTarget(52);
      TargetsTab.setBaseline(53);
      TargetsTab.setTargetFrequency('Life of Program (LoP) only');
      TargetsTab.saveIndicatorChanges();
    });
  }); // end new indicator dialog

  // Test cases from issues #21, #24, #25, #30, #33, #35, #37, #42, #43
  describe('Targets tab', function() {
    this.timeout(0);
    it('should require "Unit of measure"', function() {
      // Set everything but the unit of measure then try to save
      IndPage.clickIndicatorsLink();
      TargetsTab.clickNewIndicatorButton();
      TargetsTab.saveNewIndicator();
      TargetsTab.setIndicatorName('Unit of measure test');
      TargetsTab.setLoPTarget(68);
      TargetsTab.setBaseline(69);
      TargetsTab.setTargetFrequency('Life of Program (LoP) only');
      TargetsTab.saveIndicatorChanges();
      // Should get this error message
      assert.equal('Please complete all required fields in the Targets tab.',
                   TargetsTab.getAlertMsg(),
                   'Did not receive expected failure message');
    });

    it('should require "Life of Program (LoP) target" value', function() {
      // Set everything but the LoP target then try to save
      IndPage.clickIndicatorsLink();
      TargetsTab.clickNewIndicatorButton();
      TargetsTab.saveNewIndicator();
      TargetsTab.setIndicatorName('LoP target value test');
      TargetsTab.setUnitOfMeasure('Buckets');
      TargetsTab.setBaseline(84);
      TargetsTab.setTargetFrequency('Life of Program (LoP) only');
      TargetsTab.saveIndicatorChanges();
      // Should get this error message
      assert.equal('Please complete all required fields in the Targets tab.',
                   TargetsTab.getAlertMsg(),
                   'Did not receive expected failure message');
    });

    it('should require target Baseline if "Not applicable" not checked', function() {
      // Set everything but the baseline value then try to save
      IndPage.clickIndicatorsLink();
      TargetsTab.clickNewIndicatorButton();
      TargetsTab.saveNewIndicator();
      TargetsTab.setIndicatorName('Baseline value test');
      TargetsTab.setUnitOfMeasure('Crates');
      TargetsTab.setLoPTarget(103);
      TargetsTab.setTargetFrequency('Life of Program (LoP) only');
      TargetsTab.saveIndicatorChanges();
      // Should get this error message
      assert.equal('Please complete all required fields in the Targets tab.',
                   TargetsTab.getAlertMsg(),
                   'Did not receive expected failure message');
    });

    it('should *not* require target Baseline if "Not applicable" *is* checked', function() {
      // Set everything but the baseline value
      IndPage.clickIndicatorsLink();
      TargetsTab.clickNewIndicatorButton();
      TargetsTab.saveNewIndicator();
      TargetsTab.setIndicatorName('Baseline value not applicable test');
      TargetsTab.setUnitOfMeasure('Drops');
      TargetsTab.setLoPTarget(119);
      TargetsTab.setTargetFrequency('Life of Program (LoP) only');
      // check "Not applicable" then try to save
      TargetsTab.setBaselineNA();
      TargetsTab.saveIndicatorChanges();
      // Should get this success message
      // FIXME: This test fails because the success message is too fast;
      //        I don't know how to catch it with WebDriver
      assert.equal('Success, form data saved.',
                   TargetsTab.getAlertMsg(),
                   'Did not receive expected success message');
      // Should not get this message
      // FIXME: I'd rather not use the negative logic; much prefer the
      //        positive form above if it can be made to work
      assert.notEqual('Please complete all required fields in the Targets tab.',
                       IndPage.getAlertMsg(),
                       'Received unexpected error message');
    });

    it('should require Target frequency', function() {
      // Set everything but the target frequency then try to save
      IndPage.clickIndicatorsLink();
      TargetsTab.clickNewIndicatorButton();
      TargetsTab.saveNewIndicator();
      TargetsTab.setIndicatorName('Target frequency test');
      TargetsTab.setUnitOfMeasure('Emissions');
      TargetsTab.setLoPTarget(145);
      TargetsTab.setBaseline(146);
      TargetsTab.saveIndicatorChanges();
      // Should get this error message
      assert.equal('Please complete all required fields in the Targets tab.',
                   TargetsTab.getAlertMsg(),
                   'Did not receive expected failure message');
    });

    it('should have 8 options on Target frequency selection menu');

    describe('"Life of Program (LoP) only" target frequency', function() {
      it('should permit only numeric values for LoP target', function() {
        IndPage.clickIndicatorsLink();
        TargetsTab.clickNewIndicatorButton();
        TargetsTab.saveNewIndicator();

        TargetsTab.setIndicatorName('LoP only target testing');
        TargetsTab.setUnitOfMeasure('Furlongs per fortnight');
        TargetsTab.setLoPTarget(164);
        TargetsTab.setBaseline(165);
        TargetsTab.setTargetFrequency('Life of Program (LoP) only');
        // This should succeed
        TargetsTab.saveIndicatorChanges();
      });

      it('should reject non-numeric values for LoP target', function() {
        TargetsTab.setLoPTarget('"166"');
        // This should fail
        TargetsTab.saveIndicatorChanges();
        let errorHint = TargetsTab.getLoPErrorHint();
        assert(errorHint.includes('Please enter a number larger than zero'),
               'Did not receive expected failure message');
        // Make it numeric; this should succeed
        TargetsTab.setLoPTarget(179);
        TargetsTab.saveIndicatorChanges();
        assert.equal(179,
                     TargetsTab.getLoPTarget(),
                     'Did not receive expected value from getLoPTarget()');
      });

      // FIXME: Are these 2 test cases still important?
      it('should permit non-numeric values only in legacy data for LoP target');
      it('should require numeric value for LoP target if non-numeric legacy data is modified');
    });

    describe('"Midline and endline" target frequency', function() {
      it('should require value in Midline target field', function() {
        IndPage.clickIndicatorsLink();
        TargetsTab.clickNewIndicatorButton();
        TargetsTab.saveNewIndicator();

        // This shold succeed
        TargetsTab.setIndicatorName('Midline target required testing');
        TargetsTab.setUnitOfMeasure('Furlongs per fortnight');
        TargetsTab.setLoPTarget(199);
        TargetsTab.setBaseline(200);
        TargetsTab.setTargetFrequency('Midline and endline');
        TargetsTab.saveIndicatorChanges();

        // This should fail without midline target
        TargetsTab.setEndlineTarget(202);
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
        TargetsTab.setLoPTarget(219);
        TargetsTab.setBaseline(220);
        TargetsTab.setTargetFrequency('Midline and endline');
        TargetsTab.saveIndicatorChanges();

        // This should fail without endline target
        TargetsTab.setMidlineTarget(225);
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

        // This should succeed
        TargetsTab.setIndicatorName('Annual target first period required testing');
        TargetsTab.setUnitOfMeasure('Hawks per hectare');
        TargetsTab.setLoPTarget(242);
        TargetsTab.setBaseline(242);
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
        TargetsTab.setNumTargetPeriods(2);
        TargetsTab.saveIndicatorChanges();
        assert.equal(2, TargetsTab.getNumTargetPeriods());
      });

      it('should require entering targets for each target period')
    });

    describe('"Semi-annual" target frequency', function() {
      it('should require date that first target period begins', function() {
        IndPage.clickIndicatorsLink();
        TargetsTab.clickNewIndicatorButton();
        TargetsTab.saveNewIndicator();

        // This should succeed
        TargetsTab.setIndicatorName('Semi-annual target first period required testing');
        TargetsTab.setUnitOfMeasure('Hawks per hectare');
        TargetsTab.setLoPTarget(265);
        TargetsTab.setBaseline(266);
        TargetsTab.setTargetFrequency('Semi-annual');

        // Trying to save without setting the start date should fail
        TargetsTab.saveIndicatorChanges();
        let errorMessage = TargetsTab.getTargetFirstPeriodErrorHint();
        assert(errorMessage.includes('Please complete this field.'));
      });

      it('should default number of periods to 1', function() {
        assert.equal(1, TargetsTab.getNumTargetPeriods());
      });

      it('should create target periods for each period requested', function() {
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
        TargetsTab.setIndicatorName('Annual target first period required testing');
        TargetsTab.setUnitOfMeasure('Hawks per hectare');
        TargetsTab.setLoPTarget(238);
        TargetsTab.setBaseline(239);
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
        TargetsTab.setIndicatorName('Annual target first period required testing');
        TargetsTab.setUnitOfMeasure('Hawks per hectare');
        TargetsTab.setLoPTarget(238);
        TargetsTab.setBaseline(239);
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
        TargetsTab.setLoPTarget(238);
        TargetsTab.setBaseline(239);
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
      it('should require "First event name"');
      it('should require "Number of events"');
      it('should allow only numeric values in "Number of events"');
      it('should default "Number of events" to 1');
      it('should limit "Number of events" between 1 and 12 inclusive');
      // FIXME: The next test fails; I can enter 0 events and save
      it('should require at least one event');
      it('should inform user that only 12 events can be created at once');
    });
  }); // end test cases from GitHub issues
});
