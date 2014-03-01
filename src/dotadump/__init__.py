import json
import os

with open(os.path.dirname(__file__) + '../../config/master.json') as fp:
  config = json.load(fp)

