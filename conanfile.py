from conans import ConanFile, CMake, tools
import os

class Conan(ConanFile):
    name = "box2d"
    version = "2.3.1"
    description = "A 2D physics engine for games"
    homepage = "https://box2d.org/"
    license = "Zlib"
    url = f"https://github.com/ssrobins/conan-{name}"
    settings = "os", "compiler", "arch"
    generators = "cmake"
    revision_mode = "scm"
    exports_sources = ["CMakeLists.txt"]
    zip_folder_name = f"{name}-{version}"
    zip_name = f"v{version}.tar.gz"
    build_subfolder = "build"
    source_subfolder = "source"

    def build_requirements(self):
        self.build_requires("cmake_utils/2.0.1#bc87acc9a67867fb20e22e3c51eb4c070a9f9758")
    
    def source(self):
        tools.get(f"https://github.com/erincatto/Box2D/archive/{self.zip_name}")
        os.rename(self.zip_folder_name, self.source_subfolder)

    def build(self):
        from cmake_utils import cmake_init, cmake_build_debug_release
        cmake = cmake_init(self.settings, CMake(self), self.build_folder)
        cmake_build_debug_release(cmake, self.build_subfolder, self.run)

    def package(self):
        from cmake_utils import cmake_init, cmake_install_debug_release
        cmake = cmake_init(self.settings, CMake(self), self.build_folder)
        cmake_install_debug_release(cmake, self.build_subfolder)
        if self.settings.compiler == "msvc":
            self.copy("*.pdb", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.debug.libs = ["Box2Dd"]
        self.cpp_info.release.libs = ["Box2D"]
