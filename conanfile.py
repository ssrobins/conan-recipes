from conans import ConanFile, CMake, tools
import os, shutil

class Conan(ConanFile):
    name = "sdl2_image"
    version = "2.0.5"
    description = "A library that loads image files as SDL surfaces and textures"
    homepage = "https://www.libsdl.org/projects/SDL_image/"
    license = "Zlib"
    url = f"https://github.com/ssrobins/conan-{name}"
    settings = "os", "compiler", "arch"
    generators = "cmake"
    revision_mode = "scm"
    exports_sources = ["CMakeLists.txt", f"CMakeLists-{name}.txt"]
    zip_folder_name = f"SDL2_image-{version}"
    zip_name = f"{zip_folder_name}.tar.gz"
    build_subfolder = "build"
    source_subfolder = "source"

    def build_requirements(self):
        self.build_requires("cmake_utils/0.3.1#cc144db607f04d12c0b18303a7c7d37386ce0783")

    def requirements(self):
        self.requires("libpng/1.6.37#b5fe8c7dd7054049d119ccabcdee1821050720dd")
        self.requires("sdl2/2.0.8#abbd4c5be105743339ebff6140b9154669b9de00")

    def source(self):
        tools.get(f"https://www.libsdl.org/projects/SDL_image/release/{self.zip_name}")
        os.rename(self.zip_folder_name, self.source_subfolder)
        shutil.move(f"CMakeLists-{self.name}.txt", os.path.join(self.source_subfolder, "CMakeLists.txt"))

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
