./reset_db.sh; ./manage.py syncdb --migrate --noinput;
./manage.py customer_connetcion_event_fill;
./run.sh