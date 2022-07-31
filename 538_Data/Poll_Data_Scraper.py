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


if __name__ == '__main__':
    update_polls()
    races = np.loadtxt('', delimiter=',', dtype='str')
    desired_races = []
