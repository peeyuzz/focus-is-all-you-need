import pygetwindow as gw
import psutil
import uiautomation as auto
import time
import win32process
import win32gui
import win32api

def get_foreground_window_info():
    """
    Gets the name of the current foreground window, and if the window
    is Edge or Chrome, retrieves the current URL being browsed.

    Returns:
        str: The name of the window or the URL if it is a browser
    """

    try:
        # Get the active window
        active_window = gw.getActiveWindow()

        if not active_window:
            return "No active window found"

        # Get the process ID of the active window
        try:
            hwnd = active_window._hWnd
            thread_id, pid = win32process.GetWindowThreadProcessId(hwnd)
            process = psutil.Process(pid)
            process_name = process.name().lower()
        except Exception as pid_e:
            return f"Error getting process info: {pid_e}"

        if process_name in ["msedge.exe", "chrome.exe"]:
            # Use UIA to get the URL from the address bar
            url = get_browser_url()
            if url:
                return url
            else:
                return active_window.title  # If no URL return the title

        return active_window.title  # Return the title

    except Exception as e:
        return f"Error: {e}"


def get_browser_url():
    """
    Uses UIA to get the URL from the address bar of a Chrome or Edge window.

    Returns:
        str: The URL being browsed or None if not found.
    """
    try:
        # Get the active window using UIA
        active_control = auto.WindowControl(searchFromControl=auto.GetRootControl(), searchDepth=1,ClassName="Chrome_WidgetWin_1")
        if not active_control.Exists():
            active_control = auto.WindowControl(searchFromControl=auto.GetRootControl(), searchDepth=1,ClassName="Microsoft Edge")
            if not active_control.Exists():
              return None

        # Find the address bar control based on its AutomationId or classname
        if active_control.ClassName == "Chrome_WidgetWin_1":
            address_bar = active_control.EditControl(searchDepth=8,ClassName="NativeEditBox")
        elif active_control.ClassName == "Microsoft Edge":
            address_bar = active_control.EditControl(searchDepth=8, AutomationId="addressEditBox")

        if address_bar.Exists():
          return address_bar.GetValuePattern().Value
        else:
            return None

    except Exception as e:
        print(f"Error retrieving browser URL: {e}")
        return None

if __name__ == "__main__":
    while True:
        window_info = get_foreground_window_info()
        print(f"Current foreground window: {window_info}")
        time.sleep(2)  # Check every 2 seconds