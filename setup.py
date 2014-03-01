#!/usr/bin/env python

import os
import setuptools

# Don't install deps for development mode.
setuptools.bootstrap_install_from = None

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, "README.txt")).read()

setuptools.setup(
  name = 'dotastatistics',
  version = '0.0.1',
  platforms = 'any',

  description = README,

  # What are we packaging up?
  package_dir = {'': 'src'},
  packages = setuptools.find_packages('src'),
  include_package_data = True,

  scripts = [],
  data_files = [
    ('configs', [])
  ],

  zip_safe = False,
  verbose = False,
)
