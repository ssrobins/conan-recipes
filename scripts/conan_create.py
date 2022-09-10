#!/usr/bin/env python3

import argparse
import os.path
import shutil
import subprocess
import sys


def conan_create(recipe_path, desktop_only=False, own_code=False):
    os.environ["CONAN_REVISIONS_ENABLED"] = "1"

    script_path = os.path.dirname(os.path.realpath(__file__))

    platform = {
        "androidarm": f"-pr:h={script_path}/../profiles/androidarm.jinja",
        "androidarm64": f"-pr:h={script_path}/../profiles/androidarm64.jinja",
        "ios": f"-pr:h={script_path}/../profiles/ios",
        "linux": f"-pr:h={script_path}/../profiles/linux",
        "macos": f"-pr:h={script_path}/../profiles/macos",
        "windows": f"-pr:h={script_path}/../profiles/windows_x86 -pr:b={script_path}/../profiles/windows_x64"
    }

    parser = argparse.ArgumentParser()
    parser.add_argument("platform", choices=list(platform.keys()), help="Build platform")
    parser.add_argument("--config", help="Build config")
    parser.add_argument("--iwyu", action="store_true", help="Enable Include what you use")
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
    else:
        conan_subcommand = "create"

    if command_args.config:
        config = f"-s build_type={command_args.config}"
    else:
        config = "-s build_type=Debug"

    conan_command = f"conan {conan_subcommand} --update --user ssrobins . {platform[command_args.platform]} -pr:b={script_path}/../profiles/default {config}"
    print(conan_command, flush=True)
    subprocess.run(conan_command, cwd=recipe_path, shell=True, check=True)

    if iwyu:
        cmake_command = 'cmake -G "Ninja Multi-Config" -DCMAKE_TOOLCHAIN_FILE=build/conan_toolchain.cmake -DCMAKE_CXX_INCLUDE_WHAT_YOU_USE="include-what-you-use" -B build'
        print(cmake_command, flush=True)
        subprocess.run(cmake_command, cwd=recipe_path, shell=True, check=True)

        cmake_build_command = f"cmake --build build --clean-first"
        print(cmake_build_command, flush=True)
        subprocess.run(cmake_build_command, cwd=recipe_path, shell=True, check=True)


def conan_create_single_platform(recipe_path):
    script_path = os.path.dirname(os.path.realpath(__file__))
    conan_create = f"conan create --update --user ssrobins . -pr:b={script_path}/../profiles/default -pr:h={script_path}/../profiles/default"
    print(conan_create, flush=True)
    subprocess.run(conan_create, cwd=recipe_path, shell=True, check=True)
