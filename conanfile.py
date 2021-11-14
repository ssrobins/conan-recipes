from conans import ConanFile

class Conan(ConanFile):
    name = "android_sdl2"
    version = "1.0.0"
    description = "Android Gradle project for SDL2"
    license = "MIT"
    url = f"https://github.com/ssrobins/conan-{name}"
    revision_mode = "scm"
    exports = "*"
    build_policy = "missing"

    def package(self):
        self.copy("Android/*")
