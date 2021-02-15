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
    url = f"https://github.com/ssrobins/conan-{name}"
    settings = "os", "compiler", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"
    revision_mode = "scm"
    exports_sources = ["CMakeLists.diff", "CMakeLists.txt"]
    zip_folder_name = f"{name}-{version}"
    zip_name = f"{zip_folder_name}.tar.gz"
    build_subfolder = "build"
    source_subfolder = "source"

    def build_requirements(self):
        self.build_requires("cmake_utils/0.3.1#e474aafdec36cf92d97e781b844f390f3170f29f")

    def source(self):
        tools.get(f"https://zlib.net/{self.zip_name}",
            sha256="c3e5e9fdd5004dcb542feda5ee4f0ff0744628baf8ed2dd5d66f8ca1197cb1a1")
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
