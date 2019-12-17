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
        self.build_requires.add("cmake_utils/0.3.0#0ec3922f6b2df47dc695bacdbc5491fb972f0a75")
        self.build_requires.add("gtest/1.10.0#39adcd397319f61148b40f694b47ab5b3e6fa320")

    def requirements(self):
        self.requires.add("sdl2/2.0.8#0ac39a5179e1f92a0af645ee15c70760af8cf590")
        self.requires.add("sdl2_image/2.0.5#7128d1619c4280601d547e819bbb21c45b77d6a3")
        self.requires.add("sdl2_ttf/2.0.15#a7d869fc909d785a9aa26814d2bdd4655cd5dd05")

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
