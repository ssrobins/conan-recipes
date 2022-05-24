from conans import ConanFile, CMake, tools
import os

class Conan(ConanFile):
    name = "libpng"
    version = "1.6.37"
    description = "Official PNG image format reference library"
    homepage = "http://www.libpng.org"
    license = "Libpng http://www.libpng.org/pub/png/src/libpng-LICENSE.txt"
    url = f"https://github.com/ssrobins/conan-{name}"
    settings = "os", "arch", "compiler", "build_type"
    generators = "cmake"
    _cmake = None
    revision_mode = "scm"
    exports_sources = ["CMakeLists.diff", "CMakeLists.txt"]
    zip_folder_name = f"libpng-{version}"
    zip_name = f"{zip_folder_name}.tar.gz"
    build_subfolder = "build"
    source_subfolder = "source"
    maj_min_ver = str().join(version.split(".")[0:2])

    def build_requirements(self):
        self.build_requires("cmake_utils/7.0.0#9bf47716aeee70a8dcfc8592831a0318eb327a09")

    def requirements(self):
        self.requires("zlib/1.2.12#d1cb042e463dd5107bf96584e8ced5e1ffa0c5fa")

    def source(self):
        tools.get(f"https://sourceforge.net/projects/libpng/files/libpng16/{self.version}/{self.zip_name}",
            sha256="daeb2620d829575513e35fecc83f0d3791a620b9b93d800b763542ece9390fb4")
        os.rename(self.zip_folder_name, self.source_subfolder)

        # Apply a patch to the libpng CMakeLists.txt file with the following changes:
        # https://sourceforge.net/p/libpng/code/merge-requests/4/
        # https://github.com/glennrp/libpng/pull/318
        # https://github.com/glennrp/libpng/pull/359
        tools.patch(base_path=self.source_subfolder, patch_file="CMakeLists.diff")

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
        if self.settings.compiler == "msvc":
            self.copy("*.pdb", dst="lib", keep_path=False)

    def package_info(self):
        if self.settings.os == "Windows":
            if self.settings.build_type == "Debug":
                self.cpp_info.libs = [f"libpng{self.maj_min_ver}_staticd"]
            else:
                self.cpp_info.libs = [f"libpng{self.maj_min_ver}_static"]
        else:
            if self.settings.build_type == "Debug":
                self.cpp_info.libs = [f"png{self.maj_min_ver}d"]
            else:
                self.cpp_info.libs = [f"png{self.maj_min_ver}"]
