# pythontvtracker

Gets show info from TheTVDB api. 
Create a file, 'shows.xml', to store show info.
Create a file, 'credentials.xml', to store api and email credentials:

&lt;credentials&gt;
    &lt;username&gt;Your tvdb username&lt;/username&gt;
    &lt;userkey&gt;Your tvdb userkey&lt;/userkey&gt;
    &lt;apikey&gt;Your tvdb api key&lt;/apikey&gt;
    &lt;email&gt;From email&lt;/email&gt;
    &lt;password&gt;From email password&lt;/password&gt;
    &lt;emailto&gt;To email&lt;/emailto&gt;
&lt;/credentials&gt;

Run 'python3 main.py' to launch command line interface. CLI allows you to add and remove shows, and view show info.

Run 'python3 send_email.py' to update info and email reminders when 
new episodes are airing. Emails will be sent the day before and day the new episode 
airs. 
Create a cron job to run everyday at a given time.
