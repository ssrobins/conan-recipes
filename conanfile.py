from conans import ConanFile, CMake, tools
import os

class Conan(ConanFile):
    name = "glew"
    version = "2.1.0"
    description = "OpenGL extension wrangler library"
    homepage = "https://github.com/nigels-com/glew"
    license = "https://github.com/nigels-com/glew/blob/master/LICENSE.txt"
    url = f"https://github.com/ssrobins/conan-{name}"
    settings = "os", "arch", "compiler", "build_type"
    generators = "cmake"
    _cmake = None
    revision_mode = "scm"
    exports_sources = ["CMakeLists.diff", "CMakeLists.txt"]
    zip_folder_name = f"{name}-{version}"
    zip_name = f"{zip_folder_name}.tgz"
    build_subfolder = "build"
    source_subfolder = "source"

    def system_requirements(self):
        if self.settings.os == "Linux":
            installer = tools.SystemPackageTool()
            installer.install("freeglut3-dev")

    def build_requirements(self):
        self.build_requires("cmake_utils/7.0.0#9bf47716aeee70a8dcfc8592831a0318eb327a09")

    def source(self):
        tools.get(f"https://github.com/nigels-com/glew/releases/download/{self.zip_folder_name}/{self.zip_name}")
        os.rename(self.zip_folder_name, self.source_subfolder)

        # Apply a patch to fix error LNK2001: unresolved external symbol _memset
        # when building the shared library on MSVC
        # https://github.com/nigels-com/glew/issues/180:
        tools.patch(base_path=self.source_subfolder, patch_file="CMakeLists.diff")

    def _configure_cmake(self):
        if self._cmake:
            return self._cmake
        self._cmake = CMake(self)
        if self.settings.os != "Windows":
            self._cmake.generator = "Ninja Multi-Config"
        if self.settings.os == "Android":
            self._cmake.definitions["CMAKE_TOOLCHAIN_FILE"] = os.getenv("ANDROID_NDK_ROOT") + "/build/cmake/android.toolchain.cmake"
        elif self.settings.os == "iOS" and self.settings.arch != "x86_64":
            self._cmake.definitions["CMAKE_OSX_ARCHITECTURES"] = "armv7;arm64"
        elif self.settings.os == "Windows" and self.settings.arch == "x86":
            self._cmake.generator_platform = "Win32"
        self._cmake.configure(build_dir=self.build_subfolder)
        return self._cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build(args=["--verbose"])
        with tools.chdir(self.build_subfolder):
            self.run(f"ctest -C {self.settings.build_type} --output-on-failure")
        cmake.install()

    def package(self):
        if self.settings.compiler == "msvc":
            self.copy("*.pdb", dst="lib", keep_path=False)

    def package_info(self):
        if self.settings.os == "Windows":
            if self.settings.build_type == "Debug":
                self.cpp_info.libs = ["libglew32d"]
            else:
                self.cpp_info.libs = ["libglew32"]
            self.cpp_info.system_libs.append("OpenGL32")
            self.cpp_info.defines.append("GLEW_STATIC")
        elif self.settings.os == "Macos":
            if self.settings.build_type == "Debug":
                self.cpp_info.libs = ["GLEWd"]
            else:
                self.cpp_info.libs = ["GLEW"]
            self.cpp_info.frameworks.append("OpenGL")
        else:
            if self.settings.build_type == "Debug":
                self.cpp_info.libs = ["GLEWd"]
            else:
                self.cpp_info.libs = ["GLEW"]
            self.cpp_info.system_libs.append("GL")
