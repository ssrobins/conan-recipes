cmake_minimum_required(VERSION 3.1.2)
project(test_package CXX)

find_package(sdl_mixer REQUIRED)

if(ANDROID)
    add_library(${PROJECT_NAME} SHARED)
else()
    add_executable(${PROJECT_NAME})
endif()

target_sources(${PROJECT_NAME} PRIVATE
    main.cpp
)

target_link_libraries(${PROJECT_NAME}
    sdl_mixer::sdl_mixer
)
