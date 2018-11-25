from conans import ConanFile, CMake, tools
import os


class Conan(ConanFile):
    name = "googletest"
    version = os.getenv("package_version")
    url = "https://gitlab.com/ssrobins/conan-" + name
    description = ""
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    exports_sources = ["CMakeLists.txt"]
    zip_folder_name = "googletest-master"
    zip_name = "master.zip"
    build_subfolder = "build"
    source_subfolder = "source"

    def source(self):
        tools.download("https://gitlab.com/ssrobins/cmake-utils/raw/master/global_settings.cmake", "global_settings.cmake")
        if self.settings.os == "iOS":
            tools.download("https://gitlab.com/ssrobins/cmake-utils/raw/master/ios.toolchain.cmake", "ios.toolchain.cmake")
        tools.download("https://github.com/abseil/googletest/archive/%s" % self.zip_name, self.zip_name)
        tools.unzip(self.zip_name)
        os.unlink(self.zip_name)
        os.rename(self.zip_folder_name, self.source_subfolder)

    def configure_cmake(self):
        generator = None
        if self.settings.os == "Macos" or self.settings.os == "iOS":
            generator = "Xcode"
        cmake = CMake(self, generator=generator)
        cmake.definitions["SDL_SHARED"] = "OFF"
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
        cmake.configure(build_dir=self.build_subfolder)
        return cmake

    def build(self):
        cmake = self.configure_cmake()
        cmake.build()