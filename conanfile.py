from conans import ConanFile, CMake, tools
import os

class Conan(ConanFile):
    name = "sfml"
    version = "2.5.1"
    description = "Simple and fast multimedia library"
    homepage = "https://www.sfml-dev.org/"
    license = "Zlib"
    url = f"https://github.com/ssrobins/conan-{name}"
    settings = "os", "arch", "compiler", "build_type"
    generators = "cmake"
    _cmake = None
    revision_mode = "scm"
    exports = "cmake_utils.py"
    exports_sources = ["AudioDevice.diff", "CMakeLists.txt"]
    zip_folder_name = f"SFML-{version}"
    zip_name = f"{zip_folder_name}-sources.zip"
    build_subfolder = "build"
    source_subfolder = "source"

    def system_requirements(self):
        if self.settings.os == "Linux":
            installer = tools.SystemPackageTool()
            installer.install("libflac-dev")
            installer.install("libgl1-mesa-dev")
            installer.install("libopenal-dev")
            installer.install("libudev-dev")
            installer.install("libvorbis-dev")
            installer.install("libxrandr-dev")

    def build_requirements(self):
        self.build_requires("cmake_utils/7.0.0#9bf47716aeee70a8dcfc8592831a0318eb327a09")

    def requirements(self):
        self.requires("freetype/2.12.1#2e35e973e17761add823680b306153d36c0f16d0")

    def source(self):
        tools.get(f"https://www.sfml-dev.org/files/{self.zip_name}")
        os.rename(self.zip_folder_name, self.source_subfolder)

        # Replace auto_ptr with unique_ptr to fix build errors when using the C++17 standard
        tools.patch(base_path=os.path.join(self.source_subfolder, "src", "SFML", "Audio"), patch_file="AudioDevice.diff")

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
        if self.settings.build_type == "Debug":
            self.cpp_info.libs = ["sfml-graphics-s-d", "sfml-window-s-d", "sfml-system-s-d"]
        else:
            self.cpp_info.libs = ["sfml-graphics-s", "sfml-window-s", "sfml-system-s"]
        if self.settings.os == "Windows":
            if self.settings.build_type == "Debug":
                self.cpp_info.libs.append("sfml-main-d")
            else:
                self.cpp_info.libs.append("sfml-main")
            self.cpp_info.system_libs.extend(["opengl32", "winmm"])
        elif self.settings.os == "Linux":
            self.cpp_info.system_libs.extend(["GL", "pthread", "udev", "X11", "Xrandr"])
        elif self.settings.os == "Macos":
            self.cpp_info.frameworks.extend([
                "Carbon",
                "Cocoa",
                "CoreFoundation",
                "CoreGraphics",
                "IOKit",
                "OpenGL"])
            self.cpp_info.exelinkflags.append("-ObjC")
        self.cpp_info.defines = ["SFML_STATIC"]
