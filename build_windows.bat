@echo off
setlocal

cd /d %~dp0

for /f "delims=" %%x in (config.txt) do (set "%%x")

conan create . %package_user%/%package_channel% -s arch=x86 -s compiler.runtime=MT || goto :error
conan upload %package_name%/%package_version%@%package_user%/%package_channel% -r %package_repo% --all || goto :error

:error
exit /b %errorlevel%