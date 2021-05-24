import sys

import requests
from bs4 import BeautifulSoup


class User:

    def __init__(self, name):
        self.name = name
        self.info = {'name': self.name}
        self.parseUser()

    def get_followers(user):
        return user.info['followers_count']

    def get_repo_count(user):
        return user.info['repo_count']

    def parseUser(self):
        self.parse_repos()
        self.parse_repo_count()
        self.parse_followers_and_bio()

    def parse_followers_and_bio(self):
        response = requests.get('https://api.github.com/users/' + self.name,
                                headers={"Accept": "application/vnd.github.v3+json"}).json()
        self.info['followers_count'] = int(response.get('followers'))
        self.info['description'] = response.get('bio')

    def parse_repo_count(self):
        self.info['repo_count'] = len(self.info['repo_lang'])

    def parse_repos(self):
        response = requests.get(self.get_url_for_user('repos'))
        soup = BeautifulSoup(response.text, 'lxml')

        try:
            self.info['repo_lang'] = result = {}
            repos = soup.findAll('a', {'itemprop': "name codeRepository"})
            langs = soup.findAll('span', {'itemprop': "programmingLanguage"})
            for repo, lang in zip(repos, langs):
                result[repo.get_text().replace('\n', ' ').strip()] = lang.get_text().replace('\n', ' ').strip()

            self.info['lang_to_count'] = lang_to_count = {}
            for repo, lang in result.items():
                lang_to_count[lang] = len(list(
                    filter(lambda x: result[x] == lang, result)
                ))
            return repos, lang_to_count

        except Exception:
            return None

    def get_url_for_user(self, type):
        if type == 'user':
            return 'https://github.com/' + self.name
        if type == 'repos':
            return 'https://github.com/' + self.name + '?tab=repositories'
        if type == 'followers':
            return 'https://api.github.com/users/' + self.name + '/followers'

    def pretty_print_info(self):
        print('= ' * 20)
        print(f'name: {self.info["name"]}')
        print(f'description: {self.info["description"]}')
        for lang, count in self.info['lang_to_count'].items():
            print(f'lang: {lang}, in {count} repo')


class GitHubParser:
    def __init__(self, users):
        self.users = []
        print('wait a minute...')
        i = 0
        for user in users:
            i += 1
            print(f'{i}/{len(users)} users parsed..')
            self.users.append(User(user))
        self.print_info()
        self.run()

    def print_info(self):
        print('*' * 10, 'Info', '*' * 10)
        max_repos = max(
            self.users, key=User.get_repo_count
        )
        print(f'Max repos: {max_repos.info["name"]}, count: {max_repos.info["repo_count"]}')

        print('Language rating:')
        langs = {}
        for user in self.users:
            for lang, count in user.info['lang_to_count'].items():
                if lang not in langs:
                    langs[lang] = count
                else:
                    langs[lang] += count
        _sorted = dict(sorted(langs.items(), key=lambda item: item[1], reverse=True))
        i = 0
        for lang, count in _sorted.items():
            i += 1
            print(f'{i}: {lang}: {count}')

        max_followers = max(
            self.users, key=User.get_followers
        )
        print(f'Max followers: {max_followers.info["name"]}, count: {max_followers.info["followers_count"]}')
        print(' -' * 20)

    def run(self):
        names = list(map(lambda x: x.info["name"], self.users))
        while True:
            print()
            print('Enter username')
            print(f'Available: {names}')
            print('To exit enter "0"')
            user = input()
            print()

            if user == '0':
                break
            if user in names:
                list(filter(lambda x: x.info['name'] == user, self.users))[0].pretty_print_info()


GitHubParser(sys.argv[1:])

# example run script parameters: torvalds gvanrossum poettering dhh moxie0 fabpot brendangregg bcantrill antirez
# python main.py torvalds gvanrossum poettering dhh moxie0 fabpot brendangregg bcantrill antirez
