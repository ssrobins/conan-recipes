from conans import ConanFile, CMake, tools
import os
from cmake_utils import cmake_init, cmake_build_debug_release, cmake_install_debug_release

class Conan(ConanFile):
    name = "freetype"
    version = "2.10.1"
    description = "Freely available software library to render fonts"
    homepage = "https://www.freetype.org/"
    license = "FTL https://www.freetype.org/license.html"
    url = "https://gitlab.com/ssrobins/conan-" + name
    settings = "os", "compiler", "arch"
    generators = "cmake"
    revision_mode = "scm"
    exports = "cmake_utils.py"
    exports_sources = ["CMakeLists.diff", "CMakeLists.txt", "global_settings.cmake"]
    zip_folder_name = "%s-%s" % (name, version)
    zip_name = "%s.tar.gz" % zip_folder_name
    build_subfolder = "build"
    source_subfolder = "source"

    def requirements(self):
        self.requires.add("bzip2/1.0.6#b249c46e5f277060708ffd828d0f4bab73bd6543")
        self.requires.add("libpng/1.6.37#4feb62eebfe1932daba02a3a07b6f33b7c3c6bda")
        self.requires.add("zlib/1.2.11#ca6bcf63886881139dc047310c63473e66b0ef1a")

    def source(self):
        tools.download("http://dnqpy.com/libs/%s" % self.zip_name, self.zip_name)
        tools.unzip(self.zip_name)
        os.unlink(self.zip_name)
        os.rename(self.zip_folder_name, self.source_subfolder)

    def build(self):
        cmake = cmake_init(self.settings, CMake(self), self.build_folder)
        cmake_build_debug_release(cmake, self.build_subfolder)

    def package(self):
        cmake = cmake_init(self.settings, CMake(self), self.build_folder)
        cmake_install_debug_release(cmake, self.build_subfolder)
        if self.settings.compiler == "Visual Studio":
            self.copy("*.pdb", dst="lib", keep_path=False)
        
    def package_info(self):
        self.cpp_info.includedirs = [os.path.join("include", "freetype2")]
        self.cpp_info.debug.libs = ["freetyped"]
        self.cpp_info.release.libs = ["freetype"]
