#!/bin/bash

project_path="github/package_scheduler"
cd $project_path

source "bin/activate"
source "config/settings.local.prod"

python trigger_appointments.py

