from conans import ConanFile

class Conan(ConanFile):
    name = "android_sdl2"
    version = "2.6.2"
    description = "Android Gradle project for SDL2"
    license = "MIT"
    url = "https://github.com/ssrobins/conan-recipes"
    revision_mode = "scm"
    exports = "*"
    build_policy = "missing"

    def package(self):
        self.copy("Android/*")
