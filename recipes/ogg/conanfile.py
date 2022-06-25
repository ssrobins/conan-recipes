from conan import ConanFile
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain
from conan.tools.files import copy, get
import os

required_conan_version = ">=2.0.0-beta1"

class Conan(ConanFile):
    name = "ogg"
    version = "1.3.5"
    description = "Multimedia container format for Xiph.org multimedia codecs"
    homepage = "https://xiph.org/ogg/"
    license = "BSD license"
    url = "https://github.com/ssrobins/conan-recipes"
    settings = "os", "arch", "compiler", "build_type"
    generators = "CMakeDeps"
    revision_mode = "scm"
    exports_sources = ["CMakeLists.txt"]
    zip_folder_name = f"lib{name}-{version}"
    zip_name = f"{zip_folder_name}.tar.xz"

    def requirements(self):
        self.requires("cmake_utils/10.0.1@ssrobins")

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
        cmake.install()

    def package(self):
        if self.settings.compiler == "msvc":
            copy(self, "*.pdb",
                self.build_folder,
                os.path.join(self.package_folder, "lib"),
                keep_path=False)
        
    def package_info(self):
        if self.settings.build_type == "Debug":
            self.cpp_info.libs = ["oggd"]
        else:
            self.cpp_info.libs = ["ogg"]
