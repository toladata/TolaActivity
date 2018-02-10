.default: help

help:
	@echo "clean: remove all logs and generated files"
	@echo "update: refresh packages in top-level package.json file"
	@echo "update-all: refresh all packages in node_modules"
	@echo "doc: (re)generate test suite documentation"

install:
	@npm install --verbose

update:
	@npm update --dev --save

update-all:
	@cd node_modules && npm update --dev --save && cd ..

clean:
	@rm -fvr doc errorShots node_modules selenium-server.log 

server:
	@java -jar \
		-Dwebdriver.chrome.driver=./chromedriver \
		selenium-server-standalone-3.8.1.jar &> server.log &

test:
	@./node_modules/.bin/wdio wdio.conf.js

doc:
	@./node_modules/.bin/jsdoc --verbose \
		--package package.json \
		--recurse \
		--destination doc \
		--readme README.md \
		test/lib test/pages -R README.md
