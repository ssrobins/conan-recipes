from conan import ConanFile
from conan.tools.files import copy

class Conan(ConanFile):
    name = "android_sdl2"
    version = "2.6.2"
    description = "Android Gradle project for SDL2"
    license = "MIT"
    url = "https://github.com/ssrobins/conan-recipes"
    revision_mode = "scm"
    exports_sources = "*"

    def package(self):
        copy(self, "Android/*", self.source_folder, self.package_folder)

    def package_info(self):
        self.cpp_info.includedirs = list()
