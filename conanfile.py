from conans import ConanFile, CMake, tools
import os
from cmake_utils import cmake_init, cmake_build_debug_release, cmake_install_debug_release

class Conan(ConanFile):
    name = "libpng"
    version = "1.6.37"
    description = "Official PNG image format reference library"
    homepage = "http://www.libpng.org"
    license = "Libpng http://www.libpng.org/pub/png/src/libpng-LICENSE.txt"
    url = "https://gitlab.com/ssrobins/conan-" + name
    settings = "os", "compiler", "arch"
    generators = "cmake"
    revision_mode = "scm"
    exports = "cmake_utils.py"
    exports_sources = ["CMakeLists.diff", "CMakeLists.txt", "global_settings.cmake", "ios.toolchain.cmake"]
    zip_folder_name = "libpng-%s" % version
    zip_name = "%s.tar.gz" % zip_folder_name
    build_subfolder = "build"
    source_subfolder = "source"
    maj_min_ver = str().join(version.split(".")[0:2])

    def requirements(self):
        self.requires.add("zlib/1.2.11#85844dd3e9dcd0dadc4873592a971b1a34228ce9")

    def source(self):
        tools.download("http://dnqpy.com/libs/%s" % self.zip_name, self.zip_name)
        tools.unzip(self.zip_name)
        os.unlink(self.zip_name)
        os.rename(self.zip_folder_name, self.source_subfolder)

        # Apply a patch to the libpng CMakeLists.txt file with the following changes:
        # https://sourceforge.net/p/libpng/code/merge-requests/4/
        tools.patch(base_path=self.source_subfolder, patch_file="CMakeLists.diff")

    def build(self):
        cmake = cmake_init(self.settings, CMake(self), self.build_folder)
        cmake_build_debug_release(cmake, self.build_subfolder)

    def package(self):
        cmake = cmake_init(self.settings, CMake(self), self.build_folder)
        cmake_install_debug_release(cmake, self.build_subfolder)
        if self.settings.compiler == "Visual Studio":
            self.copy("*.pdb", dst="lib", keep_path=False)

    def package_info(self):
        if self.settings.os == "Windows":
            self.cpp_info.debug.libs = ["libpng%sd" % self.maj_min_ver]
            self.cpp_info.release.libs = ["libpng%s" % self.maj_min_ver]
        else:
            self.cpp_info.debug.libs = ["png%sd" % self.maj_min_ver]
            self.cpp_info.release.libs = ["png%s" % self.maj_min_ver]
