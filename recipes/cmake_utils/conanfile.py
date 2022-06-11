from conan import ConanFile
from conan.tools.files import copy
import os.path
import sys
sys.path.append(f"{os.path.dirname(os.path.realpath(__file__))}/../../scripts")
from conan_common import *

class Conan(ConanFile):
    name = "cmake_utils"
    version = "9.0.1"
    description = "Shared CMake utilities"
    license = "MIT"
    url = "https://github.com/ssrobins/conan-recipes"
    revision_mode = "scm"
    exports_sources = "*"

    def package(self):
        copy(self, "*.cmake", self.source_folder, self.package_folder)
        copy(self, "*.in", self.source_folder, self.package_folder)
        copy(self, "*.plist", self.source_folder, self.package_folder)
        copy(self, "*.xcsettings", self.source_folder, self.package_folder)

    def package_info(self):
        self.cpp_info.includedirs = list()
