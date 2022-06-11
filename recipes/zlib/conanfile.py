from conan import ConanFile
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain
from conan.tools.files import copy, get
import os.path
import sys
sys.path.append(f"{os.path.dirname(os.path.realpath(__file__))}/../../scripts")
from conan_common import *

class Conan(ConanFile):
    name = "zlib"
    version = "1.2.12"
    description = "A Massively Spiffy Yet Delicately Unobtrusive Compression Library " \
                  "(Also Free, Not to Mention Unencumbered by Patents)"
    homepage = "https://zlib.net/"
    license = "Zlib"
    url = "https://github.com/ssrobins/conan-recipes"
    settings = "os", "arch", "compiler", "build_type"
    generators = "CMakeDeps"
    revision_mode = "scm"
    exports_sources = ["CMakeLists.diff", "CMakeLists.txt"]
    zip_folder_name = f"{name}-{version}"
    zip_name = f"{zip_folder_name}.tar.gz"

    def requirements(self):
        self.requires("cmake_utils/9.0.1")

    @property
    def _source_subfolder(self):
        return "source"

    def layout(self):
        self.folders.build = "build"
        self.folders.generators = self.folders.build

    def source(self):
        get(self,
            f"https://zlib.net/{self.zip_name}",
            sha256="91844808532e5ce316b3c010929493c0244f3d37593afd6de04f71821d5136d9",
            destination=self._source_subfolder,
            strip_root=True)

    def generate(self):
        tc = CMakeToolchain(self)
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
            os.path.join(self.source_folder, self._source_subfolder),
            os.path.join(self.package_folder, "include"))
        copy(self, "*.h",
            self.build_folder,
            os.path.join(self.package_folder, "include"),
            keep_path=False)
        copy(self, "*zlibstatic*.lib",
            self.build_folder,
            os.path.join(self.package_folder, "lib"),
            keep_path=False)
        copy(self, "*.a",
            self.build_folder,
            os.path.join(self.package_folder, "lib"),
            keep_path=False)
        if self.settings.compiler == "msvc":
            copy(self, "*zlibstatic*.pdb",
                self.build_folder,
                os.path.join(self.package_folder, "lib"),
                keep_path=False)

    def package_info(self):
        if self.settings.os == "Windows":
            if self.settings.build_type == "Debug":
                self.cpp_info.libs = ["zlibstaticd"]
            else:
                self.cpp_info.libs = ["zlibstatic"]
        else:
            if self.settings.build_type == "Debug":
                self.cpp_info.libs = ["zd"]
            else:
                self.cpp_info.libs = ["z"]
