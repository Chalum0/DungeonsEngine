import pygame
import ctypes
import time
import os
import shutil
import json

# Configuration for saving window position and size
CONFIG_FILE = "explorer_config.json"

def save_window_config(position, size):
    """Save window position and size to config file"""
    config = {
        "position": position,
        "size": size
    }
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f)
        print(f"Window configuration saved: {position}, {size}")
    except Exception as e:
        print(f"Failed to save window configuration: {e}")

def load_window_config():
    """Load window position and size from config file"""
    default_config = {
        "position": (100, 100),
        "size": (200, 400)
    }

    if not os.path.exists(CONFIG_FILE):
        return default_config

    try:
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)

        # Validate the loaded data
        if not all(key in config for key in ["position", "size"]):
            return default_config

        # Ensure values are tuples with 2 elements
        position = tuple(config["position"])
        size = tuple(config["size"])

        if len(position) != 2 or len(size) != 2:
            return default_config

        # Make sure size is not smaller than minimum
        size = (max(size[0], 200), max(size[1], 400))

        print(f"Loaded window configuration: {position}, {size}")
        return {"position": position, "size": size}
    except Exception as e:
        print(f"Failed to load window configuration: {e}")
        return default_config

class FileOrFolder:
    def __init__(self, path, name, deepness=0):
        self.name = name
        self.children = []
        self.path = path
        self.deepness = deepness
        self.opened = False
        self.explore()

    def explore(self):
        if os.path.isdir(self.path):
            try:
                for element in os.listdir(self.path):
                    if not element.startswith(".") and not element.startswith("_"):
                        child_path = os.path.join(self.path, element)
                        self.children.append(FileOrFolder(child_path, element, self.deepness + 1))
            except (PermissionError, FileNotFoundError):
                pass

    def get_children(self):
        names = [self.name]
        for child in self.children:
            names.extend(child.get_children())
        return names

    def get_direct_children(self):
        names = []
        for child in self.children:
            names.append(child.name)
        return names

    def toggle_opening(self):
        self.opened = not self.opened

    def get_children_class(self):
        result = [self]

        if self.opened:
            folders = []
            files = []

            for child in self.children:
                if os.path.isdir(child.path):
                    folders.append(child)
                else:
                    files.append(child)

            folders = sorted(folders, key=lambda c: c.name.lower())
            files = sorted(files, key=lambda c: c.name.lower())

            for folder in folders:
                result.extend(folder.get_children_class())

            for file in files:
                result.extend(file.get_children_class())

        return result

def sort_classes(class_list):
    return sorted(class_list, key=lambda c: c.name.lower())

# --------------------------------------------------------------------
# START Pygame setup
pygame.init()
minw = 200
minh = 400

# Load window configuration
window_config = load_window_config()
initial_position = window_config["position"]
initial_size = window_config["size"]

# Set window position
os.environ['SDL_VIDEO_WINDOW_POS'] = f"{initial_position[0]},{initial_position[1]}"

# Create the window with the saved size
screen = pygame.display.set_mode(initial_size, pygame.RESIZABLE)
pygame.display.set_caption("File Explorer")

# Variables to track window position
window_position = initial_position
window_moved = False

# Enable dark mode title bar (Windows-only trick)
def enable_dark_mode():
    try:
        hwnd = pygame.display.get_wm_info()["window"]
        DWMWA_USE_IMMERSIVE_DARK_MODE = 20

        ctypes.windll.dwmapi.DwmSetWindowAttribute(
            hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE,
            ctypes.byref(ctypes.c_int(1)),
            ctypes.sizeof(ctypes.c_int)
        )

        ctypes.windll.user32.ShowWindow(hwnd, 6)  # Minimize
        time.sleep(0.05)
        ctypes.windll.user32.ShowWindow(hwnd, 9)  # Restore

        print("Dark mode title bar enabled.")
    except Exception as e:
        print(f"Failed to enable dark mode: {e}")

enable_dark_mode()

# Initialize the root folder and keep track of opened paths
def initialize_file_system():
    global root, elements, opened_paths
    root = FileOrFolder("./", "root")
    root.toggle_opening()

    # Restore previously opened folders
    if 'opened_paths' in globals():
        restore_opened_folders(root, opened_paths)
    else:
        opened_paths = [os.path.abspath("./")]

    elements = root.get_children_class()

def restore_opened_folders(folder, paths):
    """Recursively restore opened state for folders that were previously open"""
    for child in folder.children:
        abs_path = os.path.abspath(child.path)
        if os.path.isdir(child.path) and abs_path in paths:
            child.opened = True
            restore_opened_folders(child, paths)

# Function to collect currently opened paths
def collect_opened_paths(folder):
    paths = []
    if folder.opened:
        paths.append(os.path.abspath(folder.path))
        for child in folder.children:
            if os.path.isdir(child.path):
                paths.extend(collect_opened_paths(child))
    return paths

