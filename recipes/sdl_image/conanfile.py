from conans import ConanFile, tools
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain
import os
import shutil

class Conan(ConanFile):
    name = "sdl2_image"
    version = "2.0.5"
    description = "A library that loads image files as SDL surfaces and textures"
    homepage = "https://www.libsdl.org/projects/SDL_image/"
    license = "Zlib"
    url = f"https://github.com/ssrobins/conan-{name}"
    settings = "os", "arch", "compiler", "build_type"
    generators = "CMakeDeps"
    revision_mode = "scm"
    exports_sources = ["CMakeLists.txt", f"CMakeLists-{name}.txt"]
    zip_folder_name = f"SDL2_image-{version}"
    zip_name = f"{zip_folder_name}.tar.gz"

    def build_requirements(self):
        self.build_requires("cmake_utils/9.0.1")

    def requirements(self):
        self.requires("libpng/1.6.37")
        self.requires("sdl2/2.0.22")

    @property
    def _source_subfolder(self):
        return "source"

    def layout(self):
        self.folders.build = "build"
        self.folders.generators = self.folders.build

    def source(self):
        tools.get(f"https://www.libsdl.org/projects/SDL_image/release/{self.zip_name}",
            destination=self._source_subfolder,
            strip_root=True)
        shutil.move(f"CMakeLists-{self.name}.txt", os.path.join(self._source_subfolder, "CMakeLists.txt"))

    def generate(self):
        tc = CMakeToolchain(self)
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
        self.copy("SDL_image.h", dst="include", src=self._source_subfolder)
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)
        if self.settings.compiler == "msvc":
            self.copy("*.pdb", dst="lib", keep_path=False)

    def package_info(self):
        if self.settings.build_type == "Debug":
            self.cpp_info.libs = ["SDL2_imaged"]
        else:
            self.cpp_info.libs = ["SDL2_image"]
