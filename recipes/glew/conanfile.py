from conan import ConanFile
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain
from conan.tools.files import copy, get, patch
from conan.tools.system.package_manager import Apt
import os

required_conan_version = ">=2.0.4"

class Conan(ConanFile):
    name = "glew"
    version = "2.2.0"
    description = "OpenGL extension wrangler library"
    homepage = "https://github.com/nigels-com/glew"
    license = "https://github.com/nigels-com/glew/blob/master/LICENSE.txt"
    url = "https://github.com/ssrobins/conan-recipes"
    settings = "os", "arch", "compiler", "build_type"
    exports_sources = ["CMakeLists.txt"]
    zip_folder_name = f"{name}-{version}"
    zip_name = f"{zip_folder_name}.tgz"

    def system_requirements(self):
        if self.settings.os == "Linux":
            Apt(self).install(["freeglut3-dev"],
                update=True, check=True)

    @property
    def _source_subfolder(self):
        return "source"

    def layout(self):
        self.folders.build = "build"
        self.folders.generators = self.folders.build

    def source(self):
        get(self,
            f"https://github.com/nigels-com/glew/releases/download/{self.zip_folder_name}/{self.zip_name}",
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
        if self.settings.os == "Windows":
            if self.settings.build_type == "Debug":
                self.cpp_info.libs = ["libglew32d"]
            else:
                self.cpp_info.libs = ["libglew32"]
            self.cpp_info.system_libs.append("OpenGL32")
            self.cpp_info.defines.append("GLEW_STATIC")
        elif self.settings.os == "Macos":
            if self.settings.build_type == "Debug":
                self.cpp_info.libs = ["GLEWd"]
            else:
                self.cpp_info.libs = ["GLEW"]
            self.cpp_info.frameworks.append("OpenGL")
        else:
            if self.settings.build_type == "Debug":
                self.cpp_info.libs = ["GLEWd"]
            else:
                self.cpp_info.libs = ["GLEW"]
            self.cpp_info.system_libs.append("GL")
