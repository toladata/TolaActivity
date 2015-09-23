#!/bin/bash
# init
function pause(){
   read -p "$*"
}

cd ../

git remote update
changed=1
git pull --dry-run | grep -q -v 'Already up-to-date.' && changed=0

if [ $changed == 0 ]
then
    passed=0
    echo "Changes detected running test"
    git pull origin dev
    cd htdocs
    sudo py manage.py test --settings tola.settings.test | grep -q -v 'OK' && passed=0
    if [ $passed == 1 ]
    then
        echo "Test Failed"
        "Subject: Unit tests failed on [$hostname] for Tola-Activity" | /usr/sbin/sendmail glind@mercycorps.org, mkhan@mercycorps.org
    else
        echo "All Tests Passed"
    fi
else
    echo "No changes detected"
    cd htdocs
fi

echo "Running Migrations..."
sudo py manage.py migrate

cd ../deploy_scripts

echo "Would you like to empty the mail Queue (y/n)?"
read e
if [[ $e == "y" || $e == "Y" ]]; then
	sudo postsuper -d ALL
fi

echo "Done"
