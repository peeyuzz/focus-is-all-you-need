import win32gui
import win32process
import psutil
import os

def get_active_window_name_windows():
    """Gets the name of the currently active application window on Windows."""
    try:
        hwnd = win32gui.GetForegroundWindow()  # Get the handle of the active window
        if hwnd == 0:
            return None  # No window active

        # Get process id that has ownership of window
        _, pid = win32process.GetWindowThreadProcessId(hwnd)  # Use win32process here
        # Get the process object using process id
        process = psutil.Process(pid)
        # Get executable name
        process_name = os.path.splitext(process.name())[0]

        return process_name  # Return the executable name (without .exe suffix)
    except Exception as e:
        print(f"Error getting window name: {e}")
        return None  # Handle errors

if __name__ == "__main__":
    active_app = get_active_window_name_windows()
    if active_app:
        print(f"The active application is: {active_app}")
    else:
        print("No active window found or error occured.")