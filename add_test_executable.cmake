function(add_test_executable target_name)
    add_executable_custom(${target_name})

    target_link_libraries(${target_name} 
        CONAN_PKG::gtest
    )

    if(NOT ANDROID AND NOT IOS)
        add_test(NAME ${target_name} COMMAND ${target_name})

        # Run unit tests after the build
        add_custom_command(
            TARGET ${target_name}
            POST_BUILD
            COMMAND ctest -C $<CONFIGURATION> --output-on-failure
        )
    endif()
endfunction(add_test_executable)