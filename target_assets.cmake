function(target_assets target_name assets_path)
    get_filename_component(assets_dir ${assets_path} NAME)

    set(is_mac_bundle 0)
    if(APPLE)
        get_target_property(is_mac_bundle ${target_name} MACOSX_BUNDLE)
        if(${is_mac_bundle})
            if(IOS)
                set(assets_dest_dir ${assets_dir})
                add_custom_command(
                    TARGET ${target_name}
                    PRE_BUILD
                    COMMAND python3 ${CONAN_CMAKE_UTILS_ROOT}/add_xcode_folder_reference.py
                        --project=${CMAKE_BINARY_DIR}/${PROJECT_NAME}.xcodeproj/project.pbxproj
                        --folderPath=${assets_path} --target=${target_name}
                )
            else()
                set(assets_dest_dir ../Resources/${assets_dir})
            endif()
        else()
            set(assets_dest_dir ${assets_dir})
        endif()
    elseif(ANDROID)
        set(assets_dest_dir Android/app/src/main/assets/${assets_dir})
    else()
        set(assets_dest_dir ${assets_dir})
    endif()

    add_custom_command(
        TARGET ${target_name}
        PRE_BUILD
        COMMAND cmake -E copy_directory
            ${assets_path}
            $<TARGET_FILE_DIR:${target_name}>/${assets_dest_dir}
    )

    set(component_name ${target_name}_${PROJECT_VERSION}_${platform})
    if(NOT IOS AND NOT ${is_mac_bundle} AND NOT ANDROID)
        install(DIRECTORY ${assets_path} DESTINATION ${target_name} COMPONENT ${component_name})
    endif()

    # Stage assets so Visual Studio will find them.
    # Not needed if an absolute path is used.
    if(MSVC)
        add_custom_command(
            TARGET ${target_name}
            POST_BUILD
            COMMAND cmake -E copy_directory
                ${assets_path}
                ${CMAKE_CURRENT_BINARY_DIR}/assets
        )
    endif()
endfunction(target_assets)
