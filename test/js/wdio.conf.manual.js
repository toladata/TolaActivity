exports.config = {
    specs: [
        './test/specs/**/*.js'
    ],
    exclude: [
        // 'path/to/excluded/files'
    ],
    // Capabilities
    maxInstances: 3,
    capabilities: [{
        // maxInstances can get overwritten per capability
        maxInstances: 2,
        browserName: 'firefox'
    }],
    sync: true,
    logLevel: 'silent',
    coloredLogs: true,
    deprecationWarnings: true,
    bail: 0,
    screenshotPath: './errorShots/',
    baseUrl: 'http://localhost',
    waitforTimeout: 10000,
    connectionRetryTimeout: 90000,
    connectionRetryCount: 3,
    services: [],
    seleniumLogs: './logs',
    framework: 'mocha',
    reporters: ['spec'],
    mochaOpts: {
        ui: 'bdd',
        compilers: ['js:babel-register']
        //require: 'babel-register'
    }
}
