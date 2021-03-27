set -e

cd $(dirname "$0")

conan remote add artifactory-ssrobins https://ssrobins.jfrog.io/artifactory/api/conan/conan --insert --force

conan create --update . -s os=iOS -s arch=armv7 -s os.version=9.0 -s compiler.version=12.0
