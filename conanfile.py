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
        self.build_requires("cmake_utils/0.3.1#77d5f06b9b20302a5410e41ed45e7bbea7de90a5")
        self.build_requires("gtest/1.11.0#5c7586ef6610e8053ee79086fbc7743d9fbde653")

    def requirements(self):
        self.requires("sdl2/2.0.16#b5081764744dd13a648d8ae2ff0d0abce3d7fe91")
        self.requires("sdl2_image/2.0.5#b5d3918c53fdd0f98369d62a030e62d155645891")
        self.requires("sdl2_ttf/2.0.15#9ea05bfcaf8e9d6819d67f24db6a3d2300914011")

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
