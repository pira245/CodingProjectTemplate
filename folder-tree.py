import os
import sys

def build_tree_lines(root, max_depth, depth=0, prefix='', is_last=True):
    if depth > max_depth:
        return []
    try:
        entries = sorted(os.listdir(root))
    except PermissionError:
        return []
    files = [e for e in entries if not os.path.isdir(os.path.join(root, e))]
    dirs = [e for e in entries if os.path.isdir(os.path.join(root, e))]
    lines = []
    total = len(dirs) + len(files)
    for idx, d in enumerate(dirs):
        is_last_dir = (idx == len(dirs) - 1 and not files)
        connector = '└───' if is_last_dir else '├───'
        lines.append(f"{prefix}{connector}{d}")
        sub_prefix = prefix + ('    ' if is_last_dir else '│   ')
        lines += build_tree_lines(os.path.join(root, d), max_depth, depth+1, sub_prefix, is_last_dir)
    for idx, f in enumerate(files):
        is_last_file = (idx == len(files) - 1)
        connector = '└───' if is_last_file else '├───'
        lines.append(f"{prefix}{connector}{f}")
    return lines

def collect_folders(root, max_depth, depth=0, folders=None, display=None, prefix=''):
    if folders is None:
        folders = []
    if display is None:
        display = []
    if depth > max_depth:
        return folders, display
    try:
        entries = sorted(os.listdir(root))
    except PermissionError:
        return folders, display
    for entry in entries:
        abs_path = os.path.join(root, entry)
        if os.path.isdir(abs_path):
            folders.append(abs_path)
            display.append(f"{prefix}{entry}/")
            collect_folders(abs_path, max_depth, depth+1, folders, display, prefix + '    ')
    return folders, display

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Print folder tree up to a given depth.")
    parser.add_argument('--depth', type=int, default=1, help='Depth level (max 5)')
    args = parser.parse_args()
    max_depth = min(args.depth, 5)
    root = os.path.dirname(os.path.abspath(sys.argv[0]))

    # Print tree diagram for root
    print(f"{root}:")
    print(".")
    tree_lines = build_tree_lines(root, max_depth)
    for line in tree_lines:
        print(line)

    # Collect folders for selection
    folders, display = collect_folders(root, max_depth)
    if not folders:
        print("No subfolders found.")
        return
    print("\nFolders:")
    for idx, line in enumerate(display):
        print(f"{idx+1}. {line}")
    while True:
        try:
            choice = int(input("Choose a folder by its number: "))
            if 1 <= choice <= len(folders):
                break
            else:
                print(f"Please enter a number between 1 and {len(folders)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    selected_folder = os.path.abspath(folders[choice-1])

    # Print tree diagram for selected folder
    print(f"\nTree for: {selected_folder}")
    print(".")
    selected_tree_lines = build_tree_lines(selected_folder, max_depth)
    for line in selected_tree_lines:
        print(line)

    # Write to markdown file
    md_path = os.path.join(root, "folder_tree.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(f"**Selected Folder:** `{selected_folder}`\n\n")
        f.write("```\n")
        f.write(".\n")
        for line in selected_tree_lines:
            f.write(f"{line}\n")
        f.write("```\n")
    print(f"\nFolder tree written to {md_path}")

if __name__ == "__main__":
    main()



