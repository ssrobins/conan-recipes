@echo off
setlocal

cd /d %~dp0

conan remote add artifactory-ssrobins https://ssrobins.jfrog.io/artifactory/api/conan/conan --insert --force

conan create --update . -s arch=x86 -s compiler.version=16 -s compiler.runtime=MT
