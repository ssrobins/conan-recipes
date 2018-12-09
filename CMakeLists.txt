set(target_name DisplayTest)

include(${CMAKE_SOURCE_DIR}/add_executable.cmake)

target_sources(${target_name} PRIVATE
    DisplayTest.cpp
)

target_include_directories(${target_name} PRIVATE
)

target_link_libraries(${target_name}
    Display
)

include(${CMAKE_SOURCE_DIR}/testing.cmake)
