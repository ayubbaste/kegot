#!/bin/bash

# way to bot project folder
cd ~/www/kegot
source env/bin/activate

# launch the script and wait till it'll be finish
python kegot.py &
BACK_PID=$!
wait $BACK_PID

deactivate

# make it executable with command at server
# chmod +x starter.sh
# 'crontab -e' task example (start every 15 min):
# */15 * * * * ~/www/kegot/starter.sh

