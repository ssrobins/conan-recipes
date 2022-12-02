from conan import ConanFile
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain
from conan.tools.files import copy
import os

required_conan_version = ">=2.0.0-beta1"

class Conan(ConanFile):
    name = "ssrobins_engine"
    version = "2.0.7"
    description = "Thin game engine wrapper"
    homepage = "https://github.com/ssrobins/conan-recipes"
    license = "MIT"
    url = "https://github.com/ssrobins/conan-recipes"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "iwyu": [True, False]
    }
    default_options = {
        "iwyu": False
    }
    generators = "CMakeDeps"
    revision_mode = "scm"
    exports_sources = [
        "CMakeLists.txt",
        "Display/*",
        "DisplayTest/*",
        "ErrorHandler/*",
        "Game/*"
    ]

    def build_requirements(self):
        self.test_requires("gtest/1.12.1@ssrobins")

    def requirements(self):
        self.requires("cmake_utils/12.0.1@ssrobins")
        self.requires("sdl/2.26.1@ssrobins")
        self.requires("sdl_image/2.6.2@ssrobins")
        self.requires("sdl_mixer/2.6.2@ssrobins")
        self.requires("sdl_ttf/2.20.1@ssrobins")

    @property
    def _source_subfolder(self):
        return "source"

    def layout(self):
        self.folders.build = "build"
        self.folders.generators = self.folders.build

    def generate(self):
        tc = CMakeToolchain(self)
        if self.settings.os != "Windows":
            tc.generator = "Ninja Multi-Config"
        if not self.options.iwyu:
            tc.variables["CMAKE_VERBOSE_MAKEFILE"] = "TRUE"
        if self.settings.os == "iOS":
            tc.variables["CMAKE_SYSTEM_NAME"] = "iOS"
            if self.settings.arch != "x86_64" and not self.options.iwyu:
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
            os.path.join(self.source_folder),
            os.path.join(self.package_folder, "include"),
            keep_path=False)
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
                keep_path=False,
                excludes="*Test*")

    def package_info(self):
        if self.settings.build_type == "Debug":
            self.cpp_info.libs = ["Gamed", "Displayd", "ErrorHandlerd"]
        else:
            self.cpp_info.libs = ["Game", "Display", "ErrorHandler"]
