from conans import ConanFile, CMake, tools
import os, shutil
from cmake_utils import cmake_init, cmake_build_debug_release

class Conan(ConanFile):
    name = "sdl2_image"
    version = "2.0.5"
    description = "A library that loads image files as SDL surfaces and textures"
    homepage = "https://www.libsdl.org/projects/SDL_image/"
    license = "Zlib"
    url = "https://gitlab.com/ssrobins/conan-" + name
    settings = "os", "compiler", "arch"
    generators = "cmake"
    revision_mode = "scm"
    exports = "cmake_utils.py"
    exports_sources = ["CMakeLists.txt", "CMakeLists-%s.txt" % name, "global_settings.cmake"]
    zip_folder_name = "SDL2_image-%s" % version
    zip_name = "%s.tar.gz" % zip_folder_name
    build_subfolder = "build"
    source_subfolder = "source"
    
    def requirements(self):
        self.requires.add("libpng/1.6.37#5ef282214597bca8af24a11d8ef10bc7715fe96d")
        self.requires.add("sdl2/2.0.8#e119e81196414d99c32c6ef72a8c2624b9408171")

    def source(self):
        tools.download("https://www.libsdl.org/projects/SDL_image/release/%s" % self.zip_name, self.zip_name)
        tools.unzip(self.zip_name)
        os.unlink(self.zip_name)
        os.rename(self.zip_folder_name, self.source_subfolder)
        shutil.move("CMakeLists-%s.txt" % self.name, os.path.join(self.source_subfolder, "CMakeLists.txt"))

    def build(self):
        cmake = cmake_init(self.settings, CMake(self), self.build_folder)
        cmake_build_debug_release(cmake, self.build_subfolder)

    def package(self):
        self.copy("SDL_image.h", dst="include", src=self.source_subfolder)
        self.copy("*.lib", dst="lib", src=self.build_subfolder, keep_path=False)
        self.copy("build/lib/*.a", dst="lib", keep_path=False)
        if self.settings.compiler == "Visual Studio":
            self.copy("*.pdb", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.debug.libs = ["SDL2_imaged"]
        self.cpp_info.release.libs = ["SDL2_image"]
