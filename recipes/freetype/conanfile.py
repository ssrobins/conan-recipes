from conan import ConanFile
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain
from conan.tools.files import copy, get
import os

required_conan_version = ">=2.0.0-beta10"

class Conan(ConanFile):
    name = "freetype"
    version = "2.13.0"
    description = "Freely available software library to render fonts"
    homepage = "https://www.freetype.org/"
    license = "FTL https://www.freetype.org/license.html"
    url = "https://github.com/ssrobins/conan-recipes"
    settings = "os", "arch", "compiler", "build_type"
    exports_sources = ["CMakeLists.txt"]
    zip_folder_name = f"{name}-{version}"
    zip_name = f"{zip_folder_name}.tar.xz"

    def requirements(self):
        self.requires("bzip2/1.0.8@ssrobins")
        self.requires("libpng/1.6.39@ssrobins")
        self.requires("zlib/1.2.13@ssrobins")

    @property
    def _source_subfolder(self):
        return "source"

    def layout(self):
        self.folders.build = "build"
        self.folders.generators = self.folders.build

    def source(self):
        get(self,
            f"https://sourceforge.net/projects/{self.name}/files/{self.name}2/{self.version}/{self.zip_name}",
            sha256="5ee23abd047636c24b2d43c6625dcafc66661d1aca64dec9e0d05df29592624c",
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
        self.cpp_info.set_property("cmake_target_name", "Freetype::Freetype")
        self.cpp_info.includedirs = [os.path.join("include", "freetype2")]
        if self.settings.build_type == "Debug":
            self.cpp_info.libs = ["freetyped"]
        else:
            self.cpp_info.libs = ["freetype"]
