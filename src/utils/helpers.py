def format_file_size(size_bytes):
    if size_bytes == 0:
        return "0 Bytes"
    size_name = ("Bytes", "KB", "MB", "GB", "TB")
    i = int(log(size_bytes, 1024))
    p = pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_name[i]}"

def validate_image_file(file_path):
    valid_extensions = ['.png', '.jpg', '.jpeg', '.gif']
    return any(file_path.endswith(ext) for ext in valid_extensions)

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def save_json(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)