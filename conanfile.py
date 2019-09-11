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

    def requirements(self):
        self.requires.add("gtest/1.8.1#7290c5c2f56f845c053796c515eae62956c61e74")
        self.requires.add("sdl2/2.0.8#69c21e066605654a91aa48560889ada1b5e3913a")
        self.requires.add("sdl2_image/2.0.5#03753c7b4b3044db39bcbf8eb1bc16be526c4f56")
        self.requires.add("sdl2_ttf/2.0.15#8920c84a7a6a178446780d03cb1fe0dce3928468")

    def build(self):
        cmake = cmake_init(self.settings, CMake(self), self.build_folder)
        cmake_build_debug_release(cmake, self.build_subfolder, self.run)

    def package(self):
        self.copy("*.h", dst="include", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)
        self.copy("*.lib", dst="lib", keep_path=False)
        if self.settings.compiler == "Visual Studio":
            self.copy("*.pdb", dst="lib", keep_path=False)
        if self.settings.os == "Android":
            self.copy("Android/*")
        self.copy("cmake/*")

    def package_info(self):
        self.cpp_info.debug.libs = ["Gamed", "Displayd", "ErrorHandlerd"]
        self.cpp_info.release.libs = ["Game", "Display", "ErrorHandler"]
