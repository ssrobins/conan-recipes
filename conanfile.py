from conans import ConanFile, CMake
from cmake_utils import cmake_init, cmake_build_debug_release

class Conan(ConanFile):
    name = "ssrobins_engine"
    version = "0.1.0"
    description = "Thin game engine wrapper"
    homepage = "https://gitlab.com/ssrobins/conan-" + name
    license = "MIT"
    url = "https://gitlab.com/ssrobins/conan-" + name
    settings = "os", "compiler", "arch"
    generators = "cmake"
    revision_mode = "scm"
    exports = "cmake_utils.py"
    exports_sources = [
        "CMakeLists.txt",
        "global_settings.cmake",
        "Android/*",
        "cmake/*",
        "Display/*",
        "DisplayTest/*",
        "ErrorHandler/*",
        "Game/*"
    ]
    build_subfolder = "build"

    def build_requirements(self):
        self.build_requires.add("gtest/1.8.1#0ab3cafdcd7fe85deaefe41b3011d36fbd86e38e")

    def requirements(self):
        self.requires.add("sdl2/2.0.8#4841c177e6f3920faa36e56495bfcd23f55d1d1e")
        self.requires.add("sdl2_image/2.0.5#d05b5cff4d08b2726485af58b25217dd4fca0668")
        self.requires.add("sdl2_ttf/2.0.15#55cd97129e10c9f54ff98e3896df593c333881ae")

    def build(self):
        cmake = cmake_init(self.settings, CMake(self), self.build_folder)
        cmake_build_debug_release(cmake, self.build_subfolder, self.run)

    def package(self):
        self.copy("*.h", dst="include", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)
        self.copy("build/lib/*.a", dst="lib", keep_path=False)
        if self.settings.compiler == "Visual Studio":
            self.copy("*.pdb", dst="lib", keep_path=False)
        if self.settings.os == "Android":
            self.copy("Android/*")
        self.copy("cmake/*")

    def package_info(self):
        self.cpp_info.debug.libs = ["Gamed", "Displayd", "ErrorHandlerd"]
        self.cpp_info.release.libs = ["Game", "Display", "ErrorHandler"]
