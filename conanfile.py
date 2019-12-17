from conans import ConanFile, CMake, tools
import os

class Conan(ConanFile):
    name = "box2d"
    version = "2.3.1"
    description = "A 2D physics engine for games"
    homepage = "https://box2d.org/"
    license = "Zlib"
    url = "https://gitlab.com/ssrobins/conan-" + name
    settings = "os", "compiler", "arch"
    generators = "cmake"
    revision_mode = "scm"
    exports_sources = ["CMakeLists.txt"]
    zip_folder_name = "Box2D-%s" % version
    zip_name = "v%s.tar.gz" % version
    build_subfolder = "build"
    source_subfolder = "source"

    def build_requirements(self):
        self.build_requires.add("cmake_utils/0.3.0#0ec3922f6b2df47dc695bacdbc5491fb972f0a75")
    
    def source(self):
        tools.download("https://github.com/erincatto/Box2D/archive/%s" % self.zip_name, self.zip_name)
        tools.unzip(self.zip_name)
        os.unlink(self.zip_name)
        os.rename(self.zip_folder_name, self.source_subfolder)

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
        self.cpp_info.debug.libs = ["Box2Dd"]
        self.cpp_info.release.libs = ["Box2D"]
