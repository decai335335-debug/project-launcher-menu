@echo off
chcp 65001 > nul
:menu
cls
echo ================================
echo        Project Launcher Menu
echo ================================
echo 1. video-sub-md
echo 2. tabbit-ai-shortcut
echo 3. win-layout-manager
echo 4. doubao-podcast
echo 5. github-repo-downloader
echo 6. auto-unzip-interactive
echo 7. sensevoice-ime
echo 0. Exit
echo ================================
set /p choice=Input number: 
if "%choice%"=="1" goto p1
if "%choice%"=="2" goto p2
if "%choice%"=="3" goto p3
if "%choice%"=="4" goto p4
if "%choice%"=="5" goto p5
if "%choice%"=="6" goto p6
if "%choice%"=="7" goto p7
if "%choice%"=="0" goto end
goto menu

:p1
call "E:\Projects\launchers\bat\01-video-sub-md.bat"
goto menu

:p2
call "E:\Projects\launchers\bat\02-tabbit-ai-shortcut.bat"
goto menu

:p3
call "E:\Projects\launchers\bat\03-win-layout-manager.bat"
goto menu

:p4
call "E:\Projects\launchers\bat\04-doubao-podcast.bat"
goto menu

:p5
call "E:\Projects\launchers\bat\05-github-repo-downloader.bat"
goto menu

:p6
call "E:\Projects\launchers\bat\06-auto-unzip-interactive.bat"
goto menu

:p7
call "E:\Projects\launchers\bat\07-sensevoice-ime.bat"
goto menu

:end
echo Exit.
pause
