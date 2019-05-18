set -e
  
cd $(dirname "$0")

CONAN_USER=$(cat conan_user.txt)

if [ -z "$CI_COMMIT_REF_NAME" ]; then
    CI_COMMIT_REF_NAME=$(git rev-parse --abbrev-ref HEAD)
fi

conan create . $CONAN_USER/$CI_COMMIT_REF_NAME