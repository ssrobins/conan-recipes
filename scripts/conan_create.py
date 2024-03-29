#!/usr/bin/env python3

import argparse
import os.path
import shutil
import subprocess
import sys


def conan_create(recipe_path, desktop_only=False, own_code=False):
    script_path = os.path.dirname(os.path.realpath(__file__))

    platform = {
        "androidarm": f"--profile:host={script_path}/../profiles/androidarm.jinja",
        "androidarm64": f"--profile:host={script_path}/../profiles/androidarm64.jinja",
        "ios": f"--profile:host={script_path}/../profiles/ios",
        "linux": f"--profile:host={script_path}/../profiles/linux",
        "macos": f"--profile:host={script_path}/../profiles/macos",
        "windows": f"--profile:host={script_path}/../profiles/windows"
    }

    parser = argparse.ArgumentParser()
    parser.add_argument("platform", choices=list(platform.keys()), help="Build platform")
    parser.add_argument("--config", help="Build config")
    parser.add_argument("--iwyu", action="store_true", help="Enable 'Include What You Use' tool")
    command_args = parser.parse_args()

    if desktop_only and ("android" in command_args.platform or "ios" in command_args.platform):
        return

    if own_code and command_args.iwyu:
        iwyu = True
    else:
        iwyu = False

    if iwyu:
        if not shutil.which("include-what-you-use"):
            print("include-what-you-use binary not found", flush=True)
            sys.exit(1)
        conan_subcommand = "install"
        build_dir = f"build_{command_args.platform}_iwyu"
        conan_options = f" -o iwyu=True --output-folder {build_dir}"
    else:
        conan_subcommand = "create"
        conan_options = ""

    if command_args.config:
        config = f"-s build_type={command_args.config}"
    else:
        config = "-s build_type=Debug"

    conan_command = f"conan {conan_subcommand} --update --user ssrobins . {platform[command_args.platform]} {config}{conan_options}"
    print(conan_command, flush=True)
    subprocess.run(conan_command, cwd=recipe_path, shell=True, check=True)

    if iwyu:
        cmake_command = f'cmake -G "Ninja Multi-Config" -DCMAKE_TOOLCHAIN_FILE=build/conan_toolchain.cmake -DCMAKE_CXX_INCLUDE_WHAT_YOU_USE="include-what-you-use" -B {build_dir}'
        print(cmake_command, flush=True)
        subprocess.run(cmake_command, cwd=recipe_path, shell=True, check=True)

        cmake_build_command = f"cmake --build {build_dir} --clean-first"
        print(cmake_build_command, flush=True)
        subprocess.run(cmake_build_command, cwd=recipe_path, shell=True, check=True)


def conan_create_single_platform(recipe_path):
    script_path = os.path.dirname(os.path.realpath(__file__))
    conan_create = f"conan create --update --user ssrobins ."
    print(conan_create, flush=True)
    subprocess.run(conan_create, cwd=recipe_path, shell=True, check=True)
