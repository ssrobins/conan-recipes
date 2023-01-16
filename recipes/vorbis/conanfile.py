from conan import ConanFile
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain
from conan.tools.files import copy, get
import os

required_conan_version = ">=2.0.0-beta7"

class Conan(ConanFile):
    name = "vorbis"
    version = "1.3.7"
    description = "General-purpose compressed audio format for mid to high quality audio and music"
    homepage = "https://xiph.org/vorbis/"
    license = "BSD license"
    url = "https://github.com/ssrobins/conan-recipes"
    settings = "os", "arch", "compiler", "build_type"
    exports_sources = ["CMakeLists.txt"]
    zip_folder_name = f"lib{name}-{version}"
    zip_name = f"{zip_folder_name}.tar.xz"

    def requirements(self):
        self.requires("ogg/1.3.5@ssrobins")

    @property
    def _source_subfolder(self):
        return "source"

    def layout(self):
        self.folders.build = "build"
        self.folders.generators = self.folders.build

    def source(self):
        get(self,
            f"https://downloads.xiph.org/releases/{self.name}/{self.zip_name}",
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
        copy(self, "include/*.h",
            os.path.join(self.source_folder, self._source_subfolder),
            os.path.join(self.package_folder, "include"))
        copy(self, "*.lib",
            self.build_folder,
            os.path.join(self.package_folder, "lib"),
            keep_path=False)
        copy(self, "*.a",
            self.build_folder,
            os.path.join(self.package_folder, "lib"),
            keep_path=False)
        if self.settings.compiler == "msvc":
            copy(self, "*.pdb",
                self.build_folder,
                os.path.join(self.package_folder, "lib"),
                keep_path=False)

    def package_info(self):
        self.cpp_info.includedirs = ["include"]
        if self.settings.build_type == "Debug":
            self.cpp_info.libs = ["vorbisfiled", "vorbisencd", "vorbisd"]
        else:
            self.cpp_info.libs = ["vorbisfile", "vorbisenc", "vorbis"]
