from pathlib import Path
import shutil


DOWNLOADS_DIR = Path(r"C:\Users\student\Downloads")

# Map destination folder names to file extensions.
RULES = {
    "images": {".jpg", ".jpeg", ".png", ".gif"},
    "data": {".csv", ".xlsx"},
    "docs": {".txt", ".doc", ".pdf"},
    "archive": {".zip"},
}


def get_target_folder(file_path: Path) -> str | None:
    ext = file_path.suffix.lower()
    for folder_name, extensions in RULES.items():
        if ext in extensions:
            return folder_name
    return None


def unique_destination(dest_path: Path) -> Path:
    """Return a non-conflicting path by appending _1, _2, ... when needed."""
    if not dest_path.exists():
        return dest_path

    stem = dest_path.stem
    suffix = dest_path.suffix
    parent = dest_path.parent
    counter = 1

    while True:
        candidate = parent / f"{stem}_{counter}{suffix}"
        if not candidate.exists():
            return candidate
        counter += 1


def organize_downloads(downloads_dir: Path) -> None:
    if not downloads_dir.exists() or not downloads_dir.is_dir():
        raise FileNotFoundError(f"다운로드 폴더를 찾을 수 없습니다: {downloads_dir}")

    # Create destination folders in advance.
    for folder_name in RULES:
        (downloads_dir / folder_name).mkdir(parents=True, exist_ok=True)

    moved_count = 0

    for item in downloads_dir.iterdir():
        if not item.is_file():
            continue

        target_folder = get_target_folder(item)
        if target_folder is None:
            continue

        destination_dir = downloads_dir / target_folder
        destination_path = unique_destination(destination_dir / item.name)
        shutil.move(str(item), str(destination_path))
        moved_count += 1

    print(f"정리 완료: {moved_count}개 파일 이동")


if __name__ == "__main__":
    organize_downloads(DOWNLOADS_DIR)
