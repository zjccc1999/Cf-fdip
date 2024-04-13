@echo off
setlocal enabledelayedexpansion
set CSV_DIR=C:\Users\Administrator\Desktop\反代IP库
cd /d %CSV_DIR%
set FIRST_FILE=true
(for %%G in (*.csv) do (
    if !FIRST_FILE!==true (
        < "%%G" (
            set /p HEADER=
            echo !HEADER!
        )
        set FIRST_FILE=false
    ) else (
        more +1 "%%G"
    )
)) > addressescsv.csv
echo CSV files have been merged successfully.
@endlocal
pause
