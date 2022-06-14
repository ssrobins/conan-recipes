cmake_minimum_required(VERSION 3.1.2)
project(test_package CXX)

set(CMAKE_CXX_STANDARD 17)

find_package(gtest REQUIRED)

add_executable(${PROJECT_NAME} main.cpp)

target_link_libraries(${PROJECT_NAME}
    gtest::gtest
)

if(NOT ANDROID AND NOT IOS)
    enable_testing()
    add_test(NAME ${PROJECT_NAME} COMMAND ${PROJECT_NAME})
endif()
