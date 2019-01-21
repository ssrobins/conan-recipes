set -e

cd $(dirname "$0")

. ./config.txt
export $(cut -d= -f1 config.txt)

conan create . ${package_user}/${package_channel} -s compiler.libcxx=libstdc++11
conan upload ${package_name}/${package_version}@${package_user}/${package_channel} -r ${package_repo} --all
