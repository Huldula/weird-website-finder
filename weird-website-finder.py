import argparse
import requests
import re

try:
    from googlesearch import search
except ImportError:
    print("No module named 'google' found")

parser = argparse.ArgumentParser(description='Find some weird websites.')
parser.add_argument('--count', '-c', type=int, default=10, help='number google searches')
# parser.add_argument('--lang', '-l', type=str, default='en', help="google search language (default: 'en')")
parser.add_argument('--combine', '-C', type=int, default=2,
                    help="number of words combined in one google search (default: 2)")
parser.add_argument('--sites', '-s', type=int, default=1,
                    help="number of displayed websites per google search")
parser.add_argument('--filterboring', '-f', nargs='?', const=True, type=bool, default=False,
                    help='filters out many known websites (after google search so the number of outputs may change)')
parser.add_argument('--domainonly', '-d', nargs='?', const=True, type=bool, default=False,
                    help='only shows the domain, not the path afterwards')
args = parser.parse_args()

key = 'PUHIP1I2'
url = f'https://random-word-api.herokuapp.com/word?key={key}&number={args.count * args.combine}'
res = requests.get(url=url)
words = res.json()

if len(words[0]) is 0:
    print('you need to get a new api key at: https://random-word-api.herokuapp.com/key?')
    exit(1)

boring = [
    'amazon',
    'youtube',
    'wikipedia',
    'facebook',
    'twitter',
    'instagram',
    'tumblr',
    'ifunny',
    'soundcloud',
    'github',
    'dailymail',
    'shutterstock',
    'reddit',
    'wikihow',
    'duckduckgo'
]

for i in range(args.count):
    query = ''
    for j in range(args.combine):
        query += f' {words[i * args.combine + j]}'
    for result in search(query, num=args.sites, stop=args.sites, pause=1):
        printing = True
        if args.filterboring:
            for b in boring:
                if b in result:
                    printing = False
                    break
        if args.domainonly:
            result = re.search('https?://([^/])+', result)[0]
        if printing:
            print(f'{result} results from{query}')
