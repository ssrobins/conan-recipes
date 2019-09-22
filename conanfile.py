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
        self.build_requires.add("gtest/1.8.1#87754ca5593a1001e629122ee514d931aa9e8bf7")

    def requirements(self):
        self.requires.add("sdl2/2.0.8#e119e81196414d99c32c6ef72a8c2624b9408171")
        self.requires.add("sdl2_image/2.0.5#28bc0d22f59f05d2ceb9f33d8946d6309a9bfd61")
        self.requires.add("sdl2_ttf/2.0.15#6ba50e9a3e553b257e48ed24c2fc7023c090b980")

    def build(self):
        cmake = cmake_init(self.settings, CMake(self), self.build_folder)
        cmake_build_debug_release(cmake, self.build_subfolder, self.run)

    def package(self):
        self.copy("*.h", dst="include", keep_path=False)
        self.copy("*.lib", dst="lib", src=self.build_subfolder, keep_path=False)
        self.copy("build/lib/*.a", dst="lib", keep_path=False)
        if self.settings.compiler == "Visual Studio":
            self.copy("*.pdb", dst="lib", keep_path=False)
        if self.settings.os == "Android":
            self.copy("Android/*")
        self.copy("cmake/*")

    def package_info(self):
        self.cpp_info.debug.libs = ["Gamed", "Displayd", "ErrorHandlerd"]
        self.cpp_info.release.libs = ["Game", "Display", "ErrorHandler"]
