cmake_minimum_required(VERSION 3.17)

set(ANDROID_USE_LEGACY_TOOLCHAIN_FILE false)

project(Project)

option(INSTALL_GMOCK OFF)
option(INSTALL_GTEST OFF)

add_subdirectory(source)

set_target_properties(gmock_main gmock gtest_main gtest PROPERTIES DEBUG_POSTFIX d)
