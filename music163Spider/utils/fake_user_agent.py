import json
import random
__author__ = 'harry yao'
__date__ = '2018/5/7 10:21'


class FakeUserAgent(object):

    def __init__(self):
        with open('/var/browsers.json') as file:
        # with open('browsers.json') as file:
            browser_json = json.load(file)
            self.browsers = browser_json['browsers']
            self.randomize = browser_json['randomize']

    def get_user_agent(self):
        name = self.randomize[str(random.randint(0, 984))]
        user_agent = random.sample(self.browsers[name], 1)
        return user_agent

if __name__ == '__main__':
    user_agent = FakeUserAgent()
    print(user_agent.get_user_agent())