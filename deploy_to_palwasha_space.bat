@echo off
echo ========================================================
echo        HUGGING FACE DEPLOYMENT (Palwasha-49)
echo ========================================================

:: 1. Navigate to the parent directory (outside the project folder)
cd ..

:: 2. Clean up previous attempts (if any)
if exist hf_deploy_palwasha (
    echo Cleaning up old temp folder...
    rmdir /s /q hf_deploy_palwasha
)

:: 3. Clone the Hugging Face Space
echo.
echo [1/4] Downloading your Space (Palwasha-49/Hackathon-II)...
echo IMPORTANT: When prompted for a password, paste your Hugging Face TOKEN.
git clone https://huggingface.co/spaces/Palwasha-49/Hackathon-II hf_deploy_palwasha


:: 4. Copy the backend files from the current project
echo.
echo [2/4] Copying Phase 2 Backend files...
:: Note: specific path based on your project structure
xcopy "Hackathon-2-Phase-1\Phase-2\backend\*" "hf_deploy_palwasha\" /E /Y /Q

:: 5. Navigate into the deployment folder
cd hf_deploy_palwasha

echo.
echo [3/4] Preparing Git...
:: Configure user for this repo (generic) to ensure commit works
git config user.email "deploy@script.local"
git config user.name "Deployment Script"

git add .
git commit -m "Deploying Phase 2 Backend"

echo.
echo ========================================================
echo [4/4] READY TO PUSH!
echo ========================================================
echo.
echo Target: https://huggingface.co/spaces/Palwasha-49/Hackathon-II
echo Authentication: You will be prompted for your token (use it as the password).
echo.
echo Press any key to PUSH changes to the Space...
pause

echo.
echo Pushing now...
git push

echo.
echo If it says 'Success', you are done!
echo Check your Space: https://huggingface.co/spaces/Palwasha-49/Hackathon-II
pause
