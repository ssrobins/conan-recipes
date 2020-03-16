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
        self.build_requires("cmake_utils/0.3.1#d093c585be2418d6a664babbec39e71d6b5cd11d")
        self.build_requires("gtest/1.10.0#1dc34103486deb0c4056a3326c005456f805fc6b")

    def requirements(self):
        self.requires("sdl2/2.0.8#ecad87bc0bf63f851560e29d3b2e0d1881051544")
        self.requires("sdl2_image/2.0.5#b30afe725bb6b53b7ba3230c75a2ed93fe261591")
        self.requires("sdl2_ttf/2.0.15#5553982e10122a4940ad92341b2d5e6e0b39c86b")

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
