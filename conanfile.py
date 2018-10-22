from conans import ConanFile, CMake, tools
from conans.util import files
import os


class ZlibConan(ConanFile):
    name = "zlib"
    version = os.getenv("package_version")
    license = "Zlib"
    url = "https://gitlab.com/ssrobins/conan-zlib"
    description = "A Massively Spiffy Yet Delicately Unobtrusive Compression Library " \
                  "(Also Free, Not to Mention Unencumbered by Patents)"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"
    zip_folder_name = "zlib-%s" % version

    def source(self):
        z_name = "zlib-%s.tar.gz" % self.version
        tools.download("https://zlib.net/zlib-%s.tar.gz" % self.version, z_name)
        tools.unzip(z_name)
        os.unlink(z_name)
        files.rmdir("%s/contrib" % self.zip_folder_name)

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder=self.zip_folder_name)
        cmake.build()

    def package(self):
        self.copy("*.h", dst="include", src=self.zip_folder_name)
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        if self.settings.os == "Windows" and not tools.os_info.is_linux:
            self.cpp_info.libs = ['zlib']
        else:
            self.cpp_info.libs = ['z']
