from conans import ConanFile, CMake, tools
import os

class TestPackageConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake", "cmake_find_package"

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def test(self):
        #assert os.path.isfile(os.path.join(self.deps_cpp_info["gtest"].rootpath, "licenses", "LICENSE"))
        if not tools.cross_building(self):
            self.run("test_package", run_environment=True)
