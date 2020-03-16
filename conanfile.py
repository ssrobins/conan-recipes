from conans import ConanFile, CMake, tools
import os

class Conan(ConanFile):
    name = "sdl2"
    version = "2.0.8"
    description = "A cross-platform development library designed to provide low level " \
                  "access to audio, keyboard, mouse, joystick, and graphics hardware " \
                  "via OpenGL and Direct3D."
    homepage = "https://www.libsdl.org"
    license = "Zlib https://www.libsdl.org/license.php"
    url = f"https://gitlab.com/ssrobins/conan-{name}"
    settings = "os", "compiler", "arch"
    generators = "cmake"
    revision_mode = "scm"
    exports_sources = ["CMakeLists.diff", "CMakeLists.txt"]
    zip_folder_name = f"SDL2-{version}"
    zip_name = f"{zip_folder_name}.tar.gz"
    build_subfolder = "build"
    source_subfolder = "source"

    def system_requirements(self):
        if self.settings.os == "Linux":
            installer = tools.SystemPackageTool()
            installer.install("libasound2-dev")

    def build_requirements(self):
        self.build_requires("cmake_utils/0.3.1#d093c585be2418d6a664babbec39e71d6b5cd11d")

    def source(self):
        tools.get(f"https://www.libsdl.org/release/{self.zip_name}")
        os.rename(self.zip_folder_name, self.source_subfolder)
        
        # Apply a patch to the SDL2 CMakeLists.txt file with the following changes:
        # https://bugzilla.libsdl.org/show_bug.cgi?id=4143
        # https://bugzilla.libsdl.org/show_bug.cgi?id=4178
        # https://bugzilla.libsdl.org/show_bug.cgi?id=4194
        # https://bugzilla.libsdl.org/show_bug.cgi?id=4195
        # https://bugzilla.libsdl.org/show_bug.cgi?id=4419
        tools.patch(base_path=self.source_subfolder, patch_file="CMakeLists.diff")

    def build(self):
        from cmake_utils import cmake_init, cmake_build_debug_release
        cmake = cmake_init(self.settings, CMake(self), self.build_folder)
        cmake_build_debug_release(cmake, self.build_subfolder, self.run)

    def package(self):
        from cmake_utils import cmake_init, cmake_install_debug_release
        cmake = cmake_init(self.settings, CMake(self), self.build_folder)
        cmake_install_debug_release(cmake, self.build_subfolder)
        if self.settings.os == "Android":
            self.copy("*.java", dst="android", src=os.path.join(self.source_subfolder, "android-project", "app", "src", "main", "java", "org", "libsdl", "app"))
        elif self.settings.compiler == "Visual Studio":
            self.copy("*.pdb", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.includedirs = [os.path.join("include", "SDL2")]
        self.cpp_info.debug.libs = ["SDL2d", "SDL2maind"]
        self.cpp_info.release.libs = ["SDL2", "SDL2main"]
        if self.settings.os == "Windows":
            self.cpp_info.libs.extend(["imm32", "version", "winmm"])
        if self.settings.os == "Linux":
            system_libs = ["dl", "m", "pthread"]
            self.cpp_info.debug.libs.extend(system_libs)
            self.cpp_info.release.libs.extend(system_libs)
        elif self.settings.os == "Macos":
            self.cpp_info.libs.append("iconv")
            frameworks = ["Cocoa", "Carbon", "IOKit", "CoreVideo", "CoreAudio", "AudioToolbox", "ForceFeedback"]
            for framework in frameworks:
                self.cpp_info.exelinkflags.append(f"-framework {framework}")
        elif self.settings.os == "Android":
            system_libs = ["android", "GLESv2", "log"]
            self.cpp_info.debug.libs.extend(system_libs)
            self.cpp_info.release.libs.extend(system_libs)
        elif self.settings.os == "iOS":
            frameworks = ["AVFoundation", "CoreGraphics", "CoreMotion", "Foundation", "GameController", "Metal", "OpenGLES", "QuartzCore", "UIKit", "CoreVideo", "IOKit", "CoreAudio", "AudioToolbox"]
            for framework in frameworks:
                self.cpp_info.exelinkflags.append(f"-framework {framework}")
        elif self.settings.os == "Android":
            self.cpp_info.libs.extend(["android"])
