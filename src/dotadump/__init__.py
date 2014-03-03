import json
import os

with open(os.path.join(os.path.dirname(__file__),
                       '../../configs/master.json')) as fp:
  config = json.load(fp)
