import os
import sys
import sendgrid
from sendgrid.helpers.mail import *
from sendgrid import *
from dateutil import parser
from eventbrite import Eventbrite

# Settings
from_email = Email("noreply@example.com")
to_email   = Email("my_email_address@example.com")

search_term     = 'event name' # The event name or keyword to search for
search_location = '00000'      # Replace with zip code or postal code
search_radius   = '20km'       # The search radius around the location to search for listed events

EVENTBRITE_TOKEN = 'MY_EVENTBRITE_TOKEN'
SENDGRID_API_KEY = 'MY_SENDGRID_API_KEY'

# No need to edit below this line
eventbrite = Eventbrite(EVENTBRITE_TOKEN)
sg = sendgrid.SendGridAPIClient(apikey=SENDGRID_API_KEY)

# Alternatively, use a stored environment variable
#sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))

# Get a raw list of events (includes pagination details)
results = eventbrite.event_search(**{'q': search_term,\
                                     'location.address': search_location,\
                                     'location.within': search_radius})

# See what attributes you can pass to the event_search method at
# https://www.eventbrite.com/developer/v3/endpoints/events/#ebapi-get-events-search
#
# Eventbrite SDK for Python
# http://eventbrite-sdk-python.readthedocs.io/en/latest/cookbook.html

# Perform a search. If nothing found, exit.
try:
    events = results['events']
except:
    sys.exit(results)

start_time_fmt = '%A, %d %B %Y, %I:%M %p'
end_time_fmt = '%I:%M %p'

# For every event matching the search query, send an email notification
for event in events:
    name = event['name']['text']
    description = event['description']['html']
    start_time = parser.parse(event['start']['local'])
    end_time = parser.parse(event['end']['local'])
    url = event['url']
    print name
    print 'Date & Time: {0} to {1}'.format(start_time.strftime(start_time_fmt), end_time.strftime(end_time_fmt))
    print 'URL: {0}'.format(url)

    # Prepare email
    subject = "New {0} Event Detected.".format(search_term)
    body    = u'<html><body><h4>{0}</h4>\n'.format(name) + \
              u'Date & Time: {0} to {1}'.format(start_time.strftime(start_time_fmt), end_time.strftime(end_time_fmt)) + \
              u'<p><a href="{0}">{0}</a></p>'.format(url) + \
              u'<p>{0}</p>'.format(description) + \
              u'</body></html>'
    content = Content("text/html", body)
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)

