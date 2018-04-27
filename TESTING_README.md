# Unit Testing

There have been some changes to the unit test harness to make the process more
closely reflect the CI and Production environments.

The unittests should no longer use sqlite3 with an in memory DB. It should be using
a mysql database.


One of the funnest changes has been the inclution of test coverage reports. Each
devleoper can create them locally from the command line with a couple of simple
steps.

Typically when running the django unittest suite from the command line we run

% python manage.py test

With optional module names if we want to focus our efforts on a particular test or
subset of all tests.

If you would like to generate coverage reports locally you will need to install the
python coverage module http://coverage.readthedocs.io/en/coverage-4.5.1/install.html

This readme will go over installing on linux for other opperating systems please
see the documention linked above. If you are really having trouble you can contact
sparky at davila@mercycorps.org OR my personal email sparkytwobillion@gmail.com.

I will provide what support I can.

From the linux commandline installing the coverage module is pretty simple

% pip install coverage

And that should do it!

Using it from the commandline is just as simple.

% coverage run manage.py test; coverage html;

The tests will take slightly longer to run because the coverage module is gathering
information on what lines of code are exersised in our codebase and generating an html
report that you can view in your web browser.

After running the coverage command you will notice there is a new directory
named coverage_html.

You can navigate to it in your webbrowser.