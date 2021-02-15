from conans import ConanFile, CMake, tools
import os

class Conan(ConanFile):
    name = "freetype"
    version = "2.10.4"
    description = "Freely available software library to render fonts"
    homepage = "https://www.freetype.org/"
    license = "FTL https://www.freetype.org/license.html"
    url = f"https://github.com/ssrobins/conan-{name}"
    settings = "os", "compiler", "arch"
    generators = "cmake"
    revision_mode = "scm"
    exports_sources = ["CMakeLists.txt"]
    zip_folder_name = f"{name}-{version}"
    zip_name = f"{zip_folder_name}.tar.gz"
    build_subfolder = "build"
    source_subfolder = "source"

    def build_requirements(self):
        self.build_requires("cmake_utils/0.3.1#e474aafdec36cf92d97e781b844f390f3170f29f")

    def requirements(self):
        self.requires("bzip2/1.0.8#fcc0057da64dcfde6d56d74659c747ad50f0c982")
        self.requires("libpng/1.6.37#5aacf06d4d920ac2d009fad060837fc30a0e02a9")
        self.requires("zlib/1.2.11#fd869827da9c3bc571dc553e945489ec276e72a6")

    def source(self):
        tools.get(f"http://dnqpy.com/libs/{self.zip_name}")
        os.rename(self.zip_folder_name, self.source_subfolder)

    def build(self):
        from cmake_utils import cmake_init, cmake_build_debug_release
        cmake = cmake_init(self.settings, CMake(self), self.build_folder)
        cmake_build_debug_release(cmake, self.build_subfolder, self.run)

    def package(self):
        from cmake_utils import cmake_init, cmake_install_debug_release
        cmake = cmake_init(self.settings, CMake(self), self.build_folder)
        cmake_install_debug_release(cmake, self.build_subfolder)
        if self.settings.compiler == "Visual Studio":
            self.copy("*.pdb", dst="lib", keep_path=False)
        
    def package_info(self):
        self.cpp_info.includedirs = [os.path.join("include", "freetype2")]
        self.cpp_info.debug.libs = ["freetyped"]
        self.cpp_info.release.libs = ["freetype"]
