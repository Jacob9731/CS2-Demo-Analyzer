from demoparser2 import DemoParser
import pandas as pd

def main():
    demo_path = input("Enter path to demo file (.dem): ").strip()

    print("\nLoading demo... (this may take a bit)\n")
    parser = DemoParser(demo_path)

    # This pulls kill events (real match data)
    kills = parser.parse_event("player_death")

    if kills is None or len(kills) == 0:
        print("No kills found (or demo couldn't be parsed).")
        return

    df = pd.DataFrame(kills)

    print("✅ Demo parsed!")
    print("Total kills:", len(df))

    # Show a few rows so you can see it working
    print("\n--- First 10 kill events ---")
    print(df.head(10).to_string(index=False))

if __name__ == "__main__":
    main()
