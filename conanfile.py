from conans import ConanFile, CMake, tools
import os, shutil

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
    exports_sources = ["CMakeLists.txt", "CMakeLists-%s.txt" % name]
    zip_folder_name = "SDL2_image-%s" % version
    zip_name = "%s.tar.gz" % zip_folder_name
    build_subfolder = "build"
    source_subfolder = "source"

    def build_requirements(self):
        self.build_requires.add("cmake_utils/0.3.1#1cf9333e6fba1b7350ec8d4d06f737b54d163eef")

    def requirements(self):
        self.requires.add("libpng/1.6.37#25a502818834d863ef33d29dda4ef11918398da5")
        self.requires.add("sdl2/2.0.8#0ac39a5179e1f92a0af645ee15c70760af8cf590")

    def source(self):
        tools.download("https://www.libsdl.org/projects/SDL_image/release/%s" % self.zip_name, self.zip_name)
        tools.unzip(self.zip_name)
        os.unlink(self.zip_name)
        os.rename(self.zip_folder_name, self.source_subfolder)
        shutil.move("CMakeLists-%s.txt" % self.name, os.path.join(self.source_subfolder, "CMakeLists.txt"))

    def build(self):
        from cmake_utils import cmake_init, cmake_build_debug_release
        cmake = cmake_init(self.settings, CMake(self), self.build_folder)
        cmake_build_debug_release(cmake, self.build_subfolder, self.run)

    def package(self):
        self.copy("SDL_image.h", dst="include", src=self.source_subfolder)
        self.copy("*.lib", dst="lib", src=self.build_subfolder, keep_path=False)
        self.copy("build/lib/*.a", dst="lib", keep_path=False)
        if self.settings.compiler == "Visual Studio":
            self.copy("*.pdb", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.debug.libs = ["SDL2_imaged"]
        self.cpp_info.release.libs = ["SDL2_image"]
