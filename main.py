""" Main program CLI. Prints menu and allows user to view/add/remove shows """

import db_actions
import web_scraper


shows = []
has_shows = False
menuLoop = True
login_success = False
token = ''


def main_loop():
    """ gets theTVDB API login credentials, list of shows, and handles user input """
    global shows
    global has_shows
    if not has_shows:
        try:
            shows = db_actions.get_shows()
            has_shows = True
        except:
            has_shows = False
    global token
    global login_success
    try:
        token = 'Bearer ' + web_scraper.login()
        login_success = True
    except:
        login_success = False
    print_menu()
    choice = input('Enter choice: ').upper()
    if choice == 'A':
        if has_shows:
            choice_a()
        else:
            print("You don't have any shows yet!")
    elif choice == 'B':
        if has_shows:
            choice_b()
        else:
            print("You don't have any shows yet!")
    elif choice == 'C':
        choice_c()
    elif choice == 'D':
        if has_shows:
            choice_d()
        else:
            print("You don't have any shows yet!")
    elif choice == 'E':
        if has_shows:
            for show in shows:
                web_scraper.get_episodes(token, show.show_id)
    elif choice == 'F':
        if has_shows:
            db_actions.write_to_db(shows)
            exit(1)


def print_menu():
    print(10 * '-', 'Tv Tracker', 10 * '-')
    print('A: List shows')
    print('B: Show info')
    print('C: Find new show')
    print('D: Remove show')
    print("E: Update Episode Info")
    print('F: Quit')
    print(32 * '-')


def choice_a():
    """ prints show titles in numbered list """
    print()
    print("Shows:")
    for show in shows:
        print(shows.index(show) + 1, show.title)
    print()


def choice_b():
    """ shows details of a particular show """
    get_details = int(input('Enter show number to see details: '))
    print()
    if get_details > len(shows):
        print('Invalid choice')
    else:
        shows[get_details - 1].print_show()
    print()


def choice_c():
    """ lets user search for and add new shows to track """
    if login_success:
        try:
            search = input('Enter title to find: ')
            s = web_scraper.search(token, search)
            exists = False
            for show in shows:
                if show.title == s.title:
                    exists = True
                    break
            if not exists:
                tmp = web_scraper.get_episodes(token, s.show_id)
                s.update(tmp['current_season'], tmp['next_ep_no'], tmp['next_air_date'], tmp['ep_title'], tmp['ep_overview'])
                shows.append(s)
                global has_shows
                has_shows = True
            else:
                print("You're already tracking that show")
        except:
            print("Show not found")
    else:
        print('API login failed, check credentials')


def choice_d():
    """ removes show """
    remove = int(input('Select show to remove: '))
    for show in shows:
        if shows[remove - 1].show_id == show.show_id:
            shows.remove(show)


def start_main():
    while menuLoop:
        main_loop()


start_main()












