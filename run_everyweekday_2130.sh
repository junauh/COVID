#!/bin/bash

source /usr/local/anaconda3/etc/profile.d/conda.sh
conda activate volvo_social_datawarehouse
echo "test"
which python
cd /Users/junyoung.auh/Desktop/Corona
python EndofDayIndex.py
python Covid-19.py

# run to open the crontab file in Nano: export EDITOR=nano crontab -e
# to save and close: Ctrl-X
# You’ll see the “crontab: installing new crontab” message, indicating that your new crontab file was installed successfully.
# check what crontabs are currently running on your system run : crontab -l