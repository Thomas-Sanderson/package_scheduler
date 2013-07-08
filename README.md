#package scheduler

Allow students to schedule pick up times for the packages to ease congestion during peak hours.  
The idea is that a very clear visualization of the volume of traffic for each hour will encourage students to come to the package center at early and late hours.

##Configuration

The settings and configuration files for the flask app is located in the adi secrets repo.  
You should use a virtualenv and install the requirements to the environment.  
Add the database settings to the environment.
You'll have to set up the paths in the cron related scripts to match those of you own configuration.

    virtualenv --no-site-packages .
    source bin/activate
    pip install -r requirements.txt
    cron_scripts/setup_cron.sh
    source config/settings.packages.prod

