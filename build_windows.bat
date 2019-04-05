@echo off
setlocal

cd /d %~dp0

set /p CONAN_USERNAME=<conan_user.txt

if not defined CI_COMMIT_REF_NAME (
    for /f "usebackq tokens=*" %%b in (`git rev-parse --abbrev-ref HEAD`) do (set CI_COMMIT_REF_NAME=%%b)
)

conan create . %CONAN_USERNAME%/%CI_COMMIT_REF_NAME% -s arch=x86 -s compiler.version=16 -s compiler.runtime=MT

:error
exit /b %errorlevel%