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
    zip_folder_name = "SDL2-%s" % version
    zip_name = "%s.tar.gz" % zip_folder_name

    def source(self):
        tools.download("https://www.libsdl.org/release/%s" % self.zip_name, self.zip_name)
        tools.unzip(self.zip_name)
        os.unlink(self.zip_name)

    def build(self):
        cmake = CMake(self)
        cmake.definitions["SDL_SHARED"] = "OFF"
        cmake.configure(source_folder=self.zip_folder_name)
        cmake.build()

    def package(self):
    #    self.copy("*.h", dst="include", src=self.zip_folder_name)
    #    self.copy("*.h", dst="include", src=self.build_folder, keep_path=False)
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    #def package_info(self):
    #    if self.settings.os == "Windows" and not tools.os_info.is_linux:
    #        self.cpp_info.libs = ['zlib']
    #    else:
    #        self.cpp_info.libs = ['z']