opened_paths = [os.path.abspath("./")]
initialize_file_system()

fonts = pygame.sysfont.get_fonts()
emojis = [font for font in fonts if "emoji" in font]
font = pygame.font.SysFont(emojis[0] if emojis else None, 15)
input_font = pygame.font.SysFont(None, 24)

running = True

# This offset will track how much we scroll
scroll_offset = 0

# Add a timer for refreshing the file tree every 10 seconds
last_refresh_time = time.time()
REFRESH_INTERVAL = 10  # 10 seconds

# Track last window position and size to detect changes
last_window_size = initial_size
last_save_time = time.time()
SAVE_INTERVAL = 1.0  # Save at most once per second to avoid excessive writes

def get_popup_info():
    popup_options = ["New Folder", "New File", "Rename", "Delete"]
    popup_options_rendered = [font.render(text, True, (255, 255, 255)) for text in popup_options]
    popup_options_rendered_sizes = [text.get_rect().size[0] for text in popup_options_rendered]
    popup_options_rects = []
    for i, text in enumerate(popup_options_rendered):
        text_rect = text.get_rect()
        text_rect.topleft = (15-5, i*20+17-2)
        text_rect.width = max(popup_options_rendered_sizes) + 10
        text_rect.height += 4
        popup_options_rects.append(text_rect)
    popup_width = max(popup_options_rendered_sizes) + 30

    return popup_width, 20*len(popup_options), popup_options_rects

def get_popup_menu_surface(pos):
    popup_options = ["New Folder", "New File", "Rename", "Delete"]
    popup_options_rendered = [font.render(text, True, (255, 255, 255)) for text in popup_options]
    popup_options_rendered_sizes = [text.get_rect().size[0] for text in popup_options_rendered]
    popup_width = max(popup_options_rendered_sizes) + 30

    popup_surface = pygame.surface.Surface((popup_width, 20*len(popup_options)+30))

    popup_surface.fill((50, 50, 50))
    for i, text in enumerate(popup_options_rendered):
        text_rect = text.get_rect()
        text_rect.topleft = (15-5, i*20+17-2)
        text_rect.width = max(popup_options_rendered_sizes) + 10
        text_rect.height += 4
        if text_rect.collidepoint((pygame.mouse.get_pos()[0] - pos[0], pygame.mouse.get_pos()[1] - pos[1])):
            pygame.draw.rect(popup_surface, (100, 100, 100), text_rect, border_radius=3)
        popup_surface.blit(text, (15, i*20+17))

    return popup_surface

def create_input_dialog(prompt, default_text=""):
    """Create a dialog for text input with proper sizing and continuous backspace"""
    input_text = default_text
    input_active = True

    # For handling continuous backspace with initial delay
    backspace_down = False
    backspace_timer = 0
    backspace_initial_delay = 1000  # 1 second initial delay before continuous deletion
    backspace_repeat = 30  # Repeat interval in milliseconds

    # Get screen dimensions to ensure dialog fits
    screen_width, screen_height = screen.get_size()
    dialog_width = min(300, screen_width - 20)
    dialog_height = min(100, screen_height - 20)

    while input_active:
        current_time = pygame.time.get_ticks()

        # Handle continuous backspace with initial delay
        keys = pygame.key.get_pressed()
        if keys[pygame.K_BACKSPACE]:
            if not backspace_down:
                backspace_down = True
                backspace_timer = current_time + backspace_initial_delay
                input_text = input_text[:-1]  # Delete one character immediately
            elif current_time >= backspace_timer:
                input_text = input_text[:-1]
                backspace_timer = current_time + backspace_repeat
        else:
            backspace_down = False

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                return None
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_RETURN:
                    input_active = False
                elif ev.key == pygame.K_ESCAPE:
                    return None
                elif ev.key != pygame.K_BACKSPACE:  # Backspace handled separately above
                    input_text += ev.unicode

        # Draw the dialog
        dialog_x = (screen_width - dialog_width) // 2
        dialog_y = (screen_height - dialog_height) // 2

        dialog_surface = pygame.Surface((dialog_width, dialog_height))
        dialog_surface.fill((60, 60, 60))

        # Draw prompt
        prompt_surface = font.render(prompt, True, (255, 255, 255))
        dialog_surface.blit(prompt_surface, (10, 10))

        # Draw input box
        input_box = pygame.Rect(10, 40, dialog_width - 20, 30)
        pygame.draw.rect(dialog_surface, (100, 100, 100), input_box, border_radius=3)

        # Draw input text (with scrolling if text is too long)
        text_surface = input_font.render(input_text, True, (255, 255, 255))
        text_width = text_surface.get_width()

        # Check if text is too long for the box
        if text_width > input_box.width - 10:
            # Calculate display offset to show the end of text
            display_offset = text_width - (input_box.width - 15)
            input_box_surface = pygame.Surface((input_box.width - 10, input_box.height - 10))
            input_box_surface.fill((100, 100, 100))
            input_box_surface.blit(text_surface, (-display_offset, 0))
            dialog_surface.blit(input_box_surface, (input_box.x + 5, input_box.y + 5))
        else:
            dialog_surface.blit(text_surface, (input_box.x + 5, input_box.y + 5))

        # Draw cursor
        if text_width <= input_box.width - 10:
            cursor_pos = input_font.size(input_text)[0] + input_box.x + 5
        else:
            cursor_pos = input_box.x + input_box.width - 5

        if time.time() % 1 > 0.5:  # Blinking cursor
            pygame.draw.line(dialog_surface, (255, 255, 255),
                             (cursor_pos, input_box.y + 5),
                             (cursor_pos, input_box.y + 25), 2)

        # Draw to screen
        screen.fill((30, 30, 30))
        screen.blit(dialog_surface, (dialog_x, dialog_y))
        pygame.display.flip()

        # Cap the frame rate
        pygame.time.Clock().tick(60)

    return input_text

