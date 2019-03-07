@echo off
setlocal

cd /d %~dp0

if not defined CONAN_USERNAME (
    echo Set CONAN_USERNAME environment variable and re-run
    goto :error
)

if not defined CI_COMMIT_REF_NAME (
    for /f "usebackq tokens=*" %%b in (`git rev-parse --abbrev-ref HEAD`) do (set CI_COMMIT_REF_NAME=%%b)
)

conan create . %CONAN_USERNAME%/%CI_COMMIT_REF_NAME% -s arch=x86 -s compiler.runtime=MT || goto :error

echo error level %errorlevel%

:error
exit /b %errorlevel%