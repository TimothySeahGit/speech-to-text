#!/bin/sh

curl https://codeload.github.com/elastic/app-search-reference-ui-react/tar.gz/master | tar -xz
ls -la

cd app-search-reference-ui-react-master

apt-get -y update
apt-get install -y nodejs npm
npm -g i n
n 18
hash -r
node -v

# npm install --save-dev @babel/plugin-transform-private-property-in-object

npm -g i yarn

# rm package-lock.json

yarn add @elastic/search-ui-elasticsearch-connector

yarn

# copy App.js into app-search-reference-ui-react/src/
cp /usr/search-ui/App.js ./src/

yarn start