set -e

cd $(dirname "$0")

conan remote add bintray-stever https://api.bintray.com/conan/stever/conan --insert --force

conan create --update . -s os=Android -s os.api_level=16 -s arch=armv7 -s compiler=clang -s compiler.version=11 -s compiler.libcxx=libc++
