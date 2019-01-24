from conans import ConanFile, CMake, tools
import os
from cmake_utils import cmake_init, cmake_build_debug_release, cmake_install_debug_release

class Conan(ConanFile):
    name = "freetype"
    version = os.getenv("package_version")
    description = "Freely available software library to render fonts"
    homepage = "https://www.freetype.org/"
    license = "FTL https://www.freetype.org/license.html"
    url = "https://gitlab.com/ssrobins/conan-" + name
    settings = "os", "compiler", "arch"
    generators = "cmake"
    exports = "cmake_utils.py"
    exports_sources = ["CMakeLists.diff", "CMakeLists.txt"]
    zip_folder_name = "%s-%s" % (name, version)
    zip_name = "%s.tar.gz" % zip_folder_name
    build_subfolder = "build"
    source_subfolder = "source"

    def requirements(self):
        self.requires.add("bzip2/1.0.6@stever/stable")
        self.requires.add("libpng/1.6.36@stever/stable")
        self.requires.add("zlib/1.2.11@stever/stable")

    def source(self):
        tools.download("https://gitlab.com/ssrobins/cmake-utils/raw/master/global_settings.cmake", "global_settings.cmake")
        tools.download("https://gitlab.com/ssrobins/cmake-utils/raw/master/ios.toolchain.cmake", "ios.toolchain.cmake")
        tools.download("http://download.savannah.gnu.org/releases/freetype/%s" % self.zip_name, self.zip_name)
        tools.unzip(self.zip_name)
        os.unlink(self.zip_name)
        os.rename(self.zip_folder_name, self.source_subfolder)
        
        # Patch the CMakeLists.txt file with the following changes:
        # https://savannah.nongnu.org/bugs/index.php?54450
        # https://savannah.nongnu.org/bugs/index.php?54048
        # https://savannah.nongnu.org/bugs/index.php?53816
        # https://savannah.nongnu.org/bugs/index.php?53815
        tools.patch(base_path=self.source_subfolder, patch_file="CMakeLists.diff")

    def build(self):
        cmake = cmake_init(self.settings, CMake(self), self.build_folder)
        cmake_build_debug_release(cmake, self.build_subfolder)

    def package(self):
        cmake = cmake_init(self.settings, CMake(self), self.build_folder)
        cmake_install_debug_release(cmake, self.build_subfolder)
        if self.settings.compiler == "Visual Studio":
            self.copy(pattern="*.pdb", dst="lib", src="build/source/freetype.dir/Release", keep_path=False)
        
    def package_info(self):
        self.cpp_info.includedirs = [os.path.join("include", "freetype2")]
        self.cpp_info.debug.libs = ["freetyped"]
        self.cpp_info.release.libs = ["freetype"]