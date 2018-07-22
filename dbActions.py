""" Methods for reading and writing to the database and creating instances of Show with the proper parameters """
import Show
import xml.etree.ElementTree as xml


def get_shows():
    """ reads xml database and creates an instance of each show, returns a list of all shows """
    shows = []
    tree = xml.parse('shows.xml')
    root = tree.getroot()
    for show in root:
        show_id = show.find('show_id').text
        network = show.find('network').text
        title = show.find('title').text
        time = show.find('time').text
        day = show.find('day').text
        current_season = show.find('current_season').text
        next_ep_no = show.find('next_ep_no').text
        next_air_date = show.find('next_air_date').text
        shows.append(Show.Show(show_id, network, title, time, day, current_season,
                               next_ep_no, next_air_date))
    return shows


def write_to_db(shows_list):
    """ takes the list of shows and writes it to the database """
    filename = 'shows.xml'
    root = xml.Element('Shows')
    for show in shows_list:
        showElement = xml.Element("Show")
        root.append(showElement)
        show_id = xml.SubElement(showElement, 'show_id')
        network = xml.SubElement(showElement, 'network')
        title = xml.SubElement(showElement, "title")
        time = xml.SubElement(showElement, "time")
        day = xml.SubElement(showElement, "day")
        current_season = xml.SubElement(showElement, "current_season")
        next_ep_no = xml.SubElement(showElement, "next_ep_no")
        next_air_date = xml.SubElement(showElement, "next_air_date")
        show_id.text = str(show.show_id)
        network.text = show.network
        title.text = show.title
        time.text = show.time
        day.text = show.day
        current_season.text = str(show.current_season)
        next_ep_no.text = str(show.next_ep_no)
        next_air_date.text = show.next_air_date
    tree = xml.ElementTree(root)
    with open(filename, "wb") as fh:
        tree.write(fh)
