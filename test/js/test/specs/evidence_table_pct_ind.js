import LoginPage from '../pages/login.page';
import NavBar from '../pages/navbar.page';
import IndPage from '../pages/indicators.page';
import TargetsTab from '../pages/targets.page';
'use strict';

/**
 * Indicator evidence table: percentage indicator config and display
 * Tests from mc/issues/115
 */
describe('Indicator evidence number indicators', function() {
    before(function() {});
    it('should take the LoP target of a C percentage indicator from LoP target field');
    it('should take the LoP actual of a C percentage indicators from the latest target actual');
    it('should only display a % Met value for the LoP row of C percentage indicators');
    it('should display “N/A” for % Met in intermediate target rows of C percentage indicators');
    it('should take the LoP target of NC percentage indicators from the LoP target field');
    it('should calculate the LoP actual of NC percentage indicators as average of the periodic values');
    it('should append “avg.” to the LoP actual value of NC percentage indicators');
    it('should only display a % Met value for the LoP row of NC percentage indicators');
    it('should display “N/A” for % Met in intermediate target rows of NC percentage indicators');

}); 


