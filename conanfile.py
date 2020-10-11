from conans import ConanFile, CMake, tools
import os, shutil

class Conan(ConanFile):
    name = "sdl2_ttf"
    version = "2.0.15"
    description = "A sample library which allows you to use TrueType fonts in your SDL applications"
    homepage = "https://www.libsdl.org/projects/SDL_ttf/"
    license = "Zlib"
    url = f"https://github.com/ssrobins/conan-{name}"
    settings = "os", "compiler", "arch"
    generators = "cmake"
    revision_mode = "scm"
    exports_sources = ["CMakeLists.txt", f"CMakeLists-{name}.txt"]
    zip_folder_name = f"SDL2_ttf-{version}"
    zip_name = f"{zip_folder_name}.tar.gz"
    build_subfolder = "build"
    source_subfolder = "source"

    def build_requirements(self):
        self.build_requires("cmake_utils/0.3.1#724fce6f13f84579d39b6983af6213c414d69e7b")
    
    def requirements(self):
        self.requires("freetype/2.10.3#4c236b3a594caf5df3846148f80686fe44037cb9")
        self.requires("sdl2/2.0.8#e824c9c0c6aaad95da3437224a23f50cf6295b8a")

    def source(self):
        tools.get(f"https://www.libsdl.org/projects/SDL_ttf/release/{self.zip_name}")
        os.rename(self.zip_folder_name, self.source_subfolder)
        shutil.move(f"CMakeLists-{self.name}.txt", os.path.join(self.source_subfolder, "CMakeLists.txt"))

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
