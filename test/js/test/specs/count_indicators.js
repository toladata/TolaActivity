// Proposed test cases for TolaActivity v1.9.5

describe('Non-cumulative count indicators', function() {
  it('should calculate target period results from data collected during target period');
  it('should calculate the LoP result by summing the target period values');
});


describe('Cumulative count indicators', function() {
  it('should include previous period values when calculating target period results');
  it('should have the same values in the LoP target and the final period's target');
});
