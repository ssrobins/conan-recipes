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
        tools.download("https://www.libsdl.org/release/%s" % self.zip_name, self.zip_name)
        tools.unzip(self.zip_name)
        os.unlink(self.zip_name)
        tools.patch(base_path=self.zip_folder_name, patch_file="CMakeLists.diff")

    def configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["SDL_SHARED"] = "OFF"
        cmake.configure(source_folder=self.zip_folder_name)
        return cmake

    def build(self):
        cmake = self.configure_cmake()
        cmake.build()

    def package(self):
        cmake = self.configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.includedirs = [os.path.join('include', 'SDL2')]
        self.cpp_info.libs = ["SDL2", "SDL2main"]
        if self.settings.os == "Windows":
            self.cpp_info.libs.extend(["imm32", "version", "winmm"])
