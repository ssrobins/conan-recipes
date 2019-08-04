set -e

cd $(dirname "$0")

conan create --update . -s os=Android -s os.api_level=16 -s arch=armv7 -s compiler=clang -s compiler.version=8 -s compiler.libcxx=libc++
