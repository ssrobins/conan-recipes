set -e

cd $(dirname "$0")

. ./config.txt
export $(cut -d= -f1 config.txt)
export package_channel=$(git rev-parse --abbrev-ref HEAD)

conan create . ${package_user}/${package_channel} -s os=iOS -s arch=armv7 -s os.version=8.0

if [ "$CI" == "true" ]; then
    conan upload ${package_name}/${package_version}@${package_user}/${package_channel} -r ${package_repo} --all
fi
