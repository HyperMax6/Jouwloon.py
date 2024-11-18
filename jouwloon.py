from bs4 import BeautifulSoup
import requests

headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'X-MicrosoftAjax': 'Delta=true',
    'X-Requested-With': 'XMLHttpRequest',
}

def jouwloonLogin(username, password):
    loginSession = requests.Session()

    login_url = "https://jouwloon.nl/Login.aspx"

    response = loginSession.get(login_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    viewstate = soup.find('input', {'name': '__VIEWSTATE'})['value']
    viewstate_generator = soup.find('input', {'name': '__VIEWSTATEGENERATOR'})['value']
    event_validation = soup.find('input', {'name': '__EVENTVALIDATION'})['value']

    payload = {
        'ctl00$scriptmanager': 'ctl00$ContentPlaceHolder1$UpdatePanel1|ctl00$ContentPlaceHolder1$Button_Inloggen',
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        '__VIEWSTATE': viewstate,
        '__VIEWSTATEGENERATOR': viewstate_generator,
        '__EVENTVALIDATION': event_validation,
        'ctl00$AppGebruiker': '',
        'ctl00$Versie': '',
        'ctl00$ContentPlaceHolder1$HiddenTaal': 'Nederlands',
        'ctl00$ContentPlaceHolder1$input_Gebruikersnaam': username,
        'ctl00$ContentPlaceHolder1$input_Wachtwoord': password,
        'ctl00$ContentPlaceHolder1$devtype': '0',
        'ctl00$ContentPlaceHolder1$devverz': '0',
        '__ASYNCPOST': 'true',
        'ctl00$ContentPlaceHolder1$Button_Inloggen': 'Inloggen'
    }

    loginSession.post(login_url, headers=headers, data=payload)
    return loginSession

def getCalendar(session, start, end):
    vestiging = session.get(url='https://jouwloon.nl/api/rooster/GetRoosterVestigingen', headers=headers).json()[0]
    klantenData = str([{"vestigingen": [{"vestId": vestiging['VestigingsID']}]}])

    calendar_url = 'https://jouwloon.nl/api/rooster/GetKalender'
    calendar_payload = {
        'klantenData': klantenData,
        'start': start,
        'end': end
    }

    jsonResponse = session.post(calendar_url, headers=headers, data=calendar_payload).json()
    shifts = {}

    for day in jsonResponse:
        print(day)
        roosterdienst = day['roosterdienst'][0]
        shifts[day['id']] = {
            'start': roosterdienst['vanafDatum'],
            'end': roosterdienst['totDatum'],
            'afdeling': roosterdienst['afdeling'],
            'vestiging': roosterdienst['vestiging']
        }

    return shifts