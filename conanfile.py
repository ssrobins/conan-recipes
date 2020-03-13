from conans import ConanFile, CMake

class Conan(ConanFile):
    name = "ssrobins_engine"
    version = "0.2.0"
    description = "Thin game engine wrapper"
    homepage = f"https://gitlab.com/ssrobins/conan-{name}"
    license = "MIT"
    url = f"https://gitlab.com/ssrobins/conan-{name}"
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
        self.build_requires("cmake_utils/0.3.1#7b308615a235fdf046db096dd35325c0375c2f88")
        self.build_requires("gtest/1.10.0#fbedb03a0bb64f1df48a54f4394eab3978d6ffb3")

    def requirements(self):
        self.requires("sdl2/2.0.8#60fdb231f6e74bb622017585003a2c09c82d8b35")
        self.requires("sdl2_image/2.0.5#e97a7893d36ca838dc81ae576ab8fabf910cbd5e")
        self.requires("sdl2_ttf/2.0.15#1327baf47d262805ffbfee02cb55e22909ad654d")

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
