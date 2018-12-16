""" Gets show and episode info from theTVDB API """
import requests
import json
import Show
import xml.etree.ElementTree as xml
import datetime


def login():
    """ API returns authentication token after first login, good for 24 hours. Gets token """
    tree = xml.parse('credentials.xml')
    root = tree.getroot()
    apikey = root.find('apikey').text
    userkey = root.find('userkey').text
    username = root.find('username').text
    url = 'https://api.thetvdb.com/login'
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    auth = {"apikey": apikey, "userkey": userkey, "username": username}
    r = requests.post(url, headers=headers, data=json.dumps(auth))
    json_data = json.loads(r.text)
    token = json_data.get('token')
    return token


def search(token, query):
    """ searches shows based on user query, only returns shows that have status continuing
    so there will be new episodes eventually. Gets show id and call create_show """
    format_query = query.replace(" ", "%20")
    url = 'https://api.thetvdb.com/search/series?name=' + format_query
    headers = {'Accept': 'application/json', 'Authorization': token}
    r = requests.get(url, headers=headers)
    json_data = json.loads(r.text)
    show_list = json_data.get('data')
    for show in show_list:
        if show.get('status') == 'Continuing':
            show_id = show.get('id')
            s = create_show(token, show_id)
            return s


def create_show(token, show_id):
    """ gets show details - title, network, air day and time """
    url = 'https://api.thetvdb.com/series/' + str(show_id)
    headers = {'Accept': 'application/json', 'Authorization': token}
    r = requests.get(url, headers=headers)
    json_data = json.loads(r.text).get('data')
    network = json_data.get('network')
    title = json_data.get('seriesName')
    time = json_data.get('airsTime')
    day = json_data.get('airsDayOfWeek')
    overview = json_data.get('overview')
    s = Show.Show(show_id, network, title, time, day, overview)
    return s


def get_episodes(token, show_id):
    """ API returns paginated list of episodes, not always in order. calls get_season_no to get highest season number per
     page. After finding the most recent season, we can get just those episodes from API and more easily find the next episode """
    page = 1
    url = 'https://api.thetvdb.com/series/' + str(show_id) + '/episodes?page=' + str(page)
    headers = {'Accept': 'application/json', 'Authorization': token}
    r = requests.get(url, headers=headers)
    json_data = json.loads(r.text).get('links')
    first = json_data.get('first')
    last = json_data.get('last')
    no_of_seasons = 1
    if last > first:
        for p in range(1, last + 1):
            url = 'https://api.thetvdb.com/series/' + str(show_id) + '/episodes?page=' + str(p)
            s = get_season_no(token, url)
            if s > no_of_seasons:
                no_of_seasons = s
    else:
        url = 'https://api.thetvdb.com/series/' + str(show_id) + '/episodes?page=' + str(1)
        s = get_season_no(token, url)
        if s > no_of_seasons:
            no_of_seasons = s
    url = 'https://api.thetvdb.com/series/' + str(show_id) + '/episodes/query?airedSeason='
    update_details = get_episode_details(token, url, no_of_seasons)
    return update_details


def get_season_no(token, url):
    """ find the highest season number per page of episodes """
    headers = {'Accept': 'application/json', 'Authorization': token}
    r = requests.get(url, headers=headers)
    json_data = json.loads(r.text).get('data')
    high_season = 1
    for episode in json_data:
        if episode.get('airedSeason') > high_season:
            high_season = episode.get('airedSeason')
    return high_season


def get_episode_details(token, url, season):
    """ gets episodes from most recent season, goes through and stops when it finds the first episode airing
    on the current day or later. Returns season, episode number, and air date of episode """
    u = url + str(season)
    headers = {'Accept': 'application/json', 'Authorization': token}
    r = requests.get(u, headers=headers)
    json_data = json.loads(r.text).get('data')
    season_details = {}
    season_details['current_season'] = season
    if len(json_data) > 1:
        for episode in json_data:
            d = episode.get('firstAired')
            date = datetime.datetime.strptime(d, "%Y-%m-%d")
            today = datetime.datetime.today()
            if date.date() >= today.date():
                season_details['next_ep_no'] = episode.get('airedEpisodeNumber')
                season_details['next_air_date'] = episode.get('firstAired')
                season_details['ep_title'] = episode.get('episodeName')
                season_details['ep_overview'] = episode.get('overview')
                break
            else:
                season_details['next_ep_no'] = (json_data[len(json_data) - 1].get('airedEpisodeNumber'))
                season_details['next_air_date'] = (json_data[len(json_data) - 1].get('firstAired'))
                season_details['ep_title'] = (json_data[len(json_data) - 1].get('episodeName'))
                season_details['ep_overview'] = (json_data[len(json_data) - 1].get('overview'))
    else:
        season_details['next_ep_no'] = 1
        season_details['next_air_date'] = (json_data[0].get('firstAired'))
        season_details['ep_title'] = (json_data[0].get('episodeName'))
        season_details['ep_overview'] = (json_data[0].get('overview'))
    if season_details['next_air_date'] == "":
        season_details['next_air_date'] = 'TBD'
    if season_details['ep_title'] == "" or season_details['ep_title'] is None:
        season_details['ep_title'] = 'TBD'
    if season_details['ep_overview'] == "" or season_details['ep_overview'] is None:
        season_details['ep_overview'] = 'TBD'
    return season_details






