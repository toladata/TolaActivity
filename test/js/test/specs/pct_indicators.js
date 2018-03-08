describe('Non-cumulative percentage indicators', function() {
  it('should display percentage signs in all the appropriate fields');
  it('should calculate LoP result as the average of target period values');
});


describe('Cumulative percentage indicators', function() {
  it('should display percentage signs in all the appropriate fields');
  it('should set LoP value to latest period value');
  it('should not perform calculations with collected data')
  it('should display results cumulatively');
  it('should not have an average row');
  it('should have the same values between LoP Actual and % Met for latest period');
});
