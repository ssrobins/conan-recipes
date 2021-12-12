from conans import ConanFile, CMake, tools
import os

class Conan(ConanFile):
    name = "ogg"
    version = "1.3.5"
    description = "Multimedia container format for Xiph.org multimedia codecs"
    homepage = "https://xiph.org/ogg/"
    license = "BSD license"
    url = f"https://github.com/ssrobins/conan-{name}"
    settings = "os", "compiler", "arch"
    generators = "cmake"
    revision_mode = "scm"
    exports_sources = ["CMakeLists.txt"]
    zip_folder_name = f"lib{name}-{version}"
    zip_name = f"{zip_folder_name}.tar.xz"
    build_subfolder = "build"
    source_subfolder = "source"

    def build_requirements(self):
        self.build_requires("cmake_utils/5.1.0#2c0d8f9dda3cac137976849bb3851fd6c4999de0")

    def source(self):
        tools.get(f"https://downloads.xiph.org/releases/{self.name}/{self.zip_name}")
        os.rename(self.zip_folder_name, self.source_subfolder)

    def build(self):
        from cmake_utils import cmake_init, cmake_build_debug_release
        cmake = cmake_init(self.settings, CMake(self), self.build_folder)
        cmake_build_debug_release(cmake, self.build_subfolder, self.run)

    def package(self):
        self.copy("include/*.h", dst=".", src=self.source_subfolder)
        self.copy("*.lib", dst="lib", src=self.build_subfolder, keep_path=False)
        self.copy("build/lib/*.a", dst="lib", keep_path=False)
        if self.settings.compiler == "msvc":
            self.copy("*.pdb", dst="lib", keep_path=False)
        
    def package_info(self):
        self.cpp_info.includedirs = [os.path.join("include", "ogg")]
        self.cpp_info.debug.libs = ["oggd"]
        self.cpp_info.release.libs = ["ogg"]
