from conans import ConanFile, tools
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain

class Conan(ConanFile):
    name = "libpng"
    version = "1.6.37"
    description = "Official PNG image format reference library"
    homepage = "http://www.libpng.org"
    license = "Libpng http://www.libpng.org/pub/png/src/libpng-LICENSE.txt"
    url = f"https://github.com/ssrobins/conan-{name}"
    settings = "os", "arch", "compiler", "build_type"
    generators = "CMakeDeps"
    revision_mode = "scm"
    exports_sources = ["CMakeLists.diff", "CMakeLists.txt"]
    zip_folder_name = f"libpng-{version}"
    zip_name = f"{zip_folder_name}.tar.gz"
    maj_min_ver = str().join(version.split(".")[0:2])

    def build_requirements(self):
        self.build_requires("cmake_utils/9.0.1#7f745054c87ea0007a89813a4d2c30c4c95e24b2")

    def requirements(self):
        self.requires("zlib/1.2.12#c29f7752505a24f4203f4edddec7d81a89e9bc7f")

    @property
    def _source_subfolder(self):
        return "source"

    def layout(self):
        self.folders.build = "build"
        self.folders.generators = self.folders.build

    def source(self):
        tools.get(f"https://sourceforge.net/projects/libpng/files/libpng16/{self.version}/{self.zip_name}",
            sha256="daeb2620d829575513e35fecc83f0d3791a620b9b93d800b763542ece9390fb4",
            destination=self._source_subfolder,
            strip_root=True)

        # Apply a patch to the libpng CMakeLists.txt file with the following changes:
        # https://sourceforge.net/p/libpng/code/merge-requests/4/
        # https://github.com/glennrp/libpng/pull/318
        # https://github.com/glennrp/libpng/pull/359
        tools.patch(base_path=self._source_subfolder, patch_file="CMakeLists.diff")

    def generate(self):
        tc = CMakeToolchain(self)
        tc.generator = "Ninja Multi-Config"
        tc.variables["CMAKE_VERBOSE_MAKEFILE"] = "TRUE"
        if self.settings.os == "iOS":
            tc.variables["CMAKE_SYSTEM_NAME"] = "iOS"
            if self.settings.arch != "x86_64":
                tc.blocks["apple_system"].values["cmake_osx_architectures"] = "armv7;arm64"
        tc.generate()
        deps = CMakeDeps(self)
        deps.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
        self.run(f"ctest -C {self.settings.build_type} --output-on-failure")
        cmake.install()

    def package(self):
        if self.settings.compiler == "msvc":
            self.copy("*.pdb", dst="lib", keep_path=False)

    def package_info(self):
        if self.settings.os == "Windows":
            if self.settings.build_type == "Debug":
                self.cpp_info.libs = [f"libpng{self.maj_min_ver}_staticd"]
            else:
                self.cpp_info.libs = [f"libpng{self.maj_min_ver}_static"]
        else:
            if self.settings.build_type == "Debug":
                self.cpp_info.libs = [f"png{self.maj_min_ver}d"]
            else:
                self.cpp_info.libs = [f"png{self.maj_min_ver}"]
