from conans import ConanFile, tools
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain
import os

class Conan(ConanFile):
    name = "sdl2"
    version = "2.0.22"
    description = "A cross-platform development library designed to provide low level " \
                  "access to audio, keyboard, mouse, joystick, and graphics hardware " \
                  "via OpenGL and Direct3D."
    homepage = "https://www.libsdl.org"
    license = "Zlib https://www.libsdl.org/license.php"
    url = f"https://github.com/ssrobins/conan-{name}"
    settings = "os", "arch", "compiler", "build_type"
    generators = "CMakeDeps"
    revision_mode = "scm"
    exports_sources = ["CMakeLists.txt"]
    zip_folder_name = f"SDL2-{version}"
    zip_name = f"{zip_folder_name}.tar.gz"

    def system_requirements(self):
        if self.settings.os == "Linux":
            installer = tools.SystemPackageTool()
            installer.install("libasound2-dev")

    def build_requirements(self):
        self.build_requires("cmake_utils/7.0.0#9bf47716aeee70a8dcfc8592831a0318eb327a09")

    @property
    def _source_subfolder(self):
        return "source"

    def layout(self):
        self.folders.build = "build"
        self.folders.generators = self.folders.build

    def source(self):
        tools.get(f"https://www.libsdl.org/release/{self.zip_name}",
            destination=self._source_subfolder,
            strip_root=True)

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
        if self.settings.os == "Android":
            self.copy("*.java", dst="android", src=os.path.join(self._source_subfolder, "android-project", "app", "src", "main", "java", "org", "libsdl", "app"))
        elif self.settings.compiler == "msvc":
            self.copy("*.pdb", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.includedirs = [os.path.join("include", "SDL2")]
        if self.settings.build_type == "Debug":
            self.cpp_info.libs = ["SDL2d", "SDL2maind"]
        else:
            self.cpp_info.libs = ["SDL2", "SDL2main"]
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
