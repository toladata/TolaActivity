describe('Indicator evidence table: number indicators', function() {
    it('should take the LoP target of non-cumulative number indicator from LoP target field');
    it('should make the LoP actual of non-cumulative number indicators the sum of the periodic target actuals');
    it('should take the LoP target of cumulative number indicators from LoP target field');
    it('should make the LoP actual of cumulative number indicators the same as the latest target period actual value');
});

describe('Indicator evidence table: percentabe indicators', function() {
    it('should take the LoP target of cumulative percentage indicators from the LoP target field');
    it('should make the LoP actual of cumulative percentage indicators the same as the latest target period actual value');
    it('should only display a % Met value for the LoP row of cumulative percentage indicators');
    it('should display “N/A” for % Met in intermediate target rows of cumulative percentage indicators');
    it('should take the LoP target of non-cumulative percentage indicators from the LoP target field');
    it('should make the LoP actual of non-cumulative percentage indicators the average of the periodic target values');
    it('should append “avg.” to the LoP actual value of non-cumulative percentage indicators');
    it('should only display a % Met value for the LoP row of non-cumulative percentage indicators');
    it('should display “N/A” for % Met in intermediate target rows of non-cumulative percentage indicators');
});
