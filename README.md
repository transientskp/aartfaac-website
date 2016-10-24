# aartfaac-website

This is the aartfaac website running on http://www.aartfaac.org.


# usage

first install docker and docker compose

https://docs.docker.com/compose/install/

then run:
```
$ docker-compose build
$ docker-compose up
```

This should start a webserver running on port 80 serving the aartfaac
website.

the first time you start this website you need to create the content of
the database. you can do this with:
```
$ docker-compose run django python ./manage.py migrate --settings website.settings.ais001
```

Next you need to initialise a super user:
```
$ docker-compose run django python ./manage.py createsuperuser --settings website.settings.ais001
Username (leave blank to use 'root'):
```

You can use this created user/password combination to login to the
admin section (probably something like `http://localhost/admin`) and
create more users or do other funky admin things.
