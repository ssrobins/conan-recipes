from conans import ConanFile, CMake

class Conan(ConanFile):
    name = "ssrobins_engine"
    version = "0.3.0"
    description = "Thin game engine wrapper"
    homepage = f"https://github.com/ssrobins/conan-{name}"
    license = "MIT"
    url = f"https://github.com/ssrobins/conan-{name}"
    settings = "os", "compiler", "arch"
    generators = "cmake"
    revision_mode = "scm"
    exports_sources = [
        "CMakeLists.txt",
        "Display/*",
        "DisplayTest/*",
        "ErrorHandler/*",
        "Game/*"
    ]
    build_subfolder = "build"

    def build_requirements(self):
        self.build_requires("cmake_utils/0.3.1#a1d53d179d9736ff032b5f5de3e4c3e2eebcb1f0")
        self.build_requires("gtest/1.11.0#42289b3e08c69030c7f755a4d49d0b0b4d78103e")

    def requirements(self):
        self.requires("sdl2/2.0.16#d64fb9b295748eeef2db30c50a8aa6d3f948f770")
        self.requires("sdl2_image/2.0.5#22cbb9c463ce625b4c878532fd4d19e66e6442ad")
        self.requires("sdl2_ttf/2.0.15#bfda6aa5591c9a6b8dfeb88a8147f539e087ce48")

    def build(self):
        from cmake_utils import cmake_init, cmake_build_debug_release
        cmake = cmake_init(self.settings, CMake(self), self.build_folder)
        cmake_build_debug_release(cmake, self.build_subfolder, self.run)

    def package(self):
        self.copy("*.h", dst="include", keep_path=False)
        self.copy("*.lib", dst="lib", src=self.build_subfolder, keep_path=False)
        self.copy("build/lib/*.a", dst="lib", keep_path=False)
        if self.settings.compiler == "Visual Studio":
            self.copy("*.pdb", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.debug.libs = ["Gamed", "Displayd", "ErrorHandlerd"]
        self.cpp_info.release.libs = ["Game", "Display", "ErrorHandler"]
