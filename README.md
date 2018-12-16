# pythontvtracker

Gets show info from TheTVDB api. 
Create a file, 'shows.xml', to store show info.
Create a file, 'credentials.xml', to store api and email credentials:

'''xml
<credentials>
    <username>Your tvdb username</username>
    <userkey>Your tvdb userkey</userkey>
    <apikey>Your tvdb api key</apikey>
    <email>From email</email>
    <password>From email password</password>
    <emailto>To email</emailto>
</credentials>
'''

Run 'python3 main.py' to launch command line interface. CLI allows you to add and remove shows, and view show info.

Run 'python3 send_email.py' to update info and email reminders when 
new episodes are airing. Emails will be sent the day before and day the new episode 
airs. 
Create a cron job to run everyday at a given time.
