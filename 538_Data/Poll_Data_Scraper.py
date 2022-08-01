import numpy as np
import requests

FILE_NAMES = ['538Senate.csv', '538House.csv', '538Governor.csv']

def update_polls():
    urls = ['https://projects.fivethirtyeight.com/2022-general-election-forecast-data/senate_state_toplines_2022.csv',
            'https://projects.fivethirtyeight.com/2022-general-election-forecast-data/house_district_toplines_2022.csv',
            'https://projects.fivethirtyeight.com/2022-general-election-forecast-data/governor_state_toplines_2022.csv']
    for url, file in zip(urls, FILE_NAMES):
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

    for file in FILE_NAMES:
        time_check = np.loadtxt(file, delimiter=',', dtype='str', usecols=3)
        check = time_check[1]
        number = len(check)
        for i, line in enumerate(time_check[1:]):
            if line != check:
                print(line)
                number = i+1
                break
        data_dict = dict(np.loadtxt(file, delimiter=',', dtype='str', usecols=[2, 25])[:number])
        keys = data_dict.keys()
        for race in race_dict.keys():
            if race in keys:
                race_dict[race][1] = data_dict[race]
    return race_dict


if __name__ == '__main__':
    # comment out if you don't want new files
    update_polls()

    # Translations(Add more if needed)
    abbreviations = {'Kansas': 'KS', 'Michigan': 'MI', 'Wisconsin': 'WI', 'PA': 'PA'}

    election_file = 'Election_List.csv'
    races = np.loadtxt(election_file, delimiter=',', dtype='str', usecols=0)
    desired_races = {}
    # Translating into 538 Race Designators
    for race in races:
        if race.__contains__('Governor'):  # For Governor
            state = race.split(' ')[0]
            if abbreviations.keys().__contains__(state):
                updated_name = abbreviations[state] + '-G1'
                desired_races[updated_name] = [race, -1]
            else:
                print(state + ' Is not in the abbreviations list please add it')
        elif race.__contains__('U.S.'):  # For Nat. Senate
            updated_name = race.split(' ')[3] + '-S3'
            desired_races[updated_name] = [race, -1]
        elif len(race) == 5:  # For Nat. House
            updated_name = race[:3] + str(int(race[3:]))
            desired_races[updated_name] = [race, -1]
    # Get Data From Files
    desired_races = get_poll_data(desired_races)

    desired_races = dict(desired_races.values())
    ret = []
    for race in races:
        if race in desired_races.keys():
            ret.append(desired_races[race])
        else:
            ret.append('')
    ret = (np.array(ret))
    data = np.array(list(zip(list(races), list(ret))))
    np.savetxt(election_file, data, delimiter=',', fmt='%s')



