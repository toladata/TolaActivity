#!/bin/bash
# move this file to your project (tola_activity) root directory
# download a backup file and modify the ~/dumps/ to point to that backup
mysql -utola_activity -p tola_activity < ~/dumps/tola_activity_backup.sql
mysql --user="root" --password="drummer01" --database="tola_activity" --execute="RENAME TABLE tola_activity.activitydb_formguidance TO tola_activity.workflow_formguidance;"
git pull origin new_dev
python manage.py runscript workflow_migration
python manage.py migrate —fake
