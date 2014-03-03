import requests
from dotadump import config


ROOT = "https://api.steampowered.com/IDOTA2Match_570"


def decorate(url):
  return url + '/V001'


def matches(**kwargs):
  kwargs = dict(kwargs, key=config['API_KEY'])
  results_remaining = 1
  while results_remaining:
    result = requests.get(decorate(ROOT + '/GetMatchHistory'), params=kwargs).json()
    results_remaining = result['results_remaining']
    for match in result['matches']:
      yield match
    kwargs['start_at_match_id'] = match['match_id'] - 1


def details(match_id, **kwargs):
  kwargs = dict(kwargs, key=config['API_KEY'])
  return requests.get(decorate(ROOT + '/GetMatchDetails'),
                      params=dict(kwargs, match_id=match_id)).json()
