describe('Indicator performance metrics', function() {
  it('should be measurable by discrete count');
  it('should be measurable by percentage');
  it('should default to measuring discrete count');
  it('should add “%” signs automatically to LoP targets that are percentage indicators');
  it('should add “%” signs automatically to Baseline values that are percentage indicators');
  it('should add “%” signs automatically to data records for percentage indicators');
  it('should require defining count indicators as cumulative or non-cumulative');
  it('should require defined percentage indicators as cumulative or non-cumulative');
  it('should default count indicators to non-cumulative');
  it('should default percentage indicators to cumulative');
  it('should refresh display immediately when count indicator toggled to percentage');
  it('should refresh display immediately when percentage indicator toggled to count');
});
