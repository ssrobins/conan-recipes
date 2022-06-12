from conan import ConanFile
from conan.tools.files import copy

required_conan_version = ">=1.47.0"

class Conan(ConanFile):
    name = "cmake_utils"
    version = "10.0.0"
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
