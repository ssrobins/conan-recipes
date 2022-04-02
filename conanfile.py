from conans import ConanFile, CMake, tools
import os

class Conan(ConanFile):
    name = "freetype"
    version = "2.12.0"
    description = "Freely available software library to render fonts"
    homepage = "https://www.freetype.org/"
    license = "FTL https://www.freetype.org/license.html"
    url = f"https://github.com/ssrobins/conan-{name}"
    settings = "os", "compiler", "arch"
    generators = "cmake"
    revision_mode = "scm"
    exports_sources = ["CMakeLists.txt"]
    zip_folder_name = f"{name}-{version}"
    zip_name = f"{zip_folder_name}.tar.gz"
    build_subfolder = "build"
    source_subfolder = "source"

    def build_requirements(self):
        self.build_requires("cmake_utils/6.1.0#9ced9bcfd95178b35d2ec5955b725a5652dbda26")

    def requirements(self):
        self.requires("bzip2/1.0.8#580f7301c2f8fcd91c9776ca1a4651e7bad123a1")
        self.requires("libpng/1.6.37#727f83ef089858ec67d8692f1d4f122c5a9bf041")
        self.requires("zlib/1.2.12#49733ddb61eea4e49491653dfcde362a397f66e4")

    def source(self):
        tools.get(f"https://download.savannah.gnu.org/releases/{self.name}/{self.zip_name}",
            sha256="7940a46eeb0255baaa87c553d72778c4f8daa2b8888c8e2a05766a2a8686740c")
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
        self.cpp_info.includedirs = [os.path.join("include", "freetype2")]
        self.cpp_info.debug.libs = ["freetyped"]
        self.cpp_info.release.libs = ["freetype"]