def create_new_folder(parent_path):
    """Create a new folder at the given path"""
    folder_name = create_input_dialog("Enter folder name:", "New Folder")
    if folder_name and folder_name.strip():
        try:
            new_folder_path = os.path.join(parent_path, folder_name)
            if not os.path.exists(new_folder_path):
                os.makedirs(new_folder_path)
                return True
            else:
                print(f"Folder already exists: {new_folder_path}")
        except Exception as e:
            print(f"Error creating folder: {e}")
    return False

def create_new_file(parent_path):
    """Create a new file at the given path"""
    file_name = create_input_dialog("Enter file name:", "script.py")  # Changed default to script.py
    if file_name and file_name.strip():
        try:
            new_file_path = os.path.join(parent_path, file_name)
            if not os.path.exists(new_file_path):
                with open(new_file_path, 'w') as f:
                    pass  # Just create an empty file
                return True
            else:
                print(f"File already exists: {new_file_path}")
        except Exception as e:
            print(f"Error creating file: {e}")
    return False

def rename_item(item_path):
    """Rename a file or folder"""
    old_name = os.path.basename(item_path)
    new_name = create_input_dialog("Enter new name:", old_name)
    if new_name and new_name.strip() and new_name != old_name:
        try:
            parent_dir = os.path.dirname(item_path)
            new_path = os.path.join(parent_dir, new_name)
            if not os.path.exists(new_path):
                os.rename(item_path, new_path)
                return True
            else:
                print(f"Item already exists: {new_path}")
        except Exception as e:
            print(f"Error renaming item: {e}")
    return False

def delete_item(item_path):
    """Delete a file or folder"""
    try:
        if os.path.isdir(item_path):
            shutil.rmtree(item_path)
        else:
            os.remove(item_path)
        return True
    except Exception as e:
        print(f"Error deleting item: {e}")
        return False

popup_menu_hidden = True
popup_menu_pos = [0, 0]
popup_menu_target = None
popup_menu_target_rect = None

