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

###Additional Features

* kiosk-like notification for reservations
* e-mail digest with UNIs
* visual scheme of hours
* flexibility to extend times and days (for peak package season)
* support for satellite locations (via e-mails?)
* perhaps "appointment tickets" (from email) to skip lines
* admin page for package center manager to set allocation

Additional notes

* Consider methods for dealing with violations/no-shows

