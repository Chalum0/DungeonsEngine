import json
import os


def compress_json(data):
    compressed = {"segments": []}
    for segment in data["segments"]:
        compressed_segment = {
            "name": segment["name"],
            "sensitive": segment["sensitive"],
            "faces": {}
        }
        for face_name, face_data in segment["faces"].items():
            try:
                compressed_face = {
                    "v": face_data["vertices"],
                    "i": face_data["indices"]
                }
            except KeyError:
                compressed_face = {
                    "v": face_data["v"],
                    "i": face_data["i"]
                }
            compressed_segment["faces"][face_name] = compressed_face
        compressed["segments"].append(compressed_segment)
    return compressed


def modify_texture_id(data, segment_name, face_name, new_texture_id):
    for segment in data["segments"]:
        if segment["name"] == segment_name:
            face = segment["faces"][face_name]
            for i in range(5, len(face["v"]), 6):
                face["v"][i] = new_texture_id
    return data


def is_valid_texture_id(texture_id):
    try:
        texture_id = int(texture_id)
        return texture_id >= 0  # Allows any non-negative integer
    except ValueError:
        return False


def get_yes_no_input(prompt, default='n'):
    while True:
        response = input(prompt).lower() or default
        if response in ['y', 'n']:
            return response == 'y'
        print("Invalid input. Please enter 'y' or 'n'.")


def main():
    # Ask for input file
    while True:
        input_file = input("Enter the name of the JSON file to open: ")
        if os.path.exists(input_file):
            break
        print("File not found. Please try again.")

    # Load and compress the JSON data
    try:
        with open(input_file, 'r') as f:
            original_data = json.load(f)
        compressed_data = compress_json(original_data)
    except json.JSONDecodeError:
        print("Error: Invalid JSON file.")
        return

    # Process each segment and face
    for segment in compressed_data["segments"]:
        print(f"\nProcessing segment: {segment['name']}")

        # Ask if the user wants to modify this segment
        if not get_yes_no_input(f"Would you like to modify the segment '{segment['name']}'? (y/N): "):
            print(f"Skipping segment '{segment['name']}'.")
            continue

        # Ask if the segment is sensitive
        segment["sensitive"] = get_yes_no_input(f"Is the segment '{segment['name']}' sensitive? (y/N): ")

        for face_name in segment["faces"]:
            while True:
                texture_id = input(
                    f"Enter texture ID for {face_name} face (0 or positive integer, 0 for missing texture): ")
                if is_valid_texture_id(texture_id):
                    modify_texture_id(compressed_data, segment["name"], face_name, int(texture_id))
                    break
                print("Invalid texture ID. Please enter 0 or a positive integer.")

    # Save the modified JSON to the same file
    with open(input_file, 'w') as f:
        json.dump(compressed_data, f, separators=(',', ':'))

    print(f"\nProcessing complete. Modified data saved to '{input_file}'.")


if __name__ == "__main__":
    main()