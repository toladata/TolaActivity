import LoginPage from '../pages/login.page';
import NavBar from '../pages/navbar.page';
import IndPage from '../pages/indicators.page';
import TargetsTab from '../pages/targets.page';
'use strict';

/**
 * Indicator evidence table: number indicator config and display
 * Tests from mc/issues/115
 */
describe('Indicator evidence number indicators', function() {
    before(function() {});
    it('should take the LoP target of a NC number indicator from LoP target field');
    it('should calculate the LoP actual of NC number indicators as sum of target actuals');
    it('should take the LoP target of a C number indicators from LoP target field');
    it('should take the LoP actual of C number indicators from the latest target actual');
}); 


