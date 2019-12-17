from conans import ConanFile, CMake, tools
import os, shutil

class Conan(ConanFile):
    name = "sdl2_ttf"
    version = "2.0.15"
    description = "A sample library which allows you to use TrueType fonts in your SDL applications"
    homepage = "https://www.libsdl.org/projects/SDL_ttf/"
    license = "Zlib"
    url = "https://gitlab.com/ssrobins/conan-" + name 
    settings = "os", "compiler", "arch"
    generators = "cmake"
    revision_mode = "scm"
    exports_sources = ["CMakeLists.txt", "CMakeLists-%s.txt" % name]
    zip_folder_name = "SDL2_ttf-%s" % version
    zip_name = "%s.tar.gz" % zip_folder_name
    build_subfolder = "build"
    source_subfolder = "source"

    def build_requirements(self):
        self.build_requires.add("cmake_utils/0.3.0#0ec3922f6b2df47dc695bacdbc5491fb972f0a75")
    
    def requirements(self):
        self.requires.add("freetype/2.10.1#55cdddfb825c2cba23f43adfc33e97bbb1d19f3a")
        self.requires.add("sdl2/2.0.8#0ac39a5179e1f92a0af645ee15c70760af8cf590")

    def source(self):
        tools.download("https://www.libsdl.org/projects/SDL_ttf/release/%s" % self.zip_name, self.zip_name)
        tools.unzip(self.zip_name)
        os.unlink(self.zip_name)
        os.rename(self.zip_folder_name, self.source_subfolder)
        shutil.move("CMakeLists-%s.txt" % self.name, os.path.join(self.source_subfolder, "CMakeLists.txt"))

    def build(self):
        from cmake_utils import cmake_init, cmake_build_debug_release
        cmake = cmake_init(self.settings, CMake(self), self.build_folder)
        cmake_build_debug_release(cmake, self.build_subfolder, self.run)

    def package(self):
        self.copy("SDL_ttf.h", dst="include", src=self.source_subfolder)
        self.copy("*.lib", dst="lib", src=self.build_subfolder, keep_path=False)
        self.copy("build/lib/*.a", dst="lib", keep_path=False)
        if self.settings.compiler == "Visual Studio":
            self.copy("*.pdb", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.debug.libs = ["SDL2_ttfd"]
        self.cpp_info.release.libs = ["SDL2_ttf"]
