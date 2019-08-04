set -e

cd $(dirname "$0")

conan create --update . -s os=iOS -s arch=armv7 -s os.version=8.0
