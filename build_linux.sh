set -e

cd $(dirname "$0")

conan create --update . -s compiler.libcxx=libstdc++11
