@echo off
setlocal enabledelayedexpansion

if not exist "OneDark-Pro" (
    git clone https://github.com/Binaryify/OneDark-Pro.git --depth 1
)

if not exist "themes\tmp" mkdir themes\tmp

copy OneDark-Pro\themes\*.json themes\tmp\

if not exist "zed" (
    git clone https://github.com/zed-industries/zed.git --depth 1
)

cd zed
cargo build -p theme_importer
if errorlevel 1 (
    echo cargo build failed
    exit /b 1
)

set BIN=target\debug\theme_importer.exe

for %%f in (..\themes\tmp\OneDark-Pro*.json) do (
    %BIN% "%%f" --output "%%f"
    if errorlevel 1 (
        echo theme_importer failed on %%f
        exit /b 1
    )
)

cd ..
uv run merge.py
