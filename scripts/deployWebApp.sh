#!/bin/bash

# Change to your Angular app directory
cd /home/workspace/Software-Engineering-Project-Course/src

# Build the Angular app for production
ng build --configuration=production

# Assuming you have named your PM2 process 'angular-app', if not change accordingly
pm2 restart all

# Restart Nginx
systemctl restart nginx.service

