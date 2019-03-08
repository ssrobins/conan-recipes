set -e

cd $(dirname "$0")

CONAN_USERNAME=$(cat conan_user.txt)

if [ -z "$CI_COMMIT_REF_NAME" ]; then
    CI_COMMIT_REF_NAME=$(git rev-parse --abbrev-ref HEAD)
fi

conan create . $CONAN_USERNAME/$CI_COMMIT_REF_NAME -s os=iOS -s arch=armv7 -s os.version=8.0