import LoginPage from '../pages/login.page';
import NavBar from '../pages/navbar.page';
import IndPage from '../pages/indicators.page';
import TargetsTab from '../pages/targets.page';
'use strict';

/**
 * General number and percentage indicator tests
 * Tests from mc/issues/114, mc/issues/117
 */
describe('Number indicators config and display', function() {
    before(function() {});
    it('should default to number indicators');
    it('should default number indicators to non-cumulative indicators');
    it('should default percentage indicators to cumulative indicators');
    it('should add “%” to LoP target and Baseline text boxes');
}); 
