from conans import ConanFile, CMake, tools
from conans.util import files
import os


class SDL2Conan(ConanFile):
    name = "sdl2"
    version = os.getenv("package_version")
    license = "Zlib"
    url = "https://gitlab.com/ssrobins/conan-sdl2"
    description = "A cross-platform development library designed to provide low level " \
                  "access to audio, keyboard, mouse, joystick, and graphics hardware " \
                  "via OpenGL and Direct3D."
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"
    exports_sources = "CMakeLists.diff"
    zip_folder_name = "SDL2-%s" % version
    zip_name = "%s.tar.gz" % zip_folder_name

    def source(self):
        tools.download("https://gitlab.com/ssrobins/cmake-utils/raw/master/global_settings.cmake?inline=false", "global_settings.cmake")
        tools.download("https://www.libsdl.org/release/%s" % self.zip_name, self.zip_name)
        tools.unzip(self.zip_name)
        os.unlink(self.zip_name)
        tools.patch(base_path=self.zip_folder_name, patch_file="CMakeLists.diff")
        tools.replace_in_file("%s/CMakeLists.txt" % self.zip_folder_name, "conan_basic_setup()",
                              '''include(${CMAKE_BINARY_DIR}/global_settings.cmake)
conan_basic_setup()''')

    def configure_cmake(self):
        generator = None
        if self.settings.os == "Macos" and self.settings.arch == "x86_64":
            generator = "Xcode"
        cmake = CMake(self, generator=generator)
        cmake.definitions["SDL_SHARED"] = "OFF"
        if self.settings.arch == "armv7":
            cmake.definitions["CMAKE_SYSTEM_NAME"] = "Android"
            cmake.definitions["CMAKE_SYSTEM_VERSION"] = "28"
            cmake.definitions["CMAKE_ANDROID_ARCH_ABI"] = "armeabi-v7a"
            cmake.definitions["CMAKE_ANDROID_NDK"] = os.environ['ANDROID_HOME'] + "/android-ndk-r18b"
            cmake.definitions["CMAKE_ANDROID_NDK_TOOLCHAIN_VERSION"] = "clang"
            cmake.definitions["CMAKE_ANDROID_STL_TYPE"] = "c++_static"
        cmake.configure(source_folder=self.zip_folder_name)
        return cmake

    def build(self):
        cmake = self.configure_cmake()
        cmake.build()

    def package(self):
        cmake = self.configure_cmake()
        cmake.install()
        if self.settings.arch == "armv7":
            self.copy("*.java", dst="android", src=os.path.join(self.zip_folder_name, 'android-project', 'app', 'src', 'main', 'java', 'org', 'libsdl', 'app'))

    def package_info(self):
        self.cpp_info.includedirs = [os.path.join('include', 'SDL2')]
        self.cpp_info.libs = ["SDL2", "SDL2main"]
        if self.settings.os == "Windows":
            self.cpp_info.libs.extend(["imm32", "version", "winmm"])
        if self.settings.os == "Linux" and self.settings.arch == "x86_64":
            self.cpp_info.libs.extend(['dl', 'm', 'pthread'])
        elif self.settings.os == "Macos" and self.settings.arch == "x86_64":
            self.cpp_info.libs.append('iconv')
            frameworks = ['Cocoa', 'Carbon', 'IOKit', 'CoreVideo', 'CoreAudio', 'AudioToolbox', 'ForceFeedback']
            for framework in frameworks:
                self.cpp_info.exelinkflags.append("-framework %s" % framework)
        elif self.settings.arch == "armv7":
            self.cpp_info.libs.extend(['android'])
