#!/usr/bin/env python3

import argparse
import os.path
import subprocess


def conan_create(recipe_path):
    os.environ["CONAN_REVISIONS_ENABLED"] = "1"

    script_path = os.path.dirname(os.path.realpath(__file__))

    platform = {
        "androidarm": f"-pr:h={script_path}/../profiles/androidarm.jinja",
        "androidarm64": f"-pr:h={script_path}/../profiles/androidarm64.jinja",
        "ios": f"-pr:h={script_path}/../profiles/ios",
        "linux": f"-pr:h={script_path}/../profiles/linux",
        "macos": f"-pr:h={script_path}/../profiles/macos",
        "windows": f"-pr:h={script_path}/../profiles/windows"
    }

    parser = argparse.ArgumentParser()
    parser.add_argument("platform", choices=list(platform.keys()), help="Build platform")
    parser.add_argument("--config", help="Build config")
    command_args = parser.parse_args()

    if command_args.config:
        config = f"-s build_type={command_args.config}"
    else:
        config = "-s build_type=Debug"

    conan_create = f"conan create --update . {platform[command_args.platform]} {config}"
    print(conan_create, flush=True)
    subprocess.run(conan_create, cwd=recipe_path, shell=True, check=True)


def conan_create_single_platform(recipe_path):
    conan_create = "conan create --update ."
    print(conan_create, flush=True)
    subprocess.run(conan_create, cwd=recipe_path, shell=True, check=True)
