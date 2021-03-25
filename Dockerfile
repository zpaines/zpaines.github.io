FROM python:3

WORKDIR /usr/src/app

WORKDIR /usr/src/app/fantasy_basketball
CMD [ "git", "status" ]
