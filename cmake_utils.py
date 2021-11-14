import os, shutil
from conans import tools

def cmake_init(settings, cmake, build_folder):
    if settings.os == "Android":
        cmake.generator = "Ninja Multi-Config"
        if settings.arch == "armv7":
            cmake.definitions["ANDROID_ABI"] = "armeabi-v7a"
        elif settings.arch == "armv8":
            cmake.definitions["ANDROID_ABI"] = "arm64-v8a"
        cmake.definitions["ANDROID_TOOLCHAIN"] = "clang"
        cmake.definitions["ANDROID_STL"] = "c++_static"
        cmake.definitions["CMAKE_TOOLCHAIN_FILE"] = os.getenv("ANDROID_NDK_ROOT") + "/build/cmake/android.toolchain.cmake"
    elif settings.os == "iOS":
        cmake.generator = "Xcode"
        cmake.definitions["CMAKE_SYSTEM_NAME"] = "iOS"
        if settings.os.version:
            cmake.definitions["CMAKE_OSX_DEPLOYMENT_TARGET"] = settings.os.version
        if settings.arch == "x86_64":
            cmake.definitions["CMAKE_OSX_ARCHITECTURES"] = "x86_64"
        else:
            cmake.definitions["CMAKE_OSX_ARCHITECTURES"] = "armv7 arm64"
        cmake.definitions["CMAKE_TRY_COMPILE_TARGET_TYPE"] = "STATIC_LIBRARY"
    elif settings.os == "Linux":
        cmake.generator = "Ninja Multi-Config"
    elif settings.os == "Macos":
        cmake.generator = "Xcode"
        if settings.os.version:
            cmake.definitions["CMAKE_OSX_DEPLOYMENT_TARGET"] = settings.os.version
    elif settings.os == "Windows":
        cmake.generator = "Visual Studio 17 2022"
    return cmake

def configure_cmake(cmake, build_subfolder, config=None):
    if config:
        cmake.definitions["CMAKE_BUILD_TYPE"] = config
    cmake.configure(build_dir=build_subfolder)

def cmake_build_debug_release(cmake, build_subfolder, run):
    for config in ("Debug", "Release"):
        configure_cmake(cmake, build_subfolder)
        cmake.build(args=["--config", config, "--verbose"])
        with tools.chdir(build_subfolder):
            run(f"ctest -C {config} --output-on-failure")

def cmake_install_debug_release(cmake, build_subfolder):
    configure_cmake(cmake, build_subfolder)
    cmake.install(args=["--config", "Debug"])
    cmake.install(args=["--config", "Release"])
