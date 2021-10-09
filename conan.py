#!/usr/bin/env python3

import argparse
import os.path
import subprocess

def main():
    os.environ["CONAN_REVISIONS_ENABLED"] = "1"

    platform = {
        "androidarm": "-s os=Android -s os.api_level=16 -s arch=armv7 -s compiler=clang -s compiler.version=12 -s compiler.libcxx=c++_static",
        "androidarm64": "-s os=Android -s os.api_level=21 -s arch=armv8 -s compiler=clang -s compiler.version=12 -s compiler.libcxx=c++_static",
        "ios": "-s os=iOS -s arch=armv7 -s os.version=9.0 -s compiler.version=13.0",
        "linux": "-s compiler=gcc -s compiler.version=7 -s compiler.libcxx=libstdc++11",
        "macos": "-s os.version=10.9 -s compiler.version=13.0",
        "windows": "-s arch=x86 -s compiler.version=16 -s compiler.runtime=MT"
    }

    parser = argparse.ArgumentParser()
    parser.add_argument("platform", choices=list(platform.keys()), help="Build platform")
    command_args = parser.parse_args()

    script_path = os.path.dirname(os.path.realpath(__file__))

    remote_url = "https://ssrobins.jfrog.io/artifactory/api/conan/conan"
    conan_remote = f"conan remote add artifactory-ssrobins {remote_url} --insert --force"
    print(conan_remote, flush=True)
    subprocess.run(conan_remote, cwd=script_path, shell=True, check=True)

    conan_create = f"conan create --update . {platform[command_args.platform]}"
    print(conan_create, flush=True)
    subprocess.run(conan_create, cwd=script_path, shell=True, check=True)


if __name__ == "__main__":
    main()
