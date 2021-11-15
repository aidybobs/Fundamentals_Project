#!/bin/bash
sudo apt install python3 python3-pip python3-venv -y
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
while getopts "c" options; do
  case ${options} in
    c) create=true;;
  esac
done
if [ ${create} ]; then
  python3 create.py
fi

echo 'TESTING:'
<<<<<<< HEAD
python3 -m pytest tests.py --cov --cov-report
=======
python3 -m pytest tests.py --cov --cov-report html
>>>>>>> 267dbaafe015f12ee5e2c846053c0d4d9ba49251

python3 app.py


