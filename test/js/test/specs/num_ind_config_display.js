import LoginPage from '../pages/login.page';
import NavBar from '../pages/navbar.page';
import IndPage from '../pages/indicators.page';
import TargetsTab from '../pages/targets.page';
'use strict';

/**
 * Target period table: number indicator config and display
 * Tests from mc/issues/116
 */
describe('Number indicators config and display', function() {
    before(function() {});

    it('should allow to specify number indicators as non-cumulative or cumulative');
    it('should make non-cumulative number indicators the default option');
    it('should remove the “Sum of targets” row from the table for a cumulative number indicator');
}); 
