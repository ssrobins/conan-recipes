set -e

cd $(dirname "$0")

conan create . -s compiler.libcxx=libstdc++11
