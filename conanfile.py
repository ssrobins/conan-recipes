from conans import ConanFile, CMake, tools
import os

class Conan(ConanFile):
    name = "freetype"
    version = "2.10.3"
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
        self.build_requires("cmake_utils/0.3.1#cc144db607f04d12c0b18303a7c7d37386ce0783")

    def requirements(self):
        self.requires("bzip2/1.0.8#cda5e0a4ab0de77d368ac981d78bd900092b526c")
        self.requires("libpng/1.6.37#60e6bdc6bb3b6ad9c0e8844f9d7bbc40e6f5261a")
        self.requires("zlib/1.2.11#9e0f860db8a5309aef59eb1ac8a1821963dc29d8")

    def source(self):
        tools.get(f"http://dnqpy.com/libs/{self.zip_name}")
        os.rename(self.zip_folder_name, self.source_subfolder)

    def build(self):
        from cmake_utils import cmake_init, cmake_build_debug_release
        cmake = cmake_init(self.settings, CMake(self), self.build_folder)
        cmake_build_debug_release(cmake, self.build_subfolder, self.run)

    def package(self):
        from cmake_utils import cmake_init, cmake_install_debug_release
        cmake = cmake_init(self.settings, CMake(self), self.build_folder)
        cmake_install_debug_release(cmake, self.build_subfolder)
        if self.settings.compiler == "Visual Studio":
            self.copy("*.pdb", dst="lib", keep_path=False)
        
    def package_info(self):
        self.cpp_info.includedirs = [os.path.join("include", "freetype2")]
        self.cpp_info.debug.libs = ["freetyped"]
        self.cpp_info.release.libs = ["freetype"]
