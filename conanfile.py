from conans import ConanFile, CMake

class Conan(ConanFile):
    name = "ssrobins_engine"
    version = "0.2.0"
    description = "Thin game engine wrapper"
    homepage = "https://gitlab.com/ssrobins/conan-" + name
    license = "MIT"
    url = "https://gitlab.com/ssrobins/conan-" + name
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
        self.build_requires.add("cmake_utils/0.1.0#7f17deeced79eecd4a03ba2d327bee3e5e794732")
        self.build_requires.add("gtest/1.10.0#ca07d9d05d12f3bbb091f095e30f7c54cd2920ee")

    def requirements(self):
        self.requires.add("sdl2/2.0.8#6fbd96a731b885d3316671eb252968e173d48fbc")
        self.requires.add("sdl2_image/2.0.5#1c6c8f29fe92cfc43ee055200e2bd3d07da06020")
        self.requires.add("sdl2_ttf/2.0.15#cf879d4de1f7dff57b543a00418a9fa599ea20c5")

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
