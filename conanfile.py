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
        self.build_requires("cmake_utils/0.3.1#b92e3b563e31a4fe0e55849f3bfdb55eb7b06284")
        self.build_requires("gtest/1.10.0#63a50a1e81ce6ccf89196114a653fb162bbbca7e")

    def requirements(self):
        self.requires("sdl2/2.0.8#8656fec433c5348cb887387cc530547d4381115f")
        self.requires("sdl2_image/2.0.5#246219f863088fcca9100cc3c2cda6d5fe2784b8")
        self.requires("sdl2_ttf/2.0.15#5e9f7bd984d4ea157cc433308037eeda9a0e7098")

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
