#!/bin/sh
# 1. Initiate a migration folder using init command for alembic to perform the migrations.
# Use this for first time only
 python manage.py db init
# 2. Create a migration script from the detected changes in the model using the migrate command. This doesn’t affect the database yet.
echo Type message wo write with migration
read message
python manage.py db migrate --message "$message"

# 3. Apply the migration script to the database by using the upgrade command
python manage.py db upgrade
