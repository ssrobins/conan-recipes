from conans import ConanFile, CMake, tools
import os

class Conan(ConanFile):
    name = "sfml"
    version = "2.5.1"
    description = "Simple and fast multimedia library"
    homepage = "https://www.sfml-dev.org/"
    license = "Zlib"
    url = "https://gitlab.com/ssrobins/conan-" + name
    settings = "os", "compiler", "arch"
    generators = "cmake"
    revision_mode = "scm"
    exports = "cmake_utils.py"
    exports_sources = ["AudioDevice.diff", "CMakeLists.txt"]
    zip_folder_name = "SFML-%s" % version
    zip_name = "%s-sources.zip" % zip_folder_name
    build_subfolder = "build"
    source_subfolder = "source"

    def system_requirements(self):
        if self.settings.os == "Linux":
            installer = tools.SystemPackageTool()
            installer.install("libflac-dev")
            installer.install("libgl1-mesa-dev")
            installer.install("libopenal-dev")
            installer.install("libudev-dev")
            installer.install("libvorbis-dev")
            installer.install("libxrandr-dev")

    def build_requirements(self):
        self.build_requires.add("cmake_utils/0.3.1#7b308615a235fdf046db096dd35325c0375c2f88")

    def source(self):
        tools.download("https://www.sfml-dev.org/files/%s" % self.zip_name, self.zip_name)
        tools.unzip(self.zip_name)
        os.unlink(self.zip_name)
        os.rename(self.zip_folder_name, self.source_subfolder)

        # Replace auto_ptr with unique_ptr to fix build errors when using the C++17 standard
        tools.patch(base_path=os.path.join(self.source_subfolder, "src", "SFML", "Audio"), patch_file="AudioDevice.diff")

    def build(self):
        from cmake_utils import cmake_init, cmake_build_debug_release
        cmake = cmake_init(self.settings, CMake(self), self.build_folder)
        cmake_build_debug_release(cmake, self.build_subfolder, self.run)

    def package(self):
        from cmake_utils import cmake_init, cmake_install_debug_release
        cmake = cmake_init(self.settings, CMake(self), self.build_folder)
        cmake_install_debug_release(cmake, self.build_subfolder)
        if self.settings.compiler == "Visual Studio":
            self.copy("*.pdb", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.debug.libs = ["sfml-graphics-s-d", "sfml-window-s-d", "sfml-system-s-d"]
        self.cpp_info.release.libs = ["sfml-graphics-s", "sfml-window-s", "sfml-system-s"]
        if self.settings.os == "Windows":
            system_libs = ["opengl32", "winmm"]
            self.cpp_info.debug.libs.append("sfml-main-d")
            self.cpp_info.release.libs.append("sfml-main")
            self.cpp_info.debug.libs.extend(system_libs)
            self.cpp_info.release.libs.extend(system_libs)
        elif self.settings.os == "Linux":
            system_libs = ["GL", "pthread", "udev", "X11", "Xrandr"]
            self.cpp_info.debug.libs.extend(system_libs)
            self.cpp_info.release.libs.extend(system_libs)
        elif self.settings.os == "Macos":
            frameworks = ["Carbon", "Cocoa", "CoreFoundation", "CoreGraphics", "IOKit", "OpenGL"]
            for framework in frameworks:
                self.cpp_info.exelinkflags.append("-framework %s" % framework)
            self.cpp_info.exelinkflags.append("-ObjC")
        self.cpp_info.defines = ["SFML_STATIC"]
