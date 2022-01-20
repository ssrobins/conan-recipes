from conans import ConanFile, CMake

class Conan(ConanFile):
    name = "ssrobins_engine"
    version = "1.2.0"
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
        self.build_requires("cmake_utils/6.0.0#ac1a71244046f44f5484a554918f6a42a1f86d99")
        self.build_requires("gtest/1.11.0#8ef69248cd41cd3a29dcfd3340f0589a291c2631")

    def requirements(self):
        self.requires("sdl2/2.0.20#45420ef8e58422639bfab3f61e40d75a03091154")
        self.requires("sdl2_image/2.0.5#0b0319032f60f6e765be783026522fc22cb463f3")
        self.requires("sdl2_mixer/2.0.4#48a9e297f31e1bdd0e8c06242457783cfa6afc6b")
        self.requires("sdl2_ttf/2.0.18#ce0ca328fb213dd7f87bf7084948f564e35f9b68")

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
