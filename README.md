This branch is used in this bug report:
https://github.com/conan-io/conan/issues/11528

## A collection of Conan recipes!

Here are all the [Conan Package Manager](https://conan.io/) recipes for the C/C++ libraries I use in my projects. I'm not using the official [ConanCenter](https://github.com/conan-io/conan-center-index) recipes because:
- They don't completely support Android and iOS
- I want maximum flexibility to make immediate changes to the recipes
- I prefer to keep it simple and reduce the scope of the recipes to just what I need (static libs, not all features turned on, etc....)

Over time, I suspect I'll be able to transition over to ConanCenter for third-party libraries and I'll definitely look for opportunities to help with that.

## Quick tour
- [recipes](recipes): Each subdirectory contains a Conan recipe plus supporting CMake and Python scripts
- [profiles](profiles): Conan profiles that precisely articulate the packages I build across Windows, Linux, macOS, Android, and iOS platforms
- [scripts](scripts): Scripts shared across the recipes to easily automate the building/packaging process
- [.github/workflows](.github/workflows): GitHub Actions CI/CD workflows to build, package, and publish the Conan packages

## Projects that use the resulting Conan packages
- https://github.com/ssrobins/stackblox
- https://github.com/ssrobins/sdl2-example
- https://github.com/ssrobins/sfml-examples
