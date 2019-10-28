@echo off
setlocal

cd /d %~dp0

conan remote add bintray-stever https://api.bintray.com/conan/stever/conan --insert --force

conan create --update .
