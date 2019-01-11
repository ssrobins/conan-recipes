from conans import ConanFile, CMake, tools
import os, shutil
from cmake_utils import cmake_init, cmake_build_debug_release, cmake_install_debug_release

class Conan(ConanFile):
    name = "sfml"
    version = os.getenv("package_version")
    description = "Simple and fast multimedia library"
    homepage = "https://www.sfml-dev.org/"
    license = "Zlib"
    url = "https://gitlab.com/ssrobins/conan-" + name
    settings = "os", "compiler", "arch"
    generators = "cmake"
    exports = "cmake_utils.py"
    exports_sources = ["CMakeLists.txt"]
    zip_folder_name = "SFML-%s" % version
    zip_name = "%s-sources.zip" % zip_folder_name
    build_subfolder = "build"
    source_subfolder = "source"

    def requirements(self):
        self.requires.add("freetype/2.9.1@stever/testing")
    
    def source(self):
        tools.download("https://gitlab.com/ssrobins/cmake-utils/raw/master/global_settings.cmake", "global_settings.cmake")
        tools.download("https://gitlab.com/ssrobins/cmake-utils/raw/master/ios.toolchain.cmake", "ios.toolchain.cmake")
        tools.download("https://www.sfml-dev.org/files/%s" % self.zip_name, self.zip_name)
        tools.unzip(self.zip_name)
        os.unlink(self.zip_name)
        os.rename(self.zip_folder_name, self.source_subfolder)

    def build(self):
        cmake = cmake_init(self.settings, CMake(self), self.build_folder)
        cmake_build_debug_release(cmake, self.build_subfolder)
