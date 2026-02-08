@echo off
echo ========================================================
echo        HUGGING FACE DEPLOYMENT (Backend)
echo ========================================================

:: 1. Configuration
set /p HF_TOKEN="Enter your Hugging Face Token: "
set HF_REPO=muhammadhamza7718/hackathon-2
set TEMP_DIR=hf_deploy_tmp

:: 2. Clean up previous temp folder
if exist %TEMP_DIR% (
    echo Cleaning up old temp folder...
    rmdir /s /q %TEMP_DIR%
)

:: 3. Clone the Hugging Face Space
echo.
echo [1/4] Downloading your Space...
git clone https://%HF_TOKEN%@huggingface.co/spaces/%HF_REPO% %TEMP_DIR%

:: 4. Copy the backend files from Phase-2
echo.
echo [2/4] Copying Phase 2 Backend files...
:: /E copies directories and subdirectories
:: /Y suppresses prompting to confirm you want to overwrite
:: /Q suppresses the display of xcopy messages
xcopy "Phase-2\backend\*" "%TEMP_DIR%\" /E /Y /Q

:: 5. Cleanup before commit (IMPORTANT: Prevent pushing giant .venv)
echo.
echo [3/4] Cleaning up local environment files...
if exist "%TEMP_DIR%\.venv" (
    echo Removing .venv from deployment bundle...
    rmdir /s /q "%TEMP_DIR%\.venv"
)
if exist "%TEMP_DIR%\venv" (
    echo Removing venv from deployment bundle...
    rmdir /s /q "%TEMP_DIR%\venv"
)
if exist "%TEMP_DIR%\__pycache__" (
    rmdir /s /q "%TEMP_DIR%\__pycache__"
)
:: Remove the .env to ensure it doesn't leak secrets to Git
if exist "%TEMP_DIR%\.env" del "%TEMP_DIR%\.env"

:: Remove uv.lock and pyproject.toml to force Hugging Face to use standard requirements.txt + Dockerfile
:: Sometimes these files cause Hugging Face to use a different build runner that hangs.
if exist "%TEMP_DIR%\uv.lock" del "%TEMP_DIR%\uv.lock"
if exist "%TEMP_DIR%\pyproject.toml" del "%TEMP_DIR%\pyproject.toml"

:: Add a .gitignore to the temp folder to be safe

echo .venv/ > "%TEMP_DIR%\.gitignore"
echo venv/ >> "%TEMP_DIR%\.gitignore"
echo __pycache__/ >> "%TEMP_DIR%\.gitignore"
echo .env >> "%TEMP_DIR%\.gitignore"

:: 6. Push to Hugging Face
echo.
echo [4/4] Preparing Git...
cd %TEMP_DIR%


:: Configure generic user for the commit
git config user.email "deploy@hamza.local"
git config user.name "Deployment Script"

git add .
git commit -m "Update Backend: Auto-Promotion and Admin Fixes"

echo.
echo [4/4] Pushing to Hugging Face...
git push

cd ..
echo.
echo ========================================================
echo DEPLOYMENT SUCCESSFUL!
echo URL: https://huggingface.co/spaces/%HF_REPO%
echo ========================================================
pause
