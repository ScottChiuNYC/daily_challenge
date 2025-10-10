@echo off
REM Configure Git to use the repository .githooks directory for hooks
git config core.hooksPath .githooks
echo Configured git to use .githooks for hooks. Run:
echo    git config --get core.hooksPath
