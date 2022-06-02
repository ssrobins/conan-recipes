from conans import ConanFile, tools
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain
import os

class Conan(ConanFile):
    name = "freetype"
    version = "2.12.1"
    description = "Freely available software library to render fonts"
    homepage = "https://www.freetype.org/"
    license = "FTL https://www.freetype.org/license.html"
    url = f"https://github.com/ssrobins/conan-{name}"
    settings = "os", "arch", "compiler", "build_type"
    generators = "CMakeDeps"
    revision_mode = "scm"
    exports_sources = ["CMakeLists.txt"]
    zip_folder_name = f"{name}-{version}"
    zip_name = f"{zip_folder_name}.tar.gz"

    def build_requirements(self):
        self.build_requires("cmake_utils/9.0.1")

    def requirements(self):
        self.requires("bzip2/1.0.8")
        self.requires("libpng/1.6.37")
        self.requires("zlib/1.2.12")

    @property
    def _source_subfolder(self):
        return "source"

    def layout(self):
        self.folders.build = "build"
        self.folders.generators = self.folders.build

    def source(self):
        tools.get(f"https://download.savannah.gnu.org/releases/{self.name}/{self.zip_name}",
            sha256="efe71fd4b8246f1b0b1b9bfca13cfff1c9ad85930340c27df469733bbb620938",
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
            self.copy("*.pdb", dst="lib", keep_path=False)
        
    def package_info(self):
        self.cpp_info.includedirs = [os.path.join("include", "freetype2")]
        if self.settings.build_type == "Debug":
            self.cpp_info.libs = ["freetyped"]
        else:
            self.cpp_info.libs = ["freetype"]
