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

    # =========================
    # KILLS
    # =========================
    kills_df = df.groupby("attacker_name").size().reset_index(name="kills")

    # =========================
    # DEATHS
    # =========================
    deaths_df = df.groupby("victim_name").size().reset_index(name="deaths")

    # =========================
    # MERGE KILLS + DEATHS
    # =========================
    stats = pd.merge(kills_df, deaths_df,
                     left_on="attacker_name",
                     right_on="victim_name",
                     how="outer").fillna(0)

    # Create single player column (cleaner)
    stats["player"] = stats["attacker_name"].combine_first(stats["victim_name"])

    # =========================
    # K/D
    # =========================
    stats["K/D"] = stats["kills"] / stats["deaths"].replace(0, 1)

    # =========================
    # HEADSHOTS
    # =========================
    hs_df = df[df["headshot"] == True]
    hs_counts = hs_df.groupby("attacker_name").size().reset_index(name="headshots")

    stats = pd.merge(stats, hs_counts, left_on="player", right_on="attacker_name", how="left").fillna(0)

    stats["HS%"] = (stats["headshots"] / stats["kills"].replace(0, 1)) * 100

    # =========================
    # ADR (Average Damage / Round)
    # =========================
    if "dmg_health" in df.columns:
        dmg_df = df.groupby("attacker_name")["dmg_health"].sum().reset_index(name="total_damage")

        rounds = df["round"].nunique() if "round" in df.columns else 1
        dmg_df["ADR"] = dmg_df["total_damage"] / rounds

        stats = pd.merge(stats, dmg_df[["attacker_name", "ADR"]],
                         left_on="player", right_on="attacker_name", how="left").fillna(0)
    else:
        stats["ADR"] = 0

    # =========================
    # DISPLAY
    # =========================
    stats = stats.sort_values(by="kills", ascending=False)

    print("\n=== Player Stats ===")
    print(stats[["player", "kills", "deaths", "K/D", "HS%", "ADR"]]
          .to_string(index=False))

    # =========================
    # SAVE TO CSV
    # =========================
    stats.to_csv("player_stats.csv", index=False)
    print("\n📁 Stats saved to player_stats.csv")

    # =========================
    # GRAPHS
    # =========================
    top = stats.head(5)

    # Kills graph
    plt.figure()
    plt.bar(top["player"], top["kills"])
    plt.title("Top 5 Players by Kills")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # K/D graph
    plt.figure()
    plt.bar(top["player"], top["K/D"])
    plt.title("Top 5 Players by K/D")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # Headshot % graph
    plt.figure()
    plt.bar(top["player"], top["HS%"])
    plt.title("Top 5 Players by Headshot %")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
