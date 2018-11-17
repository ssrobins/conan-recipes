set -e

cd $(dirname "$0")

. config.txt
export $(cut -d= -f1 config.txt)

conan create . ${package_user}/${package_channel} -s os=iOS -s os.version=8.0
conan upload ${package_name}/${package_version}@${package_user}/${package_channel} -r ${package_repo} --all
