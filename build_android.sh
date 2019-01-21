set -e

cd $(dirname "$0")

. ./config.txt
export $(cut -d= -f1 config.txt)
export package_channel=$(git rev-parse --abbrev-ref HEAD)

conan create . ${package_user}/${package_channel} -s os=Android -s os.api_level=${android_sdk_version} -s arch=armv7 -s compiler=clang -s compiler.version=7.0 -s compiler.libcxx=libstdc++11

if [ "$CI" == "true" ]; then
    conan upload ${package_name}/${package_version}@${package_user}/${package_channel} -r ${package_repo} --all
fi
