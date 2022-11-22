from conan import ConanFile
from conan.tools.files import copy

required_conan_version = ">=2.0.0-beta1"

class Conan(ConanFile):
    name = "android_sdl"
    version = "2.7.0"
    description = "Android Gradle project for SDL2"
    license = "MIT"
    url = "https://github.com/ssrobins/conan-recipes"
    exports_sources = "*"

    def package(self):
        copy(self, "Android/*", self.source_folder, self.package_folder)

    def package_info(self):
        self.cpp_info.includedirs = list()
