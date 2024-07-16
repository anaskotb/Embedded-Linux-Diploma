import pyautogui
from time import sleep

def open_vscode():
    # Open the Start Menu
    pyautogui.press('win')
    sleep(1)
    # Type 'Visual Studio Code' and press Enter
    pyautogui.write('Visual Studio Code')
    sleep(1)
    pyautogui.press('enter')
    sleep(5)  # Wait for VS Code to open

def open_extensions_view():
    # Press Ctrl+Shift+X to open the Extensions view in VS Code
    pyautogui.hotkey('ctrl', 'shift', 'x')
    sleep(2)

def install_extension(extension_name):
    location1 = None
    while location1 is None:
        try:
            location1 = pyautogui.locateOnScreen('SearchExtensions.png', confidence=0.8)
            if location1 is not None:
                pyautogui.click(location1)
                print("Search found.")
                sleep(3)
                pyautogui.write(extension_name)
                sleep(2)
                pyautogui.press('enter')
                sleep(2)
                
                # Click on the install button (assuming it is the first result)
                location = None
                while location is None:
                    try:
                        location = pyautogui.locateOnScreen('install_button.png', confidence=0.8)
                        if location is not None:
                            pyautogui.click(location)
                            print(f"Installing {extension_name}...")
                            sleep(5)  # Wait for the installation to complete
                            pyautogui.click(location1)
                            pyautogui.hotkey('ctrl', 'a')
                            sleep(1)
                            pyautogui.press('backspace')
                            sleep(1)
                            
                        else:
                            print(f"Searching for the install button for {extension_name}...")
                            sleep(1)
                    except pyautogui.ImageNotFoundException:
                        print(f"Install button for {extension_name} not found, retrying...")
                        sleep(1)
                        
            else:
                print("Searching for the search button.")
                location1 = None
                sleep(1)
        except pyautogui.ImageNotFoundException:
            print("Search button not found, retrying...")
            sleep(1)

def main():
    open_vscode()
    open_extensions_view()

    extensions = [
        'clangd',
        'C++ TestMate',
        'C++ Helper',
        'CMake',
        'CMake Tools'
    ]

    for extension in extensions:
        install_extension(extension)
        sleep(2)

    print("All extensions installed.")

if __name__ == "__main__":
    main()
