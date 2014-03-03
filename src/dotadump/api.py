import requests
from time import sleep
from dotadump import config
from itertools import izip, product, repeat, chain


ROOT = "https://api.steampowered.com/IDOTA2Match_570"


def decorate(url):
  return url + '/V001'


MAX_MATCHES = 500


def matches(**kwargs):
  kwargs.setdefault('matches_requested', MAX_MATCHES / 20)
  kwargs = dict(kwargs, key=config['API_KEY'])
  results_remaining = 1
  while results_remaining:
    result = requests.get(decorate(ROOT + '/GetMatchHistory'), params=kwargs).json()['result']
    print 'got a result with %s matches' % len(result['matches'])
    results_remaining = result['results_remaining']
    for match in result['matches']:
      yield match
    kwargs['start_at_match_id'] = match['match_id'] - 1


def add_new_matches(seen, **kwargs):
  new = []
  for match in matches(**kwargs):
    id_ = match['match_id']
    if id_ in seen:
      break
    seen[id_] = match
    new.append(match)

  return new


def infinite_matches(interval=10, factor=1.5, lower=50., upper=10., **kwargs):
  seen = dict()

  while True:
    new = add_new_matches(seen, **kwargs)
    for match in new:
      yield match

    print 'Seen %s new since last query.' % len(new)

    if len(new) < MAX_MATCHES / lower:
      interval *= factor
    if len(new) >= MAX_MATCHES / upper:
      interval /= factor

    print 'Sleeping', interval
    sleep(interval)


def details(match_id, **kwargs):
  kwargs = dict(kwargs, key=config['API_KEY'])
  return requests.get(
    decorate(ROOT + '/GetMatchDetails'),
    params=dict(kwargs, match_id=match_id)
  ).json()['result']


def infinite_matches_with(**param_possibilities):
  streams = []
  keys, possible_values = izip(*param_possibilities.iteritems())
  for param_values in product(*possible_values):
    params = dict(izip(keys, param_values))
    print "Adding stream with ", params
    streams.append(izip(repeat(params),
                        infinite_matches(**params)))

  print streams

  for params, match in chain.from_iterable(izip(*streams)):
    yield params, match
