from conans import ConanFile, CMake, tools
import os

class Conan(ConanFile):
    name = "vorbis"
    version = "1.3.7"
    description = "General-purpose compressed audio format for mid to high quality audio and music"
    homepage = "https://xiph.org/vorbis/"
    license = "BSD license"
    url = f"https://github.com/ssrobins/conan-{name}"
    settings = "os", "arch", "compiler", "build_type"
    generators = "cmake", "cmake_find_package_multi"
    _cmake = None
    revision_mode = "scm"
    exports_sources = ["CMakeLists.txt"]
    zip_folder_name = f"lib{name}-{version}"
    zip_name = f"{zip_folder_name}.tar.xz"
    build_subfolder = "build"
    source_subfolder = "source"

    def build_requirements(self):
        self.build_requires("cmake_utils/7.0.0#9bf47716aeee70a8dcfc8592831a0318eb327a09")

    def requirements(self):
        self.requires("ogg/1.3.5#85a67c96e8fe063a9a33ee51d6c23daf0a686b19")

    def source(self):
        tools.get(f"https://downloads.xiph.org/releases/{self.name}/{self.zip_name}")
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
        self.copy("include/*.h", dst=".", src=self.source_subfolder)
        self.copy("*.lib", dst="lib", src=self.build_subfolder, keep_path=False)
        self.copy("build/lib/*.a", dst="lib", keep_path=False)
        if self.settings.compiler == "msvc":
            self.copy("*.pdb", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.includedirs = ["include"]
        if self.settings.build_type == "Debug":
            self.cpp_info.libs = ["vorbisfiled", "vorbisencd", "vorbisd"]
        else:
            self.cpp_info.libs = ["vorbisfile", "vorbisenc", "vorbis"]
