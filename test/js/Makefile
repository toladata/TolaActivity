.DEFAULT: help

help:
	@echo "clean: remove all logs and generated files"
	@echo "update: refresh packages in top-level package.json file"
	@echo "update-all: refresh all packages in node_modules"
	@echo "doc: (re)generate test suite documentation"

install:
	@npm install --verbose

update:
	@npm update --dev --save

clean:
	@rm -fvr doc errorShots logs node_modules

doc:
	@./node_modules/.bin/jsdoc --verbose \
		--package package.json \
		--recurse \
		--destination doc \
		--readme README.md \
		test/lib test/pages -R README.md
