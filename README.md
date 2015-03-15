## bs

This AI client uses the [bottle web framework](http://bottlepy.org/docs/dev/index.html) for route management and response building, and the [gunicorn web server](http://gunicorn.org/) for running bottle on Heroku.

Dependencies are listed in [requirements.txt](requirements.txt).

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)

### Running the AI locally

Clone this repo

Create new virtualenv (using virtualenvwrapper) and install dependencies:
```
> mkvirtualenv battlesnake-python
> workon battlesnake-python
> pip install -r requirements.txt
```

Run the server locally:
```
> ./run
Bottle v0.12.8 server starting up (using WSGIRefServer())...
Listening on http://localhost:8080/
Hit Ctrl-C to quit.
```

Test client in your browser: [http://localhost:8080](http://localhost:8080)

### Deploying to Heroku

Create a new Heroku app:
```
heroku create [APP_NAME]
```

Push code to Heroku servers:
```
git push heroku master
```

Open Heroku app in browser.
```
heroku open
```

Or go directly to: [http://APP_NAME.herokuapp.com](http://APP_NAME.herokuapp.com)

You can also view liveserver logs with the heroku logs command:
```
heroku logs --tail
```
