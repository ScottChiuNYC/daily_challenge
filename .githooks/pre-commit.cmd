@echo off
REM Pre-commit hook (Windows cmd): regenerate yearly heatmap before every commit

python -c "from daily_challenge import draw_2025_heatmap; draw_2025_heatmap()"
IF %ERRORLEVEL% NEQ 0 (
    echo Pre-commit: draw_2025_heatmap failed. Aborting commit.
    EXIT /B 1
)

EXIT /B 0
