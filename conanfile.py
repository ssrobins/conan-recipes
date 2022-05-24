from conans import ConanFile, CMake, tools
import os

class Conan(ConanFile):
    name = "freetype"
    version = "2.12.1"
    description = "Freely available software library to render fonts"
    homepage = "https://www.freetype.org/"
    license = "FTL https://www.freetype.org/license.html"
    url = f"https://github.com/ssrobins/conan-{name}"
    settings = "os", "arch", "compiler", "build_type"
    generators = "cmake"
    _cmake = None
    revision_mode = "scm"
    exports_sources = ["CMakeLists.txt"]
    zip_folder_name = f"{name}-{version}"
    zip_name = f"{zip_folder_name}.tar.gz"
    build_subfolder = "build"
    source_subfolder = "source"

    def build_requirements(self):
        self.build_requires("cmake_utils/7.0.0#9bf47716aeee70a8dcfc8592831a0318eb327a09")

    def requirements(self):
        self.requires("bzip2/1.0.8#1b33da2d177250fe500bd4506de0d2a4175dbbc3")
        self.requires("libpng/1.6.37#4c5a09a29b076718e8031c3e3a01aab7b30f4644")
        self.requires("zlib/1.2.12#d1cb042e463dd5107bf96584e8ced5e1ffa0c5fa")

    def source(self):
        tools.get(f"https://download.savannah.gnu.org/releases/{self.name}/{self.zip_name}",
            sha256="efe71fd4b8246f1b0b1b9bfca13cfff1c9ad85930340c27df469733bbb620938")
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
        if self.settings.compiler == "msvc":
            self.copy("*.pdb", dst="lib", keep_path=False)
        
    def package_info(self):
        self.cpp_info.includedirs = [os.path.join("include", "freetype2")]
        if self.settings.build_type == "Debug":
            self.cpp_info.libs = ["freetyped"]
        else:
            self.cpp_info.libs = ["freetype"]
