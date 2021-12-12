from conans import ConanFile, CMake, tools
import os, shutil

class Conan(ConanFile):
    name = "sdl2_mixer"
    version = "2.0.4"
    description = "A sample multi-channel audio mixer library"
    homepage = "https://www.libsdl.org/projects/SDL_mixer/"
    license = "Zlib"
    url = f"https://github.com/ssrobins/conan-{name}"
    settings = "os", "compiler", "arch"
    generators = "cmake"
    revision_mode = "scm"
    exports_sources = ["CMakeLists.txt", f"CMakeLists-{name}.txt"]
    zip_folder_name = f"SDL2_mixer-{version}"
    zip_name = f"{zip_folder_name}.tar.gz"
    build_subfolder = "build"
    source_subfolder = "source"

    def build_requirements(self):
        self.build_requires("cmake_utils/5.0.0#1ecfed8c68a43ea17d321701cc8a91df21d06453")
    
    def requirements(self):
        self.requires("sdl2/2.0.18#f9abc4b1f200e751c41e1aab3026eeb7370b0d46")
        self.requires("vorbis/1.3.7#6c0082787f1881f6c8a589304b45c20014a83ba9")

    def source(self):
        tools.get(f"https://www.libsdl.org/projects/SDL_mixer/release/{self.zip_name}")
        os.rename(self.zip_folder_name, self.source_subfolder)
        shutil.move(f"CMakeLists-{self.name}.txt", os.path.join(self.source_subfolder, "CMakeLists.txt"))

    def build(self):
        from cmake_utils import cmake_init, cmake_build_debug_release
        cmake = cmake_init(self.settings, CMake(self), self.build_folder)
        cmake_build_debug_release(cmake, self.build_subfolder, self.run)

    def package(self):
        self.copy("SDL_mixer.h", dst="include", src=self.source_subfolder)
        self.copy("*.lib", dst="lib", src=self.build_subfolder, keep_path=False)
        self.copy("build/lib/*.a", dst="lib", keep_path=False)
        if self.settings.compiler == "msvc":
            self.copy("*.pdb", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.debug.libs = ["SDL2_mixerd"]
        self.cpp_info.release.libs = ["SDL2_mixer"]
