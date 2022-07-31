import numpy as np
import requests


def update_polls():
    urls = ['https://projects.fivethirtyeight.com/2022-general-election-forecast-data/senate_state_toplines_2022.csv',
            'https://projects.fivethirtyeight.com/2022-general-election-forecast-data/house_district_toplines_2022.csv',
            'https://projects.fivethirtyeight.com/2022-general-election-forecast-data/governor_state_toplines_2022.csv']
    file_names = ['538Senate.csv', '538House.csv', '538Governor.csv']

    for url, file in zip(urls, file_names):
        r = requests.get(url, allow_redirects=True)
        open(file, 'wb').write(r.content)


def get_poll_data(race_dict):
    """
    Gets Race Data from airtable
    Inputs
        - dict: format: 538 raceid : [Airtable name, 0]
    outputs
        - dict: format: 538 raceid : [Airtable name, chance of win]
    """
    return race_dict


if __name__ == '__main__':
    # comment out if you don't want new files
    update_polls()

    # Translations(Add more if needed)
    abbreviations = {'Kansas': 'KA', 'Michigan': 'MI', 'Wisconsin': 'WI', 'PA': 'PA'}

    races = np.loadtxt('Election_List.csv', delimiter=',', dtype='str')
    desired_races = {}
    # Translating into 538 Race Designators
    for race in races:
        if race.__contains__('Governor'):  # For Governor
            state = race.split(' ')[0]
            if abbreviations.keys().__contains__(state):
                updated_name = abbreviations[state] + '-G1'
                desired_races[updated_name] = [race, 0]
            else:
                print(state + ' Is not in the abbreviations list please add it')
        elif race.__contains__('U.S.'):  # For Nat. Senate
            updated_name = race.split(' ')[3] + '-S3'
            desired_races[updated_name] = [race, 0]
        elif len(race) == 5:  # For Nat. House
            updated_name = race[:3] + str(int(race[3:]))
            desired_races[updated_name] = [race, 0]

    print(desired_races)


