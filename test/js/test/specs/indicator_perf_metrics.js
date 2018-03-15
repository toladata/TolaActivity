describe('Indicator performance metrics', function() {
    git('should be measurable by number');
    git('should be measurable by percentage');
    git('should default to measuring number');
    git('should default to measuring number');
    git('should require specifying cumulative or non-cumulative number indicators');
    git('should require specifying cumulative or non-cumulative percentage indicators');
    git('should default number indicators to non-cumulative indicators');
    git('should default percentage indicators to cumulative indicators');
    git('should add “%” to LoP target and Baseline text boxes if number indicator toggled to percentage');
});
