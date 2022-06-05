from conan import ConanFile
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain
import os

class Conan(ConanFile):
    name = "sfml"
    version = "2.5.1"
    description = "Simple and fast multimedia library"
    homepage = "https://www.sfml-dev.org/"
    license = "Zlib"
    url = "https://github.com/ssrobins/conan-recipes"
    settings = "os", "arch", "compiler", "build_type"
    generators = "CMakeDeps"
    revision_mode = "scm"
    exports = "cmake_utils.py"
    exports_sources = ["AudioDevice.diff", "CMakeLists.txt"]
    zip_folder_name = f"SFML-{version}"
    zip_name = f"{zip_folder_name}-sources.zip"

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
        self.build_requires("cmake_utils/9.0.1")

    def requirements(self):
        self.requires("freetype/2.12.1")

    @property
    def _source_subfolder(self):
        return "source"

    def layout(self):
        self.folders.build = "build"
        self.folders.generators = self.folders.build

    def source(self):
        tools.get(f"https://www.sfml-dev.org/files/{self.zip_name}",
            destination=self._source_subfolder,
            strip_root=True)

        # Replace auto_ptr with unique_ptr to fix build errors when using the C++17 standard
        tools.patch(base_path=os.path.join(self._source_subfolder, "src", "SFML", "Audio"), patch_file="AudioDevice.diff")

    def generate(self):
        tc = CMakeToolchain(self)
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
