from conans import ConanFile, CMake, tools
from conans.util import files
import os

class Conan(ConanFile):
    name = "zlib"
    version = "1.2.12"
    description = "A Massively Spiffy Yet Delicately Unobtrusive Compression Library " \
                  "(Also Free, Not to Mention Unencumbered by Patents)"
    homepage = "https://zlib.net/"
    license = "Zlib"
    url = f"https://github.com/ssrobins/conan-{name}"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"
    _cmake = None
    revision_mode = "scm"
    exports_sources = ["CMakeLists.diff", "CMakeLists.txt"]
    zip_folder_name = f"{name}-{version}"
    zip_name = f"{zip_folder_name}.tar.gz"
    build_subfolder = "build"
    source_subfolder = "source"

    def build_requirements(self):
        self.build_requires("cmake_utils/7.0.0#9bf47716aeee70a8dcfc8592831a0318eb327a09")

    def source(self):
        tools.get(f"https://zlib.net/{self.zip_name}",
            sha256="91844808532e5ce316b3c010929493c0244f3d37593afd6de04f71821d5136d9")
        os.rename(self.zip_folder_name, self.source_subfolder)

    def _configure_cmake(self):
        if self._cmake:
            return self._cmake
        self._cmake = CMake(self)
        if self.settings.os != "Windows":
            self._cmake.generator = "Ninja Multi-Config"
        if self.settings.os == "Android":
            self._cmake.definitions["CMAKE_TOOLCHAIN_FILE"] = os.getenv("ANDROID_NDK_ROOT") + "/build/cmake/android.toolchain.cmake"
        elif self.settings.os == "iOS" and self.settings.arch != "x86_64":
            self._cmake.definitions["CMAKE_OSX_ARCHITECTURES"] = "armv7;arm64"
        elif self.settings.os == "Windows" and self.settings.arch == "x86":
            self._cmake.generator_platform = "Win32"
        self._cmake.configure(build_dir=self.build_subfolder)
        return self._cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build(args=["--verbose"])
        with tools.chdir(self.build_subfolder):
            self.run(f"ctest -C {self.settings.build_type} --output-on-failure")
        cmake.install()

    def package(self):
        self.copy("*.h", dst="include", src=self.source_subfolder)
        self.copy("*.h", dst="include", src=self.build_folder, keep_path=False)
        self.copy("build/lib/zlibstatic*.lib", dst="lib", keep_path=False)
        self.copy("build/lib/*.a", dst="lib", keep_path=False)
        if self.settings.compiler == "msvc":
            self.copy("*.pdb", dst="lib", keep_path=False)

    def package_info(self):
        if self.settings.os == "Windows" and not tools.os_info.is_linux:
            if self.settings.build_type == "Debug":
                self.cpp_info.libs = ["zlibstaticd"]
            else:
                self.cpp_info.libs = ["zlibstatic"]
        else:
            if self.settings.build_type == "Debug":
                self.cpp_info.libs = ["zd"]
            else:
                self.cpp_info.libs = ["z"]
