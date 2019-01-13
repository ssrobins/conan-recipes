from conans import ConanFile, CMake, tools
import os, shutil
from cmake_utils import cmake_init, cmake_build_debug_release, cmake_install_debug_release

class Conan(ConanFile):
    name = "glew"
    version = os.getenv("package_version")
    description = "OpenGL extension wrangler library"
    homepage = "https://github.com/nigels-com/glew"
    license = "https://github.com/nigels-com/glew/blob/master/LICENSE.txt"
    url = "https://gitlab.com/ssrobins/conan-" + name
    settings = "os", "compiler", "arch"
    generators = "cmake"
    exports = "cmake_utils.py"
    exports_sources = ["CMakeLists.txt"]
    zip_folder_name = "%s-%s" % (name, version)
    zip_name = "%s.tgz" % zip_folder_name
    build_subfolder = "build"
    source_subfolder = "source"

    def source(self):
        tools.download("https://gitlab.com/ssrobins/cmake-utils/raw/master/global_settings.cmake", "global_settings.cmake")
        tools.download("https://gitlab.com/ssrobins/cmake-utils/raw/master/ios.toolchain.cmake", "ios.toolchain.cmake")
        tools.download("https://github.com/nigels-com/glew/releases/download/%s/%s" % (self.zip_folder_name, self.zip_name), self.zip_name)
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
            self.copy(pattern="*.pdb", dst="lib", src="build/source/build/cmake/glew_s.dir/Release", keep_path=False)

    def package_info(self):
        if self.settings.os == "Windows":
            self.cpp_info.debug.libs = ["libglew32d"]
            self.cpp_info.release.libs = ["libglew32"]
            self.cpp_info.libs.append("OpenGL32")
            self.cpp_info.defines.append("GLEW_STATIC")
        else:
            self.cpp_info.debug.libs = ["GLEWd"]
            self.cpp_info.release.libs = ["GLEW"]