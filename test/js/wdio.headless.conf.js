exports.config = {
    specs: [
        './test/specs/**/*.js'
    ],
    exclude: [
        // 'path/to/excluded/files'
    ],
    suites: {
        login: [
            'test/specs/login.js',
            'test/specs/password_invalid.js',
            'test/specs/username_invalid.js'
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
    // Capabilities - can override per-capability
    maxInstances: 1,
    capabilities: [
        {
            browserName: 'chrome',
            maxInstances: 1,
            chromeOptions: {
                args: ['--headless']
            }
        }
    ],
    sync: true,
    logLevel: 'verbose',
    logOutput: './log',
    coloredLogs: true,
    deprecationWarnings: false,
    bail: 0,
    screenshotPath: './errorShots/',
    baseUrl: 'http://localhost',
    waitforTimeout: 10000,
    connectionRetryTimeout: 90000,
    connectionRetryCount: 3,
    services: [],
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
        //require: 'babel-register'
    }
}
