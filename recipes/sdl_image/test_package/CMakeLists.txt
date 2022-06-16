cmake_minimum_required(VERSION 3.1.2)
project(test_package CXX)

find_package(sdl_image REQUIRED)

add_executable(${PROJECT_NAME} main.cpp)

target_link_libraries(${PROJECT_NAME}
    sdl_image::sdl_image
)
