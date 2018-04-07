describe('Target period table: percentage indicator config and display', function() {
    it('should append a % sign to numeric values types in numeric fields');
    it('should not permit non-numeric values to be typed in numeric fields');
    it('should allow to specify percentage indicators as cumulative or non-cumulative');
    it('should make percentage indicators default to cumulative');
    it('should remove the “Sum of targets” row from the table for a cumulative percentage indicator');
    it('should add an “Average of targets” row to the table for a cumulative percentage indicator');
    it('should make “Average of targets” value the average of the target period values in the table');
});
