
import base64
import requests



def main():
    data = {
        'method': 'GET',
        'url': 'https://www.google.com/',
        'headers': dict(),
        'data': '',
        'other': dict()
    }
    response = requests.post('https://requests-url.abasthan.app/url', json=data).json()
    print(base64.b64decode(response['response']['body'].encode()).decode())


if __name__ == '__main__':
    main()
