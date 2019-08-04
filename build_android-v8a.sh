set -e

cd $(dirname "$0")

conan create . -s os=Android -s os.api_level=21 -s arch=armv8 -s compiler=clang -s compiler.version=8 -s compiler.libcxx=libc++
