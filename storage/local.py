def save_local(file_path, data):
    with open(file_path, 'wb') as f:
        f.write(data)
    print(f"Backup saved to {file_path}")
