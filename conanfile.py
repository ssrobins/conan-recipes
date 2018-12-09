from conans import ConanFile, CMake, tools
import os, shutil


class Conan(ConanFile):
    name = "sdl2_mixer"
    version = os.getenv("package_version")
    url = "https://gitlab.com/ssrobins/conan-" + name
    description = ""
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    exports_sources = "CMakeLists.txt"
    zip_folder_name = "SDL2_mixer-%s" % version
    zip_name = "%s.tar.gz" % zip_folder_name
    
    def requirements(self):
        self.requires.add("sdl2/2.0.9@stever/testing")

    def source(self):
        tools.download("https://gitlab.com/ssrobins/cmake-utils/raw/master/global_settings.cmake", "global_settings.cmake")
        tools.download("https://gitlab.com/ssrobins/cmake-utils/raw/master/ios.toolchain.cmake", "ios.toolchain.cmake")
        tools.download("https://www.libsdl.org/projects/SDL_mixer/release/%s" % self.zip_name, self.zip_name)
        tools.unzip(self.zip_name)
        os.unlink(self.zip_name)
        shutil.move(self.exports_sources, self.zip_folder_name)

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
        cmake.configure(source_folder=self.zip_folder_name)
        return cmake

    def build(self):
        cmake = self.configure_cmake()
        cmake.build()

    def package(self):
        if self.settings.compiler == 'Visual Studio':
            self.copy(pattern="*.pdb", dst="lib", src=".", keep_path=False)
