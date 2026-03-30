from demoparser2 import DemoParser
import pandas as pd
import matplotlib.pyplot as plt

def main():
    demo_path = input("Enter path to demo file (.dem): ").strip()

    print("\nLoading demo...\n")
    parser = DemoParser(demo_path)

    kills = parser.parse_event("player_death")

    if kills is None or len(kills) == 0:
        print("No kills found.")
        return

    df = pd.DataFrame(kills)

    print("✅ Demo parsed!")
    print("Total kills:", len(df))

    # Kills
    kills_df = df.groupby("attacker_name").size().reset_index(name="kills")

    # Deaths
    deaths_df = df.groupby("victim_name").size().reset_index(name="deaths")

    # Merge
    stats = pd.merge(kills_df, deaths_df,
                     left_on="attacker_name",
                     right_on="victim_name",
                     how="outer").fillna(0)

    stats["K/D"] = stats["kills"] / stats["deaths"].replace(0, 1)

    # Headshots
    hs_df = df[df["headshot"] == True]
    hs_counts = hs_df.groupby("attacker_name").size().reset_index(name="headshots")

    stats = pd.merge(stats, hs_counts, on="attacker_name", how="left").fillna(0)
    stats["HS%"] = (stats["headshots"] / stats["kills"]) * 100

    print("\n=== Player Stats ===")
    print(stats[["attacker_name", "kills", "deaths", "K/D", "HS%"]]
          .sort_values(by="kills", ascending=False)
          .to_string(index=False))

    # Graph
    top = stats.sort_values(by="kills", ascending=False).head(5)

    plt.bar(top["attacker_name"], top["kills"])
    plt.title("Top 5 Players by Kills")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
