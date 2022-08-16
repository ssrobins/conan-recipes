from conan import ConanFile
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain
from conan.tools.files import copy, get
import os

required_conan_version = ">=2.0.0-beta1"

class Conan(ConanFile):
    name = "gtest"
    version = "1.12.1"
    description = "Google's C++ test framework"
    homepage = "https://github.com/google/googletest"
    license = "BSD-3-Clause"
    url = "https://github.com/ssrobins/conan-recipes"
    settings = "os", "arch", "compiler", "build_type"
    generators = "CMakeDeps"
    revision_mode = "scm"
    exports_sources = ["CMakeLists.txt"]
    zip_folder_name = f"googletest-release-{version}"
    zip_name = f"release-{version}.tar.gz"

    @property
    def _source_subfolder(self):
        return "source"

    def layout(self):
        self.folders.build = "build"
        self.folders.generators = self.folders.build

    def source(self):
        get(self,
            f"https://github.com/google/googletest/archive/{self.zip_name}",
            destination=self._source_subfolder,
            strip_root=True)

    def generate(self):
        tc = CMakeToolchain(self)
        if self.settings.os != "Windows":
            tc.generator = "Ninja Multi-Config"
        tc.variables["CMAKE_VERBOSE_MAKEFILE"] = "TRUE"
        if self.settings.os == "iOS":
            tc.variables["CMAKE_SYSTEM_NAME"] = "iOS"
            if self.settings.arch != "x86_64":
                tc.blocks["apple_system"].values["cmake_osx_architectures"] = "armv7;arm64"
        tc.generate()
        deps = CMakeDeps(self)
        deps.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
        self.run(f"ctest -C {self.settings.build_type} --output-on-failure")

    def package(self):
        copy(self, "*.h",
            os.path.join(self.source_folder, self._source_subfolder, "googletest", "include", "gtest"),
            os.path.join(self.package_folder, "include", "gtest"))
        copy(self, "*.h",
            os.path.join(self.source_folder, self._source_subfolder, "googlemock", "include", "gmock"),
            os.path.join(self.package_folder, "include", "gmock"))
        copy(self, "*.lib",
            self.build_folder,
            os.path.join(self.package_folder, "lib"),
            keep_path=False)
        copy(self, "*.a",
            self.build_folder,
            os.path.join(self.package_folder, "lib"),
            keep_path=False)
        if self.settings.compiler == "msvc":
            copy(self, "*.pdb",
                self.build_folder,
                os.path.join(self.package_folder, "lib"),
                keep_path=False)

    def package_info(self):
        if self.settings.build_type == "Debug":
            self.cpp_info.libs = ["gmock_maind", "gmockd", "gtest_maind", "gtestd"]
        else:
            self.cpp_info.libs = ["gmock_main", "gmock", "gtest_main", "gtest"]
        if self.settings.os == "Linux":
            self.cpp_info.system_libs.append("pthread")
