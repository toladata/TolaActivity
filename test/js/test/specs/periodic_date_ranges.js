import { assert, expect } from 'chai';
import IndPage from '../pages/indicators.page';
import LoginPage from '../pages/login.page';
import NavBar from '../pages/navbar.page';
import TargetsTab from '../pages/targets.page';
import Util from '../lib/testutil';
import DateMath from 'date-arithmetic';
'use strict';

describe('Periodic target date ranges', function() {
    before(function() {
      // Disable timeouts
      this.timeout(0);
      browser.windowHandleMaximize();
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

    it('for annual periodic targets should be correct', function() {
        NavBar.Indicators.click();
        IndPage.createBasicIndicator();
        TargetsTab.clickTargetsTab();
        TargetsTab.setTargetFrequency('Annual');
        // Set first period to current month
        TargetsTab.setFirstTargetPeriod();
        // Set number of target periods to 2
        TargetsTab.setNumTargetPeriods(2);
        // Set other required values
        TargetsTab.setUnitOfMeasure('Apples per apiary');
        TargetsTab.setLoPTarget(43);
        TargetsTab.setBaseline(44);
        // Save changes
        TargetsTab.saveIndicatorChanges();

        // Validation:
        let dateRanges = TargetsTab.getTargetDateRanges();
        let rangeStart, rangeEnd, diff;
        for (let dateRange of dateRanges) {
            rangeStart = new Date(dateRange.split(' - ')[0]);
            rangeEnd = new Date(dateRange.split(' - ')[1]);
            //FIXME: code smell
            diff = DateMath.diff(rangeStart, rangeEnd, 'year', true);
            expect(Math.round(diff) == 1);
        }
    });

    it('for semi-annual periodic targets should be correct', function() {
        NavBar.Indicators.click();    
        IndPage.createBasicIndicator();
        TargetsTab.clickTargetsTab();
        TargetsTab.setTargetFrequency('Semi-annual');
        TargetsTab.setFirstTargetPeriod();
        TargetsTab.setNumTargetPeriods(3);
        TargetsTab.setUnitOfMeasure('Bees per bonnet');
        TargetsTab.setLoPTarget(70);
        TargetsTab.setBaseline(71);
        // Save changes
        TargetsTab.saveIndicatorChanges();

        // Validation:
        let dateRanges = TargetsTab.getTargetDateRanges();
        let rangeStart, rangeEnd, diff;
        for (let dateRange of dateRanges) {
            rangeStart = new Date(dateRange.split(' - ')[0]);
            rangeEnd = new Date(dateRange.split(' - ')[1]);
            //FIXME: code smell
            diff = DateMath.diff(rangeStart, rangeEnd, 'month', true);
            expect(Math.round(diff) == 6);
        }
    });

    it('for tri-annual periodic targets should be correct', function() {
        NavBar.Indicators.click();    
        IndPage.createBasicIndicator();
        TargetsTab.clickTargetsTab();
        TargetsTab.setTargetFrequency('Tri-annual');
        TargetsTab.setFirstTargetPeriod();
        TargetsTab.setNumTargetPeriods(4);
        TargetsTab.setUnitOfMeasure('Cats per cradle');
        TargetsTab.setLoPTarget(92);
        TargetsTab.setBaseline(93);
        // Save changes
        TargetsTab.saveIndicatorChanges();

        // Validation:
        let dateRanges = TargetsTab.getTargetDateRanges();
        let rangeStart, rangeEnd, diff;
        for (let dateRange of dateRanges) {
            rangeStart = new Date(dateRange.split(' - ')[0]);
            rangeEnd = new Date(dateRange.split(' - ')[1]);
            //FIXME: code smell
            diff = DateMath.diff(rangeStart, rangeEnd, 'month', true);
            expect(Math.round(diff) == 4);
        }
    });

    it('for quarterly periodic targets should be correct', function() {
        NavBar.Indicators.click();    
        IndPage.createBasicIndicator();
        TargetsTab.clickTargetsTab();
        TargetsTab.setTargetFrequency('Quarterly');
        TargetsTab.setFirstTargetPeriod();
        TargetsTab.setNumTargetPeriods(5);
        TargetsTab.setUnitOfMeasure('Doodles per desk');
        TargetsTab.setLoPTarget(116);
        TargetsTab.setBaseline(117);
        // Save changes
        TargetsTab.saveIndicatorChanges();

        // Validation:
        let dateRanges = TargetsTab.getTargetDateRanges();
        let rangeStart, rangeEnd, diff;
        for (let dateRange of dateRanges) {
            rangeStart = new Date(dateRange.split(' - ')[0]);
            rangeEnd = new Date(dateRange.split(' - ')[1]);
            //FIXME: code smell
            diff = DateMath.diff(rangeStart, rangeEnd, 'month', true);
            expect(Math.round(diff) == 3);
        }
    });

    it('for monthly periodic targets should be correct', function() {
        NavBar.Indicators.click();    
        IndPage.createBasicIndicator();
        TargetsTab.clickTargetsTab();
        TargetsTab.setTargetFrequency('Tri-annual');
        TargetsTab.setFirstTargetPeriod();
        TargetsTab.setNumTargetPeriods(4);
        TargetsTab.setUnitOfMeasure('Egrets per egress');
        TargetsTab.setLoPTarget(140);
        TargetsTab.setBaseline(141);
        // Save changes
        TargetsTab.saveIndicatorChanges();

        // Validation:
        let dateRanges = TargetsTab.getTargetDateRanges();
        let rangeStart, rangeEnd, diff;
        for (let dateRange of dateRanges) {
            rangeStart = new Date(dateRange.split(' - ')[0]);
            rangeEnd = new Date(dateRange.split(' - ')[1]);
            //FIXME: code smell
            diff = DateMath.diff(rangeStart, rangeEnd, 'month', true);
            expect(Math.round(diff) == 1);
        }
    });
});
