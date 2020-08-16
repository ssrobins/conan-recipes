function(install_executable target_name)
    set(component_name ${target_name}_${PROJECT_VERSION}_${platform})

    set(androidstudio_path ${CMAKE_BINARY_DIR}/AndroidStudio/${target_name})

    if(ANDROID)
        install(DIRECTORY ${androidstudio_path}/ DESTINATION . COMPONENT ${component_name} USE_SOURCE_PERMISSIONS)
    elseif(IOS)
        configure_file(${CONAN_CMAKE_UTILS_ROOT}/export_options.plist export_options.plist)
        install(FILES ${CMAKE_CURRENT_BINARY_DIR}/export_options.plist DESTINATION . COMPONENT ${component_name})
        configure_file(${CONAN_CMAKE_UTILS_ROOT}/install_ios.cmake install_ios.cmake @ONLY)
        install(SCRIPT ${CMAKE_CURRENT_BINARY_DIR}/install_ios.cmake COMPONENT ${component_name})
    else()
        install(TARGETS ${target_name} DESTINATION ${target_name} COMPONENT ${component_name})
    endif()

    # Stage Mac bundle icon
    if(APPLE AND NOT IOS)
        if(EXISTS ${CMAKE_CURRENT_SOURCE_DIR}/icon.icns)
            get_target_property(is_mac_bundle ${target_name} MACOSX_BUNDLE)
            if(${is_mac_bundle})
                add_custom_command(
                    TARGET ${target_name}
                    POST_BUILD
                    COMMAND cmake -E copy
                        ${CMAKE_CURRENT_SOURCE_DIR}/icon.icns
                        $<TARGET_FILE_DIR:${target_name}>/../Resources/icon.icns
                )
            endif()
        endif()
    endif()
endfunction(install_executable)
