from conan import ConanFile
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain
from conan.tools.files import copy, get
from conan.tools.system.package_manager import Apt
import os

required_conan_version = ">=2.0.0-beta1"

class Conan(ConanFile):
    name = "sdl"
    version = "2.26.1"
    description = "A cross-platform development library designed to provide low level " \
                  "access to audio, keyboard, mouse, joystick, and graphics hardware " \
                  "via OpenGL and Direct3D."
    homepage = "https://www.libsdl.org"
    license = "Zlib https://www.libsdl.org/license.php"
    url = "https://github.com/ssrobins/conan-recipes"
    settings = "os", "arch", "compiler", "build_type"
    generators = "CMakeDeps"
    revision_mode = "scm"
    exports_sources = ["CMakeLists.txt"]
    zip_folder_name = f"SDL2-{version}"
    zip_name = f"{zip_folder_name}.tar.gz"

    def system_requirements(self):
        if self.settings.os == "Linux":
            Apt(self).install(["libasound2-dev"],
                update=True, check=True)

    @property
    def _source_subfolder(self):
        return "source"

    def layout(self):
        self.folders.build = "build"
        self.folders.generators = self.folders.build

    def source(self):
        get(self,
            f"https://www.libsdl.org/release/{self.zip_name}",
            destination=self._source_subfolder,
            strip_root=True)

    def generate(self):
        tc = CMakeToolchain(self)
        if self.settings.os != "Windows":
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

    def package(self):
        cmake = CMake(self)
        cmake.install()
        if self.settings.os == "Android":
            copy(self, "*.java",
                os.path.join(self.source_folder, self._source_subfolder, "android-project", "app", "src", "main", "java", "org", "libsdl", "app"),
                os.path.join(self.package_folder, "android"))
        elif self.settings.compiler == "msvc":
            copy(self, "*.pdb",
                self.build_folder,
                os.path.join(self.package_folder, "lib"),
                keep_path=False)

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "SDL2")
        self.cpp_info.set_property("cmake_target_name", "SDL2::SDL2-static")
        self.cpp_info.includedirs = [os.path.join("include", "SDL2")]
        debug_suffix = ""
        if self.settings.build_type == "Debug":
            debug_suffix = "d"
        windows_suffix = ""
        if self.settings.os == "Windows":
            windows_suffix = "-static"
        self.cpp_info.libs = [f"SDL2{windows_suffix}{debug_suffix}", f"SDL2main{debug_suffix}"]
        if self.settings.os == "Android":
            self.cpp_info.system_libs.extend(["android", "GLESv1_CM", "GLESv2", "log", "OpenSLES"])
        elif self.settings.os == "iOS":
            self.cpp_info.system_libs.append("iconv")
            self.cpp_info.frameworks.extend([
                "AudioToolbox",
                "AVFoundation",
                "CoreAudio",
                "CoreBluetooth",
                "CoreGraphics",
                "CoreHaptics",
                "CoreMotion",
                "CoreVideo",
                "Foundation",
                "GameController",
                "IOKit",
                "Metal",
                "OpenGLES",
                "QuartzCore",
                "UIKit"])
        elif self.settings.os == "Macos":
            self.cpp_info.system_libs.append("iconv")
            self.cpp_info.frameworks.extend([
                "AudioToolbox",
                "Carbon",
                "Cocoa",
                "CoreAudio",
                "CoreHaptics",
                "CoreVideo",
                "ForceFeedback",
                "GameController",
                "IOKit",
                "Metal"])
        elif self.settings.os == "Linux":
            self.cpp_info.system_libs.extend(["dl", "m", "pthread"])
        elif self.settings.os == "Windows":
            self.cpp_info.system_libs.extend(["Imm32", "SetupAPI", "Version", "WinMM"])
