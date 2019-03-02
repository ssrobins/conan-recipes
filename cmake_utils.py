import os, shutil

def cmake_init(settings, cmake, build_folder):
    if settings.os == "Android":
        cmake.definitions["ANDROID_ABI"] = os.getenv("android_arch_abi")
        cmake.definitions["ANDROID_TOOLCHAIN"] = "clang"
        cmake.definitions["ANDROID_STL"] = "c++_static"
        cmake.definitions["CMAKE_TOOLCHAIN_FILE"] = os.environ["ANDROID_HOME"] + "/android-ndk-" + \
            os.getenv("android_ndk_version") + "/build/cmake/android.toolchain.cmake"
    elif settings.os == "iOS":
        cmake.generator = "Xcode"
        cmake.definitions["CMAKE_TOOLCHAIN_FILE"] = os.path.join(build_folder, "ios.toolchain.cmake")
        cmake.definitions["ENABLE_BITCODE"] = "FALSE"
        if settings.arch == "x86_64":
            cmake.definitions["IOS_PLATFORM"] = "SIMULATOR64"
        else:
            cmake.definitions["IOS_ARCH"] = "armv7 arm64"
    elif settings.os == "Macos":
        cmake.generator = "Xcode"
    return cmake

def configure_cmake(cmake, build_subfolder, config=None):
    if config:
        cmake.definitions["CMAKE_BUILD_TYPE"] = config
    cmake.configure(build_dir=build_subfolder)

def cmake_build_debug_release(cmake, build_subfolder):
    if cmake.is_multi_configuration:
        configure_cmake(cmake, build_subfolder)
        cmake.build(args=["--config", "Debug"])
        cmake.build(args=["--config", "Release"])
    else:
        for config in ("Debug", "Release"):
            configure_cmake(cmake, build_subfolder, config)
            cmake.build()
            shutil.rmtree(os.path.join(build_subfolder, "CMakeFiles"))
            os.remove(os.path.join(build_subfolder, "CMakeCache.txt"))

def cmake_install_debug_release(cmake, build_subfolder):
    if cmake.is_multi_configuration:
        configure_cmake(cmake, build_subfolder)
        cmake.install(args=["--config", "Debug"])
        cmake.install(args=["--config", "Release"])
    else:
        for config in ("Debug", "Release"):
            configure_cmake(cmake, build_subfolder, config)
            cmake.install()
            shutil.rmtree(os.path.join(build_subfolder, "CMakeFiles"))
            os.remove(os.path.join(build_subfolder, "CMakeCache.txt"))
