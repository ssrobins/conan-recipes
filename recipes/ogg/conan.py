#!/usr/bin/env python3

import argparse
import os.path
import subprocess

def main():
    os.environ["CONAN_REVISIONS_ENABLED"] = "1"

    platform = {
        "androidarm": "-pr:h=profiles/androidarm.jinja",
        "androidarm64": "-pr:h=profiles/androidarm64.jinja",
        "ios": "-pr:h=profiles/ios",
        "linux": "-pr:h=profiles/linux",
        "macos": "-pr:h=profiles/macos",
        "windows": "-pr:h=profiles/windows"
    }

    parser = argparse.ArgumentParser()
    parser.add_argument("platform", choices=list(platform.keys()), help="Build platform")
    parser.add_argument("--config", help="Build config")
    command_args = parser.parse_args()

    script_path = os.path.dirname(os.path.realpath(__file__))

    if command_args.config:
        config = f"-s build_type={command_args.config}"
    else:
        config = "-s build_type=Debug"

    remote_url = "https://ssrobins.jfrog.io/artifactory/api/conan/conan"
    conan_remote = f"conan remote add artifactory-ssrobins {remote_url} --insert --force"
    print(conan_remote, flush=True)
    subprocess.run(conan_remote, cwd=script_path, shell=True, check=True)

    conan_create = f"conan create --update . {platform[command_args.platform]} {config}"
    print(conan_create, flush=True)
    subprocess.run(conan_create, cwd=script_path, shell=True, check=True)


if __name__ == "__main__":
    main()
