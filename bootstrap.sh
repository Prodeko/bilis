#!/usr/bin/env bash

sudo apt-get update
# Required for add-apt-repository
sudo apt-get install -y software-properties-common python-software-properties

# Add required repositories
# node.js
sudo add-apt-repository -y ppa:chris-lea/node.js >> /tmp/add-apt-errors 2>&1
# python3.3
sudo add-apt-repository -y ppa:fkrull/deadsnakes >> /tmp/add-apt-errors 2>&1

# download the package lists from the repositories
sudo apt-get update

# --- python ---

# install python3.3
sudo apt-get install -y python3.3

# set default python version to 3.3
sudo ln -sf /usr/bin/python3.3 /usr/bin/python
sudo dpkg --configure python
# install pip
sudo apt-get install -y python-pip

# --- miscellaneous ----

sudo apt-get install -y curl
sudo apt-get install -y git-core
sudo apt-get install -y screen

# --- apache ---

# install packages
sudo apt-get install -y apache2
sudo apt-get install -y libapache2-mod-rewrite
sudo apt-get install -y libapache2-mod-php5
sudo apt-get install -y libapache2-mod-wsgi

# remove default webroot
sudo rm -rf /var/www

# symlink project as webroot
sudo ln -fs /vagrant /var/www

# setup hosts file
VHOST=$(cat <<EOF
<VirtualHost *:80>
  DocumentRoot "/vagrant"
  ServerName localhost
  <Directory /vagrant>
    AllowOverride All
    Order Allow,Deny
    Allow From All
  </Directory>
</VirtualHost>
EOF
)
echo "${VHOST}" > /etc/apache2/sites-available/default

# enable apache rewrite module
sudo a2enmod rewrite




# --- mysql ---

# install packages
echo mysql-server mysql-server/root_password select "vagrant" | debconf-set-selections
echo mysql-server mysql-server/root_password_again select "vagrant" | debconf-set-selections
sudo apt-get install -y mysql-server-5.5

# create database
# mysql -uroot -pvagrant -e "CREATE DATABASE test;"


# --- node.js ---

# install node.js dependencies
sudo apt-get install -y g++ make

# install packages
sudo apt-get install -y nodejs


# --- Django ---

pip install Django
cd /vagrant && python manage.py syncdb


# --- restart apache ---

sudo service apache2 restart