try:
    while running:
        screen.fill((30, 30, 30))

        # Check if we need to refresh the file tree (every 10 seconds)
        current_time = time.time()
        if current_time - last_refresh_time >= REFRESH_INTERVAL:
            last_refresh_time = current_time
            # Save opened paths before refreshing
            opened_paths = collect_opened_paths(root)
            # Refresh the file system
            initialize_file_system()
            print("Auto-refreshed file tree")

        # Check if window size or position has changed
        current_size = screen.get_size()
        current_pos = pygame.display.get_window_pos() if hasattr(pygame.display, 'get_window_pos') else window_position

        # Update window position tracking if supported
        if hasattr(pygame.display, 'get_window_pos'):
            window_position = current_pos

        # Save window configuration if it changed and enough time has passed since last save
        size_changed = current_size != last_window_size
        pos_changed = current_pos != window_position

        if (size_changed or pos_changed) and current_time - last_save_time >= SAVE_INTERVAL:
            save_window_config(current_pos, current_size)
            last_window_size = current_size
            window_position = current_pos
            last_save_time = current_time

        # Calculate the total height of all elements
        line_height = 20
        total_height = len(elements) * line_height
        screen_width, screen_height = screen.get_size()

        # Draw each element, offset by scroll_offset
        elements_rects = []
        for i, element in enumerate(elements):
            # Decide on the icon
            if os.path.isdir(element.path):
                icon = "🏷" if "config.json" in element.get_direct_children() else "📁"
                text_str = f"{' ' * (4*element.deepness)}{icon} {element.name}"
            else:
                # Simple icon logic
                name = element.name
                if name.endswith("json"):
                    if "model" in name:
                        icon = "🧸"
                    elif "config" in name:
                        icon = "⚙️"
                    else:
                        icon = "🧾"
                elif name.endswith("py"):
                    icon = "🐍"
                elif any(name.endswith(ext) for ext in ["png","jpeg","jpg","webp"]):
                    icon = "🖼️"
                else:
                    icon = "❔"
                text_str = f"{' ' * (4*element.deepness)}{icon}{element.name}"

            text_surface = font.render(text_str, True, (255, 255, 255))
            rect = text_surface.get_rect()
            rect.width = screen_width - 20
            # Apply scroll_offset here
            rect.topleft = (10, i * line_height + scroll_offset)

            # Highlight if mouse is over
            if rect.collidepoint(pygame.mouse.get_pos()) and popup_menu_hidden:
                pygame.draw.rect(screen, (100, 100, 100), rect, border_radius=3)
            if rect == popup_menu_target_rect and not popup_menu_hidden:
                pygame.draw.rect(screen, (100, 100, 100), rect, border_radius=3)

            screen.blit(text_surface, rect)
            elements_rects.append((element, rect))

        if not popup_menu_hidden:
            screen.blit(get_popup_menu_surface(popup_menu_pos), popup_menu_pos)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Save window configuration before exiting
                current_pos = pygame.display.get_window_pos() if hasattr(pygame.display, 'get_window_pos') else window_position
                save_window_config(current_pos, screen.get_size())
                running = False

            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((max(event.w, minw), max(event.h, minh)), pygame.RESIZABLE)
                # Window size change is tracked in the main loop

            elif event.type == pygame.WINDOWMOVED:
                # Update window position when moved (if event is available)
                if hasattr(event, 'x') and hasattr(event, 'y'):
                    window_position = (event.x, event.y)
                    window_moved = True

            elif event.type == pygame.MOUSEWHEEL:
                scroll_offset += event.y * 20

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    if popup_menu_hidden:
                        for element, rect in elements_rects:
                            if rect.collidepoint(event.pos):
                                element.toggle_opening()
                                # Save the opened state before rebuilding the list
                                opened_paths = collect_opened_paths(root)
                                elements = root.get_children_class()
                    else:
                        for i, rect in enumerate(get_popup_info()[2]):
                            rect_pos = (rect.x + popup_menu_pos[0], rect.y + popup_menu_pos[1], rect.width, rect.height)
                            popup_rect = pygame.Rect(rect_pos)

                            if popup_rect.collidepoint(event.pos):
                                action_performed = False
                                target_path = popup_menu_target.path

                                # Save opened paths before any action
                                opened_paths = collect_opened_paths(root)

                                if i == 0:  # Create new folder
                                    if os.path.isdir(target_path):
                                        action_performed = create_new_folder(target_path)
                                    else:
                                        action_performed = create_new_folder(os.path.dirname(target_path))

                                elif i == 1:  # Create new file
                                    if os.path.isdir(target_path):
                                        action_performed = create_new_file(target_path)
                                    else:
                                        action_performed = create_new_file(os.path.dirname(target_path))

                                elif i == 2:  # Rename
                                    action_performed = rename_item(target_path)

                                elif i == 3:  # Delete
                                    action_performed = delete_item(target_path)

                                if action_performed:
                                    # Rebuild the file structure but maintain opened state
                                    initialize_file_system()

                                popup_menu_hidden = True
                                break
                        else:
                            popup_menu_hidden = True

                if event.button == 3:  # Right click
                    popup_menu_hidden = True  # Hide any existing menu

                    for element, rect in elements_rects:
                        if rect.collidepoint(event.pos):
                            popup_menu_hidden = False
                            popup_menu_spawn_point = list(event.pos)

                            # Adjust popup position if it would go off screen
                            popup_width, popup_height = get_popup_info()[:2]
                            if event.pos[0] + popup_width > screen_width:
                                popup_menu_spawn_point[0] = screen_width - popup_width
                            if event.pos[1] + popup_height > screen_height:
                                popup_menu_spawn_point[1] = screen_height - popup_height

                            popup_menu_pos = popup_menu_spawn_point
                            popup_menu_target = element
                            popup_menu_target_rect = rect
                            break

        # Constrain scrolling
        if total_height > screen_height:
            max_scroll_up = 0
            max_scroll_down = screen_height - total_height
            if scroll_offset > max_scroll_up:
                scroll_offset = max_scroll_up
            elif scroll_offset < max_scroll_down:
                scroll_offset = max_scroll_down
        else:
            # If content fits the screen, reset offset
            scroll_offset = 0

finally:
    # Ensure we save configuration when exiting
    try:
        current_pos = pygame.display.get_window_pos() if hasattr(pygame.display, 'get_window_pos') else window_position
        save_window_config(current_pos, screen.get_size())
    except:
        pass
    pygame.quit()