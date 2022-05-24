from conans import ConanFile, CMake, tools
import os

class Conan(ConanFile):
    name = "gtest"
    version = "1.11.0"
    description = "Google's C++ test framework"
    homepage = "https://github.com/google/googletest"
    license = "BSD-3-Clause"
    url = f"https://github.com/ssrobins/conan-{name}"
    settings = "os", "arch", "compiler", "build_type"
    generators = "cmake"
    _cmake = None
    revision_mode = "scm"
    exports_sources = ["CMakeLists.txt"]
    zip_folder_name = f"googletest-release-{version}"
    zip_name = f"release-{version}.tar.gz"
    build_subfolder = "build"
    source_subfolder = "source"

    def build_requirements(self):
        self.build_requires("cmake_utils/7.0.0#9bf47716aeee70a8dcfc8592831a0318eb327a09")

    def source(self):
        tools.get(f"https://github.com/google/googletest/archive/{self.zip_name}")
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

    def package(self):
        self.copy("*.h", dst="include/gtest", src=os.path.join(self.source_subfolder, "googletest", "include", "gtest"))
        self.copy("*.h", dst="include/gmock", src=os.path.join(self.source_subfolder, "googlemock", "include", "gmock"))
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("build/lib/*.a", dst="lib", keep_path=False)
        if self.settings.compiler == "msvc":
            self.copy("*.pdb", dst="lib", keep_path=False)

    def package_info(self):
        if self.settings.build_type == "Debug":
            self.cpp_info.libs = ["gmock_maind", "gmockd", "gtest_maind", "gtestd"]
        else:
            self.cpp_info.libs = ["gmock_main", "gmock", "gtest_main", "gtest"]
        if self.settings.os == "Linux":
            self.cpp_info.system_libs.append("pthread")
