set -e
  
cd $(dirname "$0")

conan create --update .
