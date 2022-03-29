from conans import ConanFile, CMake, tools
from conans.util import files
import os

class Conan(ConanFile):
    name = "zlib"
    version = "1.2.12"
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
        self.build_requires("cmake_utils/5.0.0#1ecfed8c68a43ea17d321701cc8a91df21d06453")

    def source(self):
        tools.get(f"https://zlib.net/{self.zip_name}",
            sha256="91844808532e5ce316b3c010929493c0244f3d37593afd6de04f71821d5136d9")
        os.rename(self.zip_folder_name, self.source_subfolder)

    def build(self):
        from cmake_utils import cmake_init, cmake_build_debug_release
        cmake = cmake_init(self.settings, CMake(self), self.build_folder)
        cmake_build_debug_release(cmake, self.build_subfolder, self.run)

    def package(self):
        self.copy("*.h", dst="include", src=self.source_subfolder)
        self.copy("*.h", dst="include", src=self.build_folder, keep_path=False)
        self.copy("build/lib/zlibstatic*.lib", dst="lib", keep_path=False)
        self.copy("build/lib/*.a", dst="lib", keep_path=False)
        if self.settings.compiler == "msvc":
            self.copy("*.pdb", dst="lib", keep_path=False)

    def package_info(self):
        if self.settings.os == "Windows" and not tools.os_info.is_linux:
            self.cpp_info.debug.libs = ["zlibstaticd"]
            self.cpp_info.release.libs = ["zlibstatic"]
        else:
            self.cpp_info.debug.libs = ["zd"]
            self.cpp_info.release.libs = ["z"]
