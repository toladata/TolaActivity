.DEFAULT: help

help:
	@echo "allure    : generates Allure HTML output from ./allure-results"
	@echo "clean     : remove all logs and generated files except test results"
	@echo "doc       : (re)generate test suite documentation"
	@echo "help      : show this help message"
	@echo "install   : install all the bits needed to run tests"
	@echo "update    : refresh packages in top-level package.json file"
	@echo "update-all: refresh all packages in node_modules"


allure: ./allure-results
	@./node_modules/.bin/allure generate ./allure-results --clean


clean:
	@rm -fvr allure-report doc errorShots logs node_modules *server.log


doc:
	@./node_modules/.bin/jsdoc --verbose \
		--package package.json \
		--recurse \
		--destination doc \
		--readme README.md \
		test/lib test/pages -R README.md


install:
	@npm install --verbose --save-dev


report: allure


update:
	@npm update --dev --save
