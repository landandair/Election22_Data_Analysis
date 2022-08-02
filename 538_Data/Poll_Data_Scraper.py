import numpy as np
import requests

FILE_NAMES = ['538Senate.csv', '538House.csv', '538Governor.csv']
OTHER_DATA = 'district_data.csv'

def update_polls():
    """Downloads fresh versions of all the csv files"""
    urls = ['https://projects.fivethirtyeight.com/2022-general-election-forecast-data/senate_state_toplines_2022.csv',
            'https://projects.fivethirtyeight.com/2022-general-election-forecast-data/house_district_toplines_2022.csv',
            'https://projects.fivethirtyeight.com/2022-general-election-forecast-data/governor_state_toplines_2022.csv']
    district = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vSBwdz78YjgsG_QccV_WvPb55xRHzK07mfPnLowjcS9r_lRgcQZS3OHONRHE0PeVbZwlFVjoHMiJ2Ju/pub?gid=211606255&single=true&output=csv'
    # 538 Data
    for url, file in zip(urls, FILE_NAMES):
        r = requests.get(url, allow_redirects=True)
        open(file, 'wb').write(r.content)
    # Other Data importing
    r = requests.get(district, allow_redirects=True)
    open(OTHER_DATA, 'wb').write(r.content)


def get_poll_data(race_dict):
    """
    Searches through files for the desired p.win for Legislative elections
    Inputs
        - dict: format: 538 raceid : [Airtable name, 0]
    outputs
        - dict: format: 538 raceid : [Airtable name, chance of win]
    """
    # National Elections
    for file in FILE_NAMES:
        time_check = np.loadtxt(file, delimiter=',', dtype='str', usecols=3)
        check = time_check[1]
        number = len(check)
        for i, line in enumerate(time_check[1:]):
            if line != check:
                print('Now Searching-' + file + ': ' + check)
                number = i+1
                break
        data_dict = dict(np.loadtxt(file, delimiter=',', dtype='str', usecols=[2, 25])[:number])
        keys = data_dict.keys()
        for race in race_dict.keys():
            if race in keys:
                race_dict[race][1] = data_dict[race]

    # Local Elections
    print('Now Searching-' + OTHER_DATA)
    data_dict = dict(np.loadtxt(OTHER_DATA, delimiter=',', dtype='str', usecols=[1, 12]))
    keys = data_dict.keys()
    for race in race_dict.keys():
        if race in keys:
            race_dict[race][1] = data_dict[race]

    return race_dict


if __name__ == '__main__':
    # comment out if you don't want new files
    print('getting fresh data')
    update_polls()

    # Translations(Add more if needed) needed for governors
    abbreviations = {'Kansas': 'KS', 'Michigan': 'MI', 'Wisconsin': 'WI', 'PA': 'PA'}

    district_trans = {'Senate': 'u', 'House': 'l'}

    election_file = 'Election_List.csv'
    races = np.loadtxt(election_file, delimiter=',', dtype='str', usecols=0)[1:]
    desired_races = {}
    # Translating into 538 Race Designators
    for race in races:
        if race.__contains__('Governor') and len(race.split(' ')) == 2:  # For Governor
            state = race.split(' ')[0]
            if abbreviations.keys().__contains__(state):
                print(state)
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
        elif len(race.split(' ')) == 3 and district_trans.keys().__contains__(race.split(' ')[1]):  # For District Races
            race_split = race.split(' ')
            updated_name = race_split[0].lower()+district_trans[race_split[1]]+race_split[2].strip('D')
            desired_races[updated_name] = [race, -1]
    # Get Data From Files
    print('searching for data from files')
    desired_races = get_poll_data(desired_races)
    print(desired_races)
    desired_races = dict(desired_races.values())
    ret = []
    for race in races:
        if race in desired_races.keys():
            ret.append(desired_races[race])
        else:
            ret.append('')
    races = list(races)
    races.insert(0, 'Office Name')
    ret.insert(0, 'Polls')
    data = np.array(list(zip(races, ret)))
    print('Saving Data')
    np.savetxt(election_file, data, delimiter=',', fmt='%s')
    print('done')



