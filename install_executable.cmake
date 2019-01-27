function(install_executable target_name)
    set(component_name ${target_name}_${version_major}.${version_minor}.${version_patch}_${platform})

    install(TARGETS ${target_name} DESTINATION ${target_name} COMPONENT ${component_name})

    # Stage assets so they are available at runtime in the build directory and install directory
    if(EXISTS ${CMAKE_CURRENT_SOURCE_DIR}/assets)
        get_target_property(is_mac_bundle ${target_name} MACOSX_BUNDLE)
        if(APPLE)
            if(${is_mac_bundle})
                if(IOS)
                    set(assets_dest_dir assets)
                else()
                    set(assets_dest_dir ../Resources/assets)
                endif()
            else()
                set(assets_dest_dir assets)
            endif()
        elseif(ANDROID)
            set(assets_dest_dir Android/app/src/main/assets/assets)
        else()
            set(assets_dest_dir assets)
        endif()

        add_custom_command(
            TARGET ${target_name}
            POST_BUILD
            COMMAND cmake -E copy_directory
                ${CMAKE_CURRENT_SOURCE_DIR}/assets
                $<TARGET_FILE_DIR:${target_name}>/${assets_dest_dir}
        )

        if(NOT IOS AND NOT ${is_mac_bundle} AND NOT ANDROID)
            install(DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/assets DESTINATION ${target_name} COMPONENT ${component_name})
        endif()

        # Stage assets so Visual Studio will find them.
        # Not needed if an absolute path is used.
        if(MSVC)
            add_custom_command(
                TARGET ${target_name}
                POST_BUILD
                COMMAND cmake -E copy_directory
                    ${CMAKE_CURRENT_SOURCE_DIR}/assets
                    ${CMAKE_CURRENT_BINARY_DIR}/assets
            )
        endif()
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