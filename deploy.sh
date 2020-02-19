#! /bin/bash

cd frontend

cp public/index.production.html public/index.html

npm run build

cp public/index.development.html public/index.html

cd ..

heroku container:login

heroku container:push web --app bloomingmath

heroku container:release web --app bloomingmath
