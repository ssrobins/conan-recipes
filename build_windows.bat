@echo off
setlocal

cd /d %~dp0

for /f "delims=" %%x in (config.txt) do (set "%%x")
for /f "usebackq tokens=*" %%b in (`git rev-parse --abbrev-ref HEAD`) do (set package_channel=%%b)

conan create . %package_user%/%package_channel% -s arch=x86 -s compiler.runtime=MT || goto :error

if "%conan_upload%" == "true" (
    conan upload %package_name%/%package_version%@%package_user%/%package_channel% -r %package_repo% --all || goto :error
)

:error
exit /b %errorlevel%