#!/usr/bin/env python3

import os.path
import sys
sys.path.append(f"{os.path.dirname(os.path.realpath(__file__))}/../../scripts")
from conan_create import *
conan_create(os.path.dirname(os.path.realpath(__file__)))
