#! /bin/bash

#cd frontend

#npm run build

#cd ..

#cd frontend_stag

#npm run build

#cd ..

heroku container:login

heroku container:push web --app bloomingmath

heroku container:release web --app bloomingmath
