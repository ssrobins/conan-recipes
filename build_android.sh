set -e

cd $(dirname "$0")

if [ -z "$CONAN_USERNAME" ]; then
    echo "Set CONAN_USERNAME environment variable and re-run"
    exit 1
fi

if [ -z "$CI_COMMIT_REF_NAME" ]; then
    package_channel=$(git rev-parse --abbrev-ref HEAD)
fi

conan create . $CONAN_USERNAME/$CI_COMMIT_REF_NAME -s os=Android -s os.api_level=$android_sdk_version -s arch=armv7 -s compiler=clang -s compiler.version=8 -s compiler.libcxx=libc++