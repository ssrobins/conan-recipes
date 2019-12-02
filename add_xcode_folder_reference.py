import argparse
import os
import uuid


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", help="Path to the Xcode project", required=True)
    parser.add_argument("--folderPath", help="Path to the folder reference", required=True)
    parser.add_argument("--target", help="Build target name", required=True)
    command_args = parser.parse_args()
    
    with open(command_args.project) as f:
        project_data = f.read()
        
    folder_path = command_args.folderPath
    folder = os.path.basename(folder_path)
    
    id1 = str(uuid.uuid4().hex)
    id2 = str(uuid.uuid4().hex)
    
    pbxbuildfile_header = '/* Begin PBXBuildFile section */'
    project_data = project_data.replace(
        pbxbuildfile_header,
        '{0}\n\t\t{1} /* {2} in Resources */ = {{isa = PBXBuildFile; fileRef = {3} /* {2} */; }};'.format(pbxbuildfile_header, id1, folder, id2),
    )

    if folder.endswith(".xcassets"):
        last_known_file_type = "folder.assetcatalog"
    else:
        last_known_file_type = "folder"
    
    pbxfilereference_header = '/* Begin PBXFileReference section */'
    project_data = project_data.replace(
        pbxfilereference_header,
        '{0}\n\t\t{1} /* {2} */ = {{isa = PBXFileReference; lastKnownFileType = {3}; name = {2}; path = {4}; sourceTree = "<group>"; }};'.format(pbxfilereference_header, id2, folder, last_known_file_type, folder_path)
    )
    
    # Get <RESOURCES_PBXGROUP_ID> for 'Resources' in <TARGET>:
    # <PBXGROUP_ID> /* <TARGET> */ = {
    #        isa = PBXGroup;
    #        children = (
    #            <RESOURCES_PBXGROUP_ID> /* Resources */,
    index_pbx_group = project_data.find('/* {0} */ = {{\n\t\t\tisa = PBXGroup;'.format(command_args.target))
    index_resources_child = project_data.find('/* Resources */', index_pbx_group)
    index_start_resources_pbxgroup = project_data.rfind('\t', 0, index_resources_child)
    resources_pbxgroup_id = project_data[index_start_resources_pbxgroup:index_resources_child].strip()
    
    pbxgroup_section = '{0} /* Resources */ = {{\n\t\t\tisa = PBXGroup;\n\t\t\tchildren = ('.format(resources_pbxgroup_id)
    project_data = project_data.replace(
        pbxgroup_section,
        '{0}\n\t\t\t\t{1} /* {2} */,'.format(pbxgroup_section, id2, folder)
    )

    pbxbuildphase_section = 'isa = PBXResourcesBuildPhase;\n\t\t\tbuildActionMask = 2147483647;\n\t\t\tfiles = ('
    project_data = project_data.replace(
        pbxbuildphase_section,
        '{0}\n\t\t\t\t{1} /* {2} in Resources */,'.format(pbxbuildphase_section, id1, folder)
    )
        
    with open(command_args.project, "w") as f:
        f.write(project_data)      


if __name__ == "__main__":
    main()
