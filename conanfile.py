from conans import ConanFile, CMake, tools
import os
from cmake_utils import cmake_init, cmake_build_debug_release, cmake_install_debug_release


class Conan(ConanFile):
    name = "sdl2"
    version = os.getenv("package_version")
    description = "A cross-platform development library designed to provide low level " \
                  "access to audio, keyboard, mouse, joystick, and graphics hardware " \
                  "via OpenGL and Direct3D."
    homepage = "https://www.libsdl.org"
    license = "Zlib https://www.libsdl.org/license.php"
    url = "https://gitlab.com/ssrobins/conan-" + name
    settings = "os", "compiler", "arch"
    generators = "cmake"
    exports = "cmake_utils.py"
    exports_sources = ["CMakeLists.diff", "CMakeLists.txt"]
    zip_folder_name = "SDL2-%s" % version
    zip_name = "%s.tar.gz" % zip_folder_name
    build_subfolder = "build"
    source_subfolder = "source"

    def source(self):
        tools.download("https://gitlab.com/ssrobins/cmake-utils/raw/master/global_settings.cmake", "global_settings.cmake")
        tools.download("https://gitlab.com/ssrobins/cmake-utils/raw/master/ios.toolchain.cmake", "ios.toolchain.cmake")
        tools.download("https://www.libsdl.org/release/%s" % self.zip_name, self.zip_name)
        tools.unzip(self.zip_name)
        os.unlink(self.zip_name)
        os.rename(self.zip_folder_name, self.source_subfolder)
        
        # Apply a patch to the SDL2 CMakeLists.txt file with the following changes:
        # https://bugzilla.libsdl.org/show_bug.cgi?id=4143
        # https://bugzilla.libsdl.org/show_bug.cgi?id=4178
        # https://bugzilla.libsdl.org/show_bug.cgi?id=4194
        # https://bugzilla.libsdl.org/show_bug.cgi?id=4195
        # https://bugzilla.libsdl.org/show_bug.cgi?id=4419
        tools.patch(base_path=self.source_subfolder, patch_file="CMakeLists.diff")

    def build(self):
        cmake = cmake_init(self.settings, CMake(self), self.build_folder)
        cmake_build_debug_release(cmake, self.build_subfolder)

    def package(self):
        cmake = cmake_init(self.settings, CMake(self), self.build_folder)
        cmake_install_debug_release(cmake, self.build_subfolder)
        if self.settings.os == "Android":
            self.copy("*.java", dst="android", src=os.path.join(self.source_subfolder, 'android-project', 'app', 'src', 'main', 'java', 'org', 'libsdl', 'app'))
        elif self.settings.compiler == 'Visual Studio':
            self.copy(pattern="*.pdb", dst="lib", src=".", keep_path=False)

    def package_info(self):
        self.cpp_info.includedirs = [os.path.join('include', 'SDL2')]
        self.cpp_info.debug.libs = ["SDL2d", "SDL2maind"]
        self.cpp_info.release.libs = ["SDL2", "SDL2main"]
        if self.settings.os == "Windows":
            self.cpp_info.libs.extend(["imm32", "version", "winmm"])
        if self.settings.os == "Linux":
            self.cpp_info.libs.extend(['dl', 'm', 'pthread'])
        elif self.settings.os == "Macos":
            self.cpp_info.libs.append('iconv')
            frameworks = ['Cocoa', 'Carbon', 'IOKit', 'CoreVideo', 'CoreAudio', 'AudioToolbox', 'ForceFeedback']
            for framework in frameworks:
                self.cpp_info.exelinkflags.append("-framework %s" % framework)
        elif self.settings.os == "iOS":
            frameworks = ['AVFoundation', 'CoreGraphics', 'CoreMotion', 'Foundation', 'GameController', 'Metal', 'OpenGLES', 'QuartzCore', 'UIKit', 'CoreVideo', 'IOKit', 'CoreAudio', 'AudioToolbox']
            for framework in frameworks:
                self.cpp_info.exelinkflags.append("-framework %s" % framework)
        elif self.settings.os == "Android":
            self.cpp_info.libs.extend(['android'])
