from itertools import izip, product, repeat, chain
from time import sleep
from logging import getLogger

import requests

from dotadump import config


log = getLogger(__name__)


ROOT = "https://api.steampowered.com/IDOTA2Match_570"
MAX_MATCHES = 500


def decorate(url):
  return url + '/V001'


def matches(**kwargs):
  kwargs.setdefault('matches_requested', MAX_MATCHES)
  kwargs = dict(kwargs, key=config['API_KEY'])
  results_remaining = 1
  while results_remaining:
    result = requests.get(decorate(ROOT + '/GetMatchHistory'), params=kwargs).json()['result']
    log.debug('Got a result with %s matches', len(result['matches']))
    results_remaining = result['results_remaining']
    for match in result['matches']:
      yield match
    kwargs['start_at_match_id'] = match['match_id'] - 1


def add_new_matches(seen, **kwargs):
  for match in matches(**kwargs):
    id_ = match['match_id']
    if id_ in seen:
      continue
    seen.add(id_)
    yield match


def infinite_matches(interval=10, factor=1.5, max_wait=100, lower=50., upper=10., **kwargs):
  seen = set()

  while True:
    new = list(add_new_matches(seen, **kwargs))
    log.debug('Seen %s new since last query.', len(new))
    yield new

    if len(new) < MAX_MATCHES / lower:
      interval *= factor
      interval = min(interval, max_wait)
    if len(new) >= MAX_MATCHES / upper:
      interval /= factor

    log.debug('Sleeping for %s', interval)
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
    log.debug("Adding stream with %s", params)
    streams.append(izip(repeat(params),
                        infinite_matches(**params)))

  for params, matches in chain.from_iterable(izip(*streams)):
    for match in matches:
      yield params, match
