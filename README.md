#package scheduler
---

Allow students to schedule pick up times for the packages to ease congestion during peak hours.  
The idea is that a very clear visualization of the volume of traffic for each hour will encourage students to come to the package center at early and late hours.


##Configuration
---
The settings and configuration files for the flask app is located in the adi secrets repo.  
You should use a virtualenv and install the requirements to the environment.

    virtualenv --no-site-packages .
    pip install -r requirements.txt


##Resource
---
https://columbiauniversity.ikontrac.com/external/kiosks/mail/pickup/

##Package Center Meeting Notes 4/22
---

Timeline

* Completion by June 30th
* Heavy testing by July via dummy packages as they do for full mailboxes
* Rock solid before August 15th

Features to work on

* kiosk-like notification for reservations
* e-mail digest with UNIs
* visual scheme of hours
* flexibility to extend times and days (for peak package season)
* support for satellite locations (via e-mails?)
* perhaps "appointment tickets" to skip lines

Additional notes

* Consider methods for dealing with violations/no-shows
* Who should we bring in for front-end?
* Explore heat-map like visualizations using our data or the university's

