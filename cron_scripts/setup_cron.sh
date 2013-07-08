
crontab -l > mycron
echo "10,25,40,55 * * * * . ~/github/package_scheduler/cron_scripts/trigger_appointments.sh" >> mycron
crontab mycron
rm mycron

