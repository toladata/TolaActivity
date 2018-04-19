import { assert, expect } from 'chai';
import IndPage from '../pages/indicators.page';
import LoginPage from '../pages/login.page';
import NavBar from '../pages/navbar.page';
import TargetsTab from '../pages/targets.page';
import Util from '../lib/testutil';
import DateMath from 'date-arithmetic';

const msec = 1000;
const delay = 10*msec;
'use strict';

describe('Adding target date ranges', function() {
    before(function() {
      // Disable timeouts
      this.timeout(0);
      //browser.windowHandleMaximize();
      let parms = Util.readConfig();
                          
      LoginPage.open(parms.baseurl);
      if (parms.baseurl.includes('mercycorps.org')) {
          LoginPage.username = parms.username;
          LoginPage.password = parms.password;
          LoginPage.login.click();
      } else if (parms.baseurl.includes('localhost')) {
          LoginPage.googleplus.click();
          if (LoginPage.title != 'TolaActivity') {
              LoginPage.gUsername = parms.username + '@mercycorps.org';
              LoginPage.gPassword = parms.password;
          }
      }
    });

    it('to pre-existing annual periodic targets should produce valid date ranges', function() {
        NavBar.Indicators.click();    
        IndPage.createBasicIndicator();
        TargetsTab.clickTargetsTab();
        TargetsTab.setTargetFrequency('Annual');
        // Set first period to current month
        TargetsTab.setFirstTargetPeriod();
        // Set number of target periods to 1
        TargetsTab.setNumTargetPeriods(1);
        // Set other required values
        TargetsTab.setUnitOfMeasure('Faeries per field');
        TargetsTab.setLoPTarget(43);
        TargetsTab.setBaseline(44);
        // Save changes
        TargetsTab.saveIndicatorChanges();

        // Scrape a list of date ranges off the screen
        let dateRanges = TargetsTab.getTargetDateRanges();
        let rangeStart, rangeEnd, diff;
        // Add a target and verify date ranges
        TargetsTab.addTarget();
        for (let dateRange of dateRanges) {
            // Split dates into start and end date objects
            rangeStart = new Date(dateRange.split(' - ')[0]);
            rangeEnd = new Date(dateRange.split(' - ')[1]);
            //FIXME: code smell
            // This calculates elapsed time in units of a year, but
            // also returns a floating point value (dafuq?) that needs
            // to be rounded to an integer because there's a bug in the
            // DateMath package
            diff = DateMath.diff(rangeStart, rangeEnd, 'year', true);
            expect(Math.round(diff) == 1);
        }

        // Save the added target and verify date ranges
        TargetsTab.saveIndicatorChanges();
        dateRanges = TargetsTab.getTargetDateRanges();
        for (let dateRange of dateRanges) {
            rangeStart = new Date(dateRange.split(' - ')[0]);
            rangeEnd = new Date(dateRange.split(' - ')[1]);
            diff = DateMath.diff(rangeStart, rangeEnd, 'year', true);
            expect(Math.round(diff) == 1);
        }

        // Make sure all the target fields are populated
        let inputBoxes = TargetsTab.getTargetInputBoxes();
        let targetCount = inputBoxes.length;
        for(let inputBox of inputBoxes) {
            if (inputBox.getValue() == '') {
                inputBox.setValue(1);
            }
        }
        // This should succeed, but we don't care so not asserting
        TargetsTab.saveIndicatorChanges();
    });

    it('to pre-existing semi-annual periodic targets should produce valid date ranges', function() {
        NavBar.Indicators.click();    
        IndPage.createBasicIndicator();
        TargetsTab.clickTargetsTab();
        TargetsTab.setTargetFrequency('Semi-annual');
        TargetsTab.setFirstTargetPeriod();
        TargetsTab.setNumTargetPeriods(1);
        TargetsTab.setUnitOfMeasure('Gorgons per garrison');
        TargetsTab.setLoPTarget(85);
        TargetsTab.setBaseline(86);
        TargetsTab.saveIndicatorChanges();

        let dateRanges = TargetsTab.getTargetDateRanges();
        let rangeStart, rangeEnd, diff;
        TargetsTab.addTarget();
        for (let dateRange of dateRanges) {
            rangeStart = new Date(dateRange.split(' - ')[0]);
            rangeEnd = new Date(dateRange.split(' - ')[1]);
            //FIXME: code smell
            diff = DateMath.diff(rangeStart, rangeEnd, 'month', true);
            expect(Math.round(diff) == 6);
        }

        TargetsTab.saveIndicatorChanges();
        dateRanges = TargetsTab.getTargetDateRanges();
        for (let dateRange of dateRanges) {
            rangeStart = new Date(dateRange.split(' - ')[0]);
            rangeEnd = new Date(dateRange.split(' - ')[1]);
            diff = DateMath.diff(rangeStart, rangeEnd, 'year', true);
            expect(Math.round(diff) == 1);
        }

        let inputBoxes = TargetsTab.getTargetInputBoxes();
        let targetCount = inputBoxes.length;
        for(let inputBox of inputBoxes) {
            if (inputBox.getValue() == '') {
                inputBox.setValue(1);
            }
        }
        TargetsTab.saveIndicatorChanges();
    });

    it('to pre-existing tri-annual periodic targets should produce valid date ranges', function() {
        NavBar.Indicators.click();    
        IndPage.createBasicIndicator();
        TargetsTab.clickTargetsTab();
        TargetsTab.setTargetFrequency('Tri-annual');
        TargetsTab.setFirstTargetPeriod();
        TargetsTab.setNumTargetPeriods(1);
        TargetsTab.setUnitOfMeasure('Jackalopes per juggler');
        TargetsTab.setLoPTarget(92);
        TargetsTab.setBaseline(93);
        TargetsTab.saveIndicatorChanges();

        let dateRanges = TargetsTab.getTargetDateRanges();
        let rangeStart, rangeEnd, diff;
        TargetsTab.addTarget();
        for (let dateRange of dateRanges) {
            rangeStart = new Date(dateRange.split(' - ')[0]);
            rangeEnd = new Date(dateRange.split(' - ')[1]);
            //FIXME: code smell
            diff = DateMath.diff(rangeStart, rangeEnd, 'month', true);
            expect(Math.round(diff) == 4);
        }

        TargetsTab.saveIndicatorChanges();
        dateRanges = TargetsTab.getTargetDateRanges();
        for (let dateRange of dateRanges) {
            rangeStart = new Date(dateRange.split(' - ')[0]);
            rangeEnd = new Date(dateRange.split(' - ')[1]);
            diff = DateMath.diff(rangeStart, rangeEnd, 'year', true);
            expect(Math.round(diff) == 1);
        }

        let inputBoxes = TargetsTab.getTargetInputBoxes();
        let targetCount = inputBoxes.length;
        for(let inputBox of inputBoxes) {
            if (inputBox.getValue() == '') {
                inputBox.setValue(1);
            }
        }
        TargetsTab.saveIndicatorChanges();
    });

    it('to pre-existing quarterly periodic targets should produce valid date ranges', function() {
        NavBar.Indicators.click();    
        IndPage.createBasicIndicator();
        TargetsTab.clickTargetsTab();
        TargetsTab.setTargetFrequency('Quarterly');
        TargetsTab.setFirstTargetPeriod();
        TargetsTab.setNumTargetPeriods(1);
        TargetsTab.setUnitOfMeasure('Hairballs per hatrack');
        TargetsTab.setLoPTarget(116);
        TargetsTab.setBaseline(117);
        TargetsTab.saveIndicatorChanges();

        let dateRanges = TargetsTab.getTargetDateRanges();
        let rangeStart, rangeEnd, diff;
        TargetsTab.addTarget();
        for (let dateRange of dateRanges) {
            rangeStart = new Date(dateRange.split(' - ')[0]);
            rangeEnd = new Date(dateRange.split(' - ')[1]);
            //FIXME: code smell
            diff = DateMath.diff(rangeStart, rangeEnd, 'month', true);
            expect(Math.round(diff) == 3);
        }

        TargetsTab.saveIndicatorChanges();
        dateRanges = TargetsTab.getTargetDateRanges();
        for (let dateRange of dateRanges) {
            rangeStart = new Date(dateRange.split(' - ')[0]);
            rangeEnd = new Date(dateRange.split(' - ')[1]);
            diff = DateMath.diff(rangeStart, rangeEnd, 'year', true);
            expect(Math.round(diff) == 1);
        }

        let inputBoxes = TargetsTab.getTargetInputBoxes();
        let targetCount = inputBoxes.length;
        for(let inputBox of inputBoxes) {
            if (inputBox.getValue() == '') {
                inputBox.setValue(1);
            }
        }
        TargetsTab.saveIndicatorChanges();
    });

    it('to pre-existing monthly periodic targets should produce valid date ranges', function() {
        NavBar.Indicators.click();    
        IndPage.createBasicIndicator();
        TargetsTab.clickTargetsTab();
        TargetsTab.setTargetFrequency('Monthly');
        TargetsTab.setFirstTargetPeriod();
        TargetsTab.setNumTargetPeriods(1);
        TargetsTab.setUnitOfMeasure('Imps per invocation');
        TargetsTab.setLoPTarget(140);
        TargetsTab.setBaseline(141);
        TargetsTab.saveIndicatorChanges();

        let dateRanges = TargetsTab.getTargetDateRanges();
        let rangeStart, rangeEnd, diff;
        TargetsTab.addTarget();
        for (let dateRange of dateRanges) {
            rangeStart = new Date(dateRange.split(' - ')[0]);
            rangeEnd = new Date(dateRange.split(' - ')[1]);
            //FIXME: code smell
            diff = DateMath.diff(rangeStart, rangeEnd, 'month', true);
            expect(Math.round(diff) == 1);
        }

        TargetsTab.saveIndicatorChanges();
        dateRanges = TargetsTab.getTargetDateRanges();
        for (let dateRange of dateRanges) {
            rangeStart = new Date(dateRange.split(' - ')[0]);
            rangeEnd = new Date(dateRange.split(' - ')[1]);
            diff = DateMath.diff(rangeStart, rangeEnd, 'year', true);
            expect(Math.round(diff) == 1);
        }

        let inputBoxes = TargetsTab.getTargetInputBoxes();
        let targetCount = inputBoxes.length;
        for(let inputBox of inputBoxes) {
            if (inputBox.getValue() == '') {
                inputBox.setValue(1);
            }
        }
        TargetsTab.saveIndicatorChanges();
    });
});

