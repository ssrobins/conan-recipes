from conans import ConanFile, CMake, tools
import os


class Conan(ConanFile):
    name = "sdl2"
    version = os.getenv("package_version")
    description = "A cross-platform development library designed to provide low level " \
                  "access to audio, keyboard, mouse, joystick, and graphics hardware " \
                  "via OpenGL and Direct3D."
    homepage = "https://www.libsdl.org"
    license = "Zlib https://www.libsdl.org/license.php"
    url = "https://gitlab.com/ssrobins/conan-" + name
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
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

    def configure_cmake(self):
        generator = None
        if self.settings.os == "Macos" or self.settings.os == "iOS":
            generator = "Xcode"
        cmake = CMake(self, generator=generator)
        if self.settings.os == "Android":
            cmake.definitions["CMAKE_SYSTEM_NAME"] = "Android"
            cmake.definitions["CMAKE_SYSTEM_VERSION"] = os.getenv("android_sdk_version")
            cmake.definitions["CMAKE_ANDROID_ARCH_ABI"] = os.getenv("android_arch_abi")
            cmake.definitions["CMAKE_ANDROID_NDK"] = os.environ['ANDROID_HOME'] + "/android-ndk-" + os.getenv("android_ndk_version")
            cmake.definitions["CMAKE_ANDROID_NDK_TOOLCHAIN_VERSION"] = "clang"
            cmake.definitions["CMAKE_ANDROID_STL_TYPE"] = "c++_static"
        if self.settings.os == "iOS":
            cmake.definitions["CMAKE_TOOLCHAIN_FILE"] = os.path.join(self.build_folder, "ios.toolchain.cmake")
            cmake.definitions["ENABLE_BITCODE"] = "FALSE"
            if self.settings.arch == "x86_64":
                cmake.definitions["IOS_PLATFORM"] = "SIMULATOR64"
            else:
                cmake.definitions["IOS_ARCH"] = "armv7"
        cmake.configure(build_dir=self.build_subfolder)
        return cmake

    def build(self):
        cmake = self.configure_cmake()
        cmake.build()

    def package(self):
        cmake = self.configure_cmake()
        cmake.install()
        if self.settings.os == "Android":
            self.copy("*.java", dst="android", src=os.path.join(self.source_subfolder, 'android-project', 'app', 'src', 'main', 'java', 'org', 'libsdl', 'app'))
        elif self.settings.compiler == 'Visual Studio':
            self.copy(pattern="*.pdb", dst="lib", src=".", keep_path=False)

    def package_info(self):
        self.cpp_info.includedirs = [os.path.join('include', 'SDL2')]
        self.cpp_info.libs = ["SDL2", "SDL2main"]
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
