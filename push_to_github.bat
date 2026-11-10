@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ==========================================================
echo   AI Visual Generation Index - one-click GitHub push
echo ==========================================================
echo.
echo This script pushes the local repository to your GitHub account.
echo A browser / Git Credential Manager window may open for sign-in.
echo No token is stored in this file.
echo.
set "GHUSER="
set "GHREPO="
set /p "GHUSER=Your GitHub username (e.g. Rythonme): "
if "%GHUSER%"=="" goto :cancel
set /p "GHREPO=Repository name (Enter for ai-visual-gen-index): "
if "%GHREPO%"=="" set "GHREPO=ai-visual-gen-index"
echo.
echo Target: https://github.com/%GHUSER%/%GHREPO%.git
echo.
git remote remove origin >nul 2>&1
git remote add origin https://github.com/%GHUSER%/%GHREPO%.git
git branch -M main
git push -u origin main
if errorlevel 1 goto :failed
echo.
echo [OK] Push complete.
echo Next steps on github.com/%GHUSER%/%GHREPO% :
echo   1. Settings -^> Pages -^> Build and deployment -^> Source: GitHub Actions
echo   2. Actions -^> "Weekly Update" -^> Run workflow (first full refresh)
echo   3. Update README badge URLs and data/config.json -^> project.owner / site_url
echo.
pause
exit /b 0

:failed
echo.
echo [FAILED] Push did not complete.
echo Check that the repository already exists on GitHub, your account has
echo write access, and the Git Credential Manager sign-in succeeded.
echo You can also push manually with:
echo   git remote add origin https://github.com/USERNAME/REPO.git
echo   git push -u origin main
echo.
pause
exit /b 1

:cancel
echo Cancelled, nothing was changed.
pause
exit /b 0
