exports.config = {
    specs: [
        './test/specs/**/*.js'
    ],
    exclude: [
        // 'path/to/excluded/files'
    ],
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
