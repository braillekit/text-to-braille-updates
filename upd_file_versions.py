import os
import pefile

# Define constants
FILES_DIR = 'Files'
UPDATES_FILE = os.path.join(FILES_DIR, '_updates.txt')

def get_file_version(filepath):
    """
    Extracts the version information from a .exe or .dll file.
    Returns the version string (e.g., "1.0.0.0") or None if not found/error.
    """
    try:
        pe = pefile.PE(filepath)
        if hasattr(pe, 'VS_FIXEDFILEINFO'):
            version_info = pe.VS_FIXEDFILEINFO[0]
            major = version_info.FileVersionMS >> 16
            minor = version_info.FileVersionMS & 0xFFFF
            patch = version_info.FileVersionLS >> 16
            build = version_info.FileVersionLS & 0xFFFF
            return f"{major}.{minor}.{patch}.{build}"
    except pefile.PEFormatError:
        pass # Not a valid PE file or other format error
    except Exception as e:
        print(f"Error reading version from {filepath}: {e}")
    return None

def main():
    update_entries = []
    
    print("--- 開始掃描檔案並蒐集資訊 ---")

    # 1. Read target directory and 2. Collect file info with feedback
    for filename in os.listdir(FILES_DIR):
        filepath = os.path.join(FILES_DIR, filename)

        if filename == os.path.basename(UPDATES_FILE):
            continue # Skip the updates file itself

        if os.path.isfile(filepath):
            version = None
            if filename.lower().endswith(('.exe', '.dll')):
                version = get_file_version(filepath)
                if version:
                    print(f"更新 {filename} (版本: {version})")
                    update_entries.append((filename, version))
                else:
                    print(f"無法讀取 {filename} 版本，將標示為 ?")
                    update_entries.append((filename, '?'))
            else:
                print(f"加入 {filename}")
                update_entries.append((filename, '?'))
    
    print("--- 檔案蒐集完成，開始排序與格式化 ---")

    # 4. Sort entries by filename
    update_entries.sort(key=lambda x: x[0].lower())

    # 5. Format output
    max_filename_len = 0
    if update_entries:
        max_filename_len = max(len(entry[0]) for entry in update_entries)

    formatted_lines = []
    for filename, version in update_entries:
        padded_filename = filename.ljust(max_filename_len)
        formatted_lines.append(f"{padded_filename} ; {version}")

    # Write to _updates.txt
    try:
        with open(UPDATES_FILE, 'w', encoding='utf-8') as f:
            for line in formatted_lines:
                f.write(line + '\n')
        print(f"--- {UPDATES_FILE} 已成功更新 ---")
    except Exception as e:
        print(f"寫入 {UPDATES_FILE} 時發生錯誤: {e}")

if __name__ == "__main__":
    main()
