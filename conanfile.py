from conans import ConanFile, CMake

class Conan(ConanFile):
    name = "ssrobins_engine"
    version = "1.1.0"
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
        self.build_requires("cmake_utils/5.0.0#1ecfed8c68a43ea17d321701cc8a91df21d06453")
        self.build_requires("gtest/1.11.0#7a8dc4022cf1753b71057bfe89043cf4a5b4dc8f")

    def requirements(self):
        self.requires("sdl2/2.0.18#1b637c42e56a9747a74c2bdeb53370c0cd24c414")
        self.requires("sdl2_image/2.0.5#a5bb813d197df422cc8d9034adfc7a866f47b42d")
        self.requires("sdl2_ttf/2.0.15#d5f3a47390d23aba76e992030674d316479acfa7")

    def build(self):
        from cmake_utils import cmake_init, cmake_build_debug_release
        cmake = cmake_init(self.settings, CMake(self), self.build_folder)
        cmake_build_debug_release(cmake, self.build_subfolder, self.run)

    def package(self):
        self.copy("*.h", dst="include", keep_path=False)
        self.copy("*.lib", dst="lib", src=self.build_subfolder, keep_path=False)
        self.copy("build/lib/*.a", dst="lib", keep_path=False)
        if self.settings.compiler == "msvc":
            self.copy("*.pdb", dst="lib", keep_path=False, excludes="*Test*")

    def package_info(self):
        self.cpp_info.debug.libs = ["Gamed", "Displayd", "ErrorHandlerd"]
        self.cpp_info.release.libs = ["Game", "Display", "ErrorHandler"]
