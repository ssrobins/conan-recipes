from conans import ConanFile, CMake, tools
import os

class Conan(ConanFile):
    name = "freetype"
    version = "2.11.1"
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
        self.build_requires("cmake_utils/5.0.0#1ecfed8c68a43ea17d321701cc8a91df21d06453")

    def requirements(self):
        self.requires("bzip2/1.0.8#580f7301c2f8fcd91c9776ca1a4651e7bad123a1")
        self.requires("libpng/1.6.37#a9b43a54310aa506830552f91b827ef47b8f13cc")
        self.requires("zlib/1.2.11#d4f0926217661284546b547bd9a6f2bf5b6127ec")

    def source(self):
        tools.get(f"https://download.savannah.gnu.org/releases/{self.name}/{self.zip_name}")
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
