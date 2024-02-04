import requests

class Gurushots:
    def __init__(self):
        self.member_id = None
        self.token = None
        self.get_tokens()

    def get_tokens(self):
        url = "https://api.gurushots.com/rest/signin"

        payload = 'login=potatotraveler&password=lPxRwZ15pnNNo%24n'
        headers = {
            'authority': 'api.gurushots.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'no-cache',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://gurushots.com',
            'pragma': 'no-cache',
            'referer': 'https://gurushots.com/',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Microsoft Edge";v="120"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
            'x-api-version': '13',
            'x-env': 'WEB',
            'x-requested-with': 'XMLHttpRequest'
        }
        
        response = requests.request("POST", url, headers=headers, data=payload)
        self.token = response.json()['token']
        self.member_id = response.json()['member_id']

    def get_photos(self):
        url = "https://api.gurushots.com/rest/get_photos_public"

        payload = f"get_achievements=true&get_liked=true&get_likes=true&get_member=true&get_votes=true&limit=40&member_id={self.member_id}&order=date&search=&sort=desc&start=0&type=photos"
        headers = {
            'authority': 'api.gurushots.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'no-cache',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://gurushots.com',
            'pragma': 'no-cache',
            'referer': 'https://gurushots.com/',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Microsoft Edge";v="120"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
            'x-api-version': '13',
            'x-env': 'WEB',
            'x-requested-with': 'XMLHttpRequest',
            'x-token': self.token
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.json())


if __name__ == "__main__":
    gs = Gurushots()
    gs.get_photos()