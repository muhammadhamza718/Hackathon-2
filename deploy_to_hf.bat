@echo off
echo ========================================================
echo        HUGGING FACE DEPLOYMENT HELPER (PHASE 2)
echo ========================================================

:: 1. Navigate to the parent directory (outside the project)
cd ..

:: 2. Clean up previous attempts
if exist hf_deploy_temp (
    echo Cleaning up old temp folder...
    rmdir /s /q hf_deploy_temp
)

:: 3. Clone the Hugging Face Space
echo.
echo [1/4] Downloading your Space...
git clone https://huggingface.co/spaces/muhammadhamza7718/hackathon-2 hf_deploy_temp

:: 4. Copy the backend files
echo.
echo [2/4] Copying Phase 2 Backend files...
xcopy "Hackathon-2-Phase-1\Phase-2\backend\*" "hf_deploy_temp\" /E /Y /Q

:: 5. Navigate into the deployment folder
cd hf_deploy_temp

echo.
echo [3/4] Preparing Git...
git add .
git commit -m "Deploying Phase 2 Backend"

echo.
echo ========================================================
echo [4/4] READY TO PUSH!
echo ========================================================
echo.
echo logic: We have prepared everything in a temporary folder 'hf_deploy_temp'.
echo.
echo ACTION REQUIRED:
echo 1. The script will now try to PUSH.
echo 2. If it asks for a Password, paste your TOKEN:
echo 2. If it asks for a Password, paste your TOKEN (same as before)
echo.
pause

echo.
echo Pushing now...
git push

echo.
echo If it says 'Success' or 'Everything up-to-date', you are done!
echo You can check your Space URL: https://huggingface.co/spaces/muhammadhamza7718/hackathon-2
pause
