exports.config = {
    // Specify Test Files
    specs: [
        './tests/**/*.js'
    ],
    // Patterns to exclude.
    exclude: [
        //'./tests/**/*.js'
    ],
    suites: {
        login: [
            'test/specs/00_login.js'
        ],
        dashboard: [
            'test/specs/dashboard.js'
        ],
        indicators: [
            'test/specs/annual.js',
            'test/specs/event.js',
            'test/specs/lop_only.js',
            'test/specs/mid-end_line.js',
            'test/specs/monthly.js',
            'test/specs/quarterly.js',
            'test/specs/semiannual.js',
            'test/specs/triannual.js',
            'test/specs/count_indicators.js',
            'test/specs/create_indicator_form.js',
            'test/specs/filtering_indicators.js',
            'test/specs/indicator_detail_form.js',
            'test/specs/indicator_perf_metrics.js',
            'test/specs/indicators_landing_page.js',
            'test/specs/indicators_table.js',
            'test/specs/pct_indicators.js',
            'test/specs/sorting_indicators.js',
            'test/specs/target_actuals.js'
        ],
        evidence: [
            'test/specs/attach_evidence.js',
            'test/specs/collected_data_form.js',
            'test/specs/indicator_evidence_dropdown.js',
            'test/specs/indicator_evidence_table.js'
        ],
        reports: [
            'test/specs/export_reports.js',
            'test/specs/grid_report.js',
            'test/specs/prog_impact_assessment.js',
            'test/specs/prog_impact_overview.js'
        ]
    },
    // Capabilities
    maxInstances: 1,
    capabilities: [{
        // maxInstances can get overwritten per capability
        maxInstances: 1,
        browserName: 'chrome'
    },
    {
        maxInstances: 1,
        browserName: 'firefox'
    }],
    // Test Configurations
    sync: true,
    logLevel: 'verbose',
    logOutput: './log',
    coloredLogs: true,
    deprecationWarnings: true,
    bail: 0,
    screenshotPath: './errorShots/',
    baseUrl: 'http://localhost',
    waitforTimeout: 10000,
    connectionRetryTimeout: 90000,
    connectionRetryCount: 3,
    services: ['selenium-standalone'],
    seleniumLogs: './log',
    framework: 'mocha',
    reporters: ['spec', 'allure'],
    reporterOptions: {
        allure: {
            outputDir: './allure-results'
        }
    },
    mochaOpts: {
        ui: 'bdd',
        compilers: ['js:babel-register']
        //require: ['babel-register']
    },
    onComplete: function(exitCode, config, capabilities) {
        var proc = require('child_process');
        proc.execSync('/bin/rm -rfv /tmp/tats');
    }
}
