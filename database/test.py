import pathlib

parent_directory = pathlib.Path(__file__).parent.parent #RMS Folder

t = parent_directory / "data" / "restaurant.db"

print(t)
#db_path = SCRIPT_DIR / "data" / "restaurant.db"
# Print information about the parent directory
print(f"Parent Directory: {parent_directory}")
print(f"Does it exist? {parent_directory.exists()}")
print(f"Is it a directory? {parent_directory.is_dir()}")
