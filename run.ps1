
# Start the Python and npm processes in hidden PowerShell windows
Start-Process PowerShell -ArgumentList "-NoExit", "-Command", "python app.py" -WindowStyle Hidden
Start-Process PowerShell -ArgumentList "-NoExit", "-Command", "cd vbms-frontend; npm start" -WindowStyle Hidden
