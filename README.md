# Event Radar 

A basic Python app useful for looking up public events on Eventbrite. Uses the Eventbrite Python API to search for an event and the Sendgrid API to send an email when events are detected. Requires accounts and API tokens at Eventbrite and Sendgrid.

Combines well with Heroku Scheduler to regularly run the app and be notified when a particular event is listed.

## Deploying to Heroku

```
$ heroku create
$ git push heroku master

$ heroku run python manage.py migrate
$ heroku open
```

## Documentation

For more information about using Python on Heroku, see these Dev Center articles:

- [Python on Heroku](https://devcenter.heroku.com/categories/python)
