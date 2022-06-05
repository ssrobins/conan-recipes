from conans import ConanFile, tools
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain

class Conan(ConanFile):
    name = "ssrobins_engine"
    version = "1.2.0"
    description = "Thin game engine wrapper"
    homepage = f"https://github.com/ssrobins/conan-{name}"
    license = "MIT"
    url = "https://github.com/ssrobins/conan-recipes"
    settings = "os", "arch", "compiler", "build_type"
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
        self.build_requires("cmake_utils/9.0.1")
        self.build_requires("gtest/1.11.0")

    def requirements(self):
        self.requires("sdl2/2.0.22")
        self.requires("sdl2_image/2.0.5")
        self.requires("sdl2_mixer/2.0.4")
        self.requires("sdl2_ttf/2.0.18")

    def layout(self):
        self.folders.build = "build"
        self.folders.generators = self.folders.build

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
        self.copy("*.h", dst="include", keep_path=False)
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)
        if self.settings.compiler == "msvc":
            self.copy("*.pdb", dst="lib", keep_path=False, excludes="*Test*")

    def package_info(self):
        if self.settings.build_type == "Debug":
            self.cpp_info.libs = ["Gamed", "Displayd", "ErrorHandlerd"]
        else:
            self.cpp_info.libs = ["Game", "Display", "ErrorHandler"]
