# python script to manage postgresql backups

** 1) Install required python modules**
pip install -r requirements.pip

** 2) Configure md5 authentication in postgresql **

** 3) Set password for the postgres user account"
alter user postgres with password 'your_password';

** 4) Copy env.sample to .env and set the Db and backup variables correctly

** 5) Run python script. Best to schedule with cron **
python backup.py