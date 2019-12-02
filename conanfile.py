from conans import ConanFile

class Conan(ConanFile):
    name = "cmake_utils"
    version = "0.2.0"
    description = "Shared CMake utilities"
    license = "MIT"
    url = "https://gitlab.com/ssrobins/conan-" + name
    revision_mode = "scm"
    exports = "*"
    build_policy = "missing"

    def package(self):
        self.copy("*.cmake")
        self.copy("*.in")
        self.copy("*.plist")
        self.copy("*.py")

    def package_info(self):
        self.env_info.PYTHONPATH.append(self.package_folder)
