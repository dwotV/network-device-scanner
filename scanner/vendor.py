import requests

def get_vendor(mac):
    try:
        url = f'https://api.macvendors.com/{mac}'
        answered = requests.get(url)
        if answered.status_code == 200:
            return answered.text
        else:
            return 'Unknown'
    except:
        return 'Error to connect to the macvendors API'
