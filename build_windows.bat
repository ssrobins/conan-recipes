@echo off
setlocal

cd /d %~dp0

conan create --update . -s arch=x86 -s compiler.version=16 -s compiler.runtime=MT
