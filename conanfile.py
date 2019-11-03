from conans import ConanFile

class Conan(ConanFile):
    name = "android_sdl2"
    version = "0.1.0"
    description = "Android Gradle project for SDL2"
    license = "MIT"
    url = "https://gitlab.com/ssrobins/conan-" + name
    revision_mode = "scm"
    exports = "*"
    build_policy = "missing"

    def package(self):
        self.copy("Android/*")
