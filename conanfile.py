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
        self.build_requires("cmake_utils/0.3.1#217df94bdd79aaa9b2aec1a8bd8b4eca73411f25")
        self.build_requires("gtest/1.10.0#af5a75e307b6039ab662434cb838441f1342fb51")

    def requirements(self):
        self.requires("sdl2/2.0.8#b16a079e0dd4a2a068a287212aaf9ec0cfaa1fa0")
        self.requires("sdl2_image/2.0.5#5f88748804f984c2827a78502850ae808dcd801a")
        self.requires("sdl2_ttf/2.0.15#0a9c42d9afe2523e1af87256a8d55eb917b6bac9")

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
