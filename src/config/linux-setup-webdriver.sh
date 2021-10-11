#!/bin/bash

# # update google chrome browser to latest version
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
sh -c 'echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
apt-get update
apt-get --only-upgrade install google-chrome-stable
# # get chrome webdriver based on installed chrome version
CHROME_VERSION=`google-chrome --version | grep -Eo "[0-9.]{10,20}"`
echo "System using version $CHROME_VERSION of google-chrome"
CHROME_VERSION_FIRST_DIGITS="${CHROME_VERSION:0:2}"
echo $CHROME_VERSION_FIRST_DIGITS
wget "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_VERSION_FIRST_DIGITS"
CHROME_WEBDRIVER_LATEST_RELEASE_VERSION=`(cat LATEST_RELEASE_$CHROME_VERSION_FIRST_DIGITS)`
wget "https://chromedriver.storage.googleapis.com/${CHROME_WEBDRIVER_LATEST_RELEASE_VERSION}/chromedriver_linux64.zip"
rm LATEST_RELEASE_$CHROME_VERSION_FIRST_DIGITS
unzip chromedriver_linux64.zip
# # set chromedriver to path, add permission and make it executable
mv chromedriver /usr/bin/chromedriver
chown root:root /usr/bin/chromedriver
sudo chmod +x /usr/bin/chromedriver
rm chromedriver_linux64.zip