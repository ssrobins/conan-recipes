from conans import ConanFile, CMake, tools
import os

class Conan(ConanFile):
    name = "libpng"
    version = "1.6.37"
    description = "Official PNG image format reference library"
    homepage = "http://www.libpng.org"
    license = "Libpng http://www.libpng.org/pub/png/src/libpng-LICENSE.txt"
    url = f"https://gitlab.com/ssrobins/conan-{name}"
    settings = "os", "compiler", "arch"
    generators = "cmake"
    revision_mode = "scm"
    exports_sources = ["CMakeLists.diff", "CMakeLists.txt"]
    zip_folder_name = f"libpng-{version}"
    zip_name = f"{zip_folder_name}.tar.gz"
    build_subfolder = "build"
    source_subfolder = "source"
    maj_min_ver = str().join(version.split(".")[0:2])

    def build_requirements(self):
        self.build_requires("cmake_utils/0.3.1#b92e3b563e31a4fe0e55849f3bfdb55eb7b06284")

    def requirements(self):
        self.requires("zlib/1.2.11#4def8af360413cf604268e17f1dc6cf33a9706db")

    def source(self):
        tools.get(f"http://dnqpy.com/libs/{self.zip_name}",
            sha256="daeb2620d829575513e35fecc83f0d3791a620b9b93d800b763542ece9390fb4")
        os.rename(self.zip_folder_name, self.source_subfolder)

        # Apply a patch to the libpng CMakeLists.txt file with the following changes:
        # https://sourceforge.net/p/libpng/code/merge-requests/4/
        # https://github.com/glennrp/libpng/pull/318
        tools.patch(base_path=self.source_subfolder, patch_file="CMakeLists.diff")

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
        if self.settings.os == "Windows":
            self.cpp_info.debug.libs = [f"libpng{self.maj_min_ver}_staticd"]
            self.cpp_info.release.libs = [f"libpng{self.maj_min_ver}_static"]
        else:
            self.cpp_info.debug.libs = [f"png{self.maj_min_ver}d"]
            self.cpp_info.release.libs = [f"png{self.maj_min_ver}"]
