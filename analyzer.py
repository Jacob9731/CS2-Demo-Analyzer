import os

def analyze_demo(file_path):
    if not os.path.exists(file_path):
        print("File does not exist.")
        return

    print("Demo file loaded:", file_path)
    print("File size:", os.path.getsize(file_path), "bytes")
    print("More features coming soon...")

if __name__ == "__main__":
    demo_path = input("Enter path to demo file: ")
    analyze_demo(demo_path)
