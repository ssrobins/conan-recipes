@echo off
setlocal

cd /d %~dp0

for /f "delims=" %%x in (config.txt) do (set "%%x")

if defined CI_COMMIT_REF_NAME (
    set package_channel=%CI_COMMIT_REF_NAME%
) else (
    set package_channel=testing
)

conan create . %package_user%/%package_channel% -s arch=x86 -s compiler.runtime=MT || goto :error

if "%CI%" == "true" (
    conan upload %package_name%/%package_version%@%package_user%/%package_channel% -r %package_repo% --all || goto :error
)

:error
exit /b %errorlevel%