""" Show class. Class contains all relevant show information stored in the xml database. Contains methods
for updating season number and next episode info, and printing show details """

import datetime


class Show:

    def __init__(self, show_id, network, title, time, day, overview, current_season=0, next_ep_no=0,
                 next_air_date='TBD', ep_title='TBD', ep_overview='TBD'):
        self.show_id = show_id
        self.network = network
        self.title = title
        self.time = time
        self.day = day
        self.overview = overview
        self.current_season = current_season
        self.next_ep_no = next_ep_no
        self.next_air_date = next_air_date
        self.ep_title = ep_title
        self.ep_overview = ep_overview

    def update(self, current_season, next_ep_no, next_air_date, ep_title, ep_overview):
        self.current_season = current_season
        self.next_ep_no = next_ep_no
        self.next_air_date = next_air_date
        self.ep_title = ep_title
        self.ep_overview = ep_overview

    def print_show(self):
        print(self.title)
        print(self.overview)
        print("Network:", self.network)
        print("Airs", self.time, "on", self.day)
        if self.next_air_date == 'TBD':
            print("Next Episode: Season", self.current_season, "Episode", self.next_ep_no, "Air date TBD")
            print(self.ep_title + ':', self.ep_overview)
        else:
            date = datetime.datetime.strptime(self.next_air_date, "%Y-%m-%d")
            air_date = date.strftime("%m-%d-%Y")
            if date >= datetime.datetime.today():
                print("Next Episode: Season", self.current_season, "Episode", self.next_ep_no, "Air date", air_date)
                print(self.ep_title + ':', self.ep_overview)
            else:
                print("Last Episode: Season", self.current_season, "Episode", self.next_ep_no, "Air date", air_date)
                print(self.ep_title + ':', self.ep_overview)


