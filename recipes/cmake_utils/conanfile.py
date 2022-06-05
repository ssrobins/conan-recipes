from conans import ConanFile

class Conan(ConanFile):
    name = "cmake_utils"
    version = "9.0.1"
    description = "Shared CMake utilities"
    license = "MIT"
    url = "https://github.com/ssrobins/conan-recipes"
    revision_mode = "scm"
    exports_sources = "*"

    def package(self):
        self.copy("*.cmake")
        self.copy("*.in")
        self.copy("*.plist")
        self.copy("*.xcsettings")
