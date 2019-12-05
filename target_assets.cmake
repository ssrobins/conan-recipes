function(target_assets target_name assets_path)
    set(assets_path_list ${ARGV})
    list(REMOVE_AT assets_path_list 0)

    foreach(assets_path ${assets_path_list})
        get_filename_component(assets_dir "${assets_path}" NAME)

        get_filename_component(assets_path "${assets_path}"
            REALPATH BASE_DIR "${CMAKE_CURRENT_SOURCE_DIR}")

        if(IOS)
            set(assets_dest_dir ${assets_dir})
            add_custom_command(
                TARGET ${target_name}
                PRE_BUILD
                COMMAND python3 ${CONAN_CMAKE_UTILS_ROOT}/add_xcode_folder_reference.py
                    --project=${CMAKE_BINARY_DIR}/${PROJECT_NAME}.xcodeproj/project.pbxproj
                    --folderPath=${assets_path} --target=${target_name}
            )
        elseif(APPLE)
            set(assets_dest_dir $<IF:$<BOOL:$<TARGET_PROPERTY:${target_name},MACOSX_BUNDLE>>,../Resources/${assets_dir},${assets_dir}>)
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

        if(NOT IOS AND NOT ANDROID)
            if(APPLE)
                set(assets_install_dir $<IF:$<BOOL:$<TARGET_PROPERTY:${target_name},MACOSX_BUNDLE>>,${target_name}.app/Contents/Resources,>)
            endif()
            set(component_name ${target_name}_${PROJECT_VERSION}_${platform})
            install(DIRECTORY ${assets_path} DESTINATION ${target_name}/${assets_install_dir} COMPONENT ${component_name})
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
    endforeach()
endfunction(target_assets)
