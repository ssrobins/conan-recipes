from conans import ConanFile, CMake, tools
from conans.util import files
import os
from cmake_utils import cmake_init, cmake_build_debug_release

class Conan(ConanFile):
    name = "zlib"
    version = "1.2.11"
    description = "A Massively Spiffy Yet Delicately Unobtrusive Compression Library " \
                  "(Also Free, Not to Mention Unencumbered by Patents)"
    homepage = "https://zlib.net/"
    license = "Zlib"
    url = "https://gitlab.com/ssrobins/conan-" + name
    settings = "os", "compiler", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"
    exports = "cmake_utils.py"
    exports_sources = ["CMakeLists.diff", "CMakeLists.txt", "global_settings.cmake", "ios.toolchain.cmake"]
    zip_folder_name = "%s-%s" % (name, version)
    zip_name = "%s.tar.gz" % zip_folder_name
    build_subfolder = "build"
    source_subfolder = "source"

    def source(self):
        tools.download("https://zlib.net/%s" % self.zip_name, self.zip_name)
        tools.unzip(self.zip_name)
        files.rmdir("%s/contrib" % self.zip_folder_name)
        os.unlink(self.zip_name)
        os.rename(self.zip_folder_name, self.source_subfolder)
        
        # Patch the CMakeLists.txt file with:
        #   -New options BUILD_ZLIB_EXAMPLE and BUILD_ZLIB_MINIGZIP that allow shutting off
        #    those example executable builds so I don't have to set MACOSX_BUNDLE,
        #    XCODE_ATTRIBUTE_CODE_SIGN_IDENTITY, and XCODE_ATTRIBUTE_DEVELOPMENT_TEAM to get
        #    iOS builds to work
        #   -MACOSX_RPATH set to ON to avoid CMake configure warning
        # Submitted these changes to zlib@gzip.org
        tools.patch(base_path=self.source_subfolder, patch_file="CMakeLists.diff")

    def build(self):
        cmake = cmake_init(self.settings, CMake(self), self.build_folder)
        cmake_build_debug_release(cmake, self.build_subfolder)

    def package(self):
        self.copy("*.h", dst="include", src=self.source_subfolder)
        self.copy("*.h", dst="include", src=self.build_folder, keep_path=False)
        self.copy("build/lib/zlibstatic*.lib", dst="lib", keep_path=False)
        self.copy("build/lib/*.a", dst="lib", keep_path=False)
        if self.settings.compiler == "Visual Studio":
            self.copy("*.pdb", dst="lib", keep_path=False)

    def package_info(self):
        if self.settings.os == "Windows" and not tools.os_info.is_linux:
            self.cpp_info.debug.libs = ["zlibstaticd"]
            self.cpp_info.release.libs = ["zlibstatic"]
        else:
            self.cpp_info.debug.libs = ["zd"]
            self.cpp_info.release.libs = ["z"]
        self.cpp_info.libs = self.cpp_info.release.libs
