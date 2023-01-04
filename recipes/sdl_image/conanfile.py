from conan import ConanFile
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain
from conan.tools.files import copy, get
import os
import shutil

required_conan_version = ">=2.0.0-beta7"

class Conan(ConanFile):
    name = "sdl_image"
    version = "2.6.2"
    description = "A library that loads image files as SDL surfaces and textures"
    homepage = "https://www.libsdl.org/projects/SDL_image/"
    license = "Zlib"
    url = "https://github.com/ssrobins/conan-recipes"
    settings = "os", "arch", "compiler", "build_type"
    revision_mode = "scm"
    exports_sources = ["CMakeLists.txt"]
    zip_name = f"release-{version}.tar.gz"

    def requirements(self):
        self.requires("libpng/1.6.39@ssrobins")
        self.requires("sdl/2.26.2@ssrobins")

    @property
    def _source_subfolder(self):
        return "source"

    def layout(self):
        self.folders.build = "build"
        self.folders.generators = self.folders.build

    def source(self):
        get(self,
            f"https://github.com/libsdl-org/SDL_image/archive/refs/tags/{self.zip_name}",
            destination=self._source_subfolder,
            strip_root=True)

    def generate(self):
        tc = CMakeToolchain(self)
        if self.settings.os != "Windows":
            tc.generator = "Ninja Multi-Config"
        tc.variables["CMAKE_VERBOSE_MAKEFILE"] = "TRUE"
        if self.settings.os == "iOS":
            tc.variables["CMAKE_SYSTEM_NAME"] = "iOS"
            if self.settings.arch != "x86_64":
                tc.blocks["apple_system"].values["cmake_osx_architectures"] = "armv7;arm64"
        tc.generate()
        deps = CMakeDeps(self)
        deps.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
        self.run(f"ctest -C {self.settings.build_type} --output-on-failure")

    def package(self):
        cmake = CMake(self)
        cmake.install()
        if self.settings.compiler == "msvc":
            copy(self, "*.pdb",
                self.build_folder,
                os.path.join(self.package_folder, "lib"),
                keep_path=False)

    def package_info(self):
        self.cpp_info.includedirs = [os.path.join("include", "SDL2")]
        if self.settings.build_type == "Debug":
            self.cpp_info.libs = ["SDL2_imaged"]
        else:
            self.cpp_info.libs = ["SDL2_image"]
