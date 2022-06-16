cmake_minimum_required(VERSION 3.1.2)
project(test_package CXX)

find_package(sdl REQUIRED)

add_executable(${PROJECT_NAME} main.cpp)

target_link_libraries(${PROJECT_NAME}
    sdl::sdl
)
