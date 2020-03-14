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
        self.build_requires("cmake_utils/0.3.1#09e87aa7b71951c0c77bbf861baaaa53c3d55830")
        self.build_requires("gtest/1.10.0#e61f09593757c0bc883d927a3b7f284dfb1c0267")

    def requirements(self):
        self.requires("sdl2/2.0.8#51a526f605844c5d5f73275bf3fe1ad121509866")
        self.requires("sdl2_image/2.0.5#306817061e8c746beee556b04facaf7ab1dcc585")
        self.requires("sdl2_ttf/2.0.15#c390ca26f68facafb46d1cf7270c38d647b567c7")

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
