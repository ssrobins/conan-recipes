from conans import ConanFile, CMake, tools
from conans.util import files
import os

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
    revision_mode = "scm"
    exports_sources = ["CMakeLists.diff", "CMakeLists.txt"]
    zip_folder_name = "%s-%s" % (name, version)
    zip_name = "%s.tar.gz" % zip_folder_name
    build_subfolder = "build"
    source_subfolder = "source"

    def build_requirements(self):
        self.build_requires.add("cmake_utils/0.3.1#1cf9333e6fba1b7350ec8d4d06f737b54d163eef")

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
        #   -MACOSX_RPATH set to ON to avoid CMake configure warning (no longer an issue in CMake 3.15?)
        # Submitted these changes to zlib@gzip.org and filed this PR:
        # https://github.com/madler/zlib/pull/441
        tools.patch(base_path=self.source_subfolder, patch_file="CMakeLists.diff")

    def build(self):
        from cmake_utils import cmake_init, cmake_build_debug_release
        cmake = cmake_init(self.settings, CMake(self), self.build_folder)
        cmake_build_debug_release(cmake, self.build_subfolder, self.run)

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
