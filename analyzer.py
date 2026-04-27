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
    print("Total kill events:", len(df))

    # =========================
    # PREVIEW KILL EVENTS
    # =========================
    print("\n=== First 10 Kill Events ===")
    print(df.head(10).to_string(index=False))

    # =========================
    # CHECK REQUIRED COLUMNS
    # =========================
    required_columns = ["attacker_name", "victim_name"]

    for column in required_columns:
        if column not in df.columns:
            print(f"Missing required column: {column}")
            return

    # Remove empty attackers like world damage or suicide events
    df = df[df["attacker_name"].notna()]
    df = df[df["victim_name"].notna()]
    df = df[df["attacker_name"] != ""]

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
    stats = pd.merge(
        kills_df,
        deaths_df,
        left_on="attacker_name",
        right_on="victim_name",
        how="outer"
    )

    stats["player"] = stats["attacker_name"].combine_first(stats["victim_name"])

    stats["kills"] = stats["kills"].fillna(0).astype(int)
    stats["deaths"] = stats["deaths"].fillna(0).astype(int)

    # =========================
    # K/D
    # =========================
    stats["K/D"] = stats["kills"] / stats["deaths"].replace(0, 1)
    stats["K/D"] = stats["K/D"].round(2)

    # =========================
    # HEADSHOTS
    # =========================
    if "headshot" in df.columns:
        hs_df = df[df["headshot"] == True]
        hs_counts = hs_df.groupby("attacker_name").size().reset_index(name="headshots")

        stats = pd.merge(
            stats,
            hs_counts,
            left_on="player",
            right_on="attacker_name",
            how="left"
        )

        stats["headshots"] = stats["headshots"].fillna(0).astype(int)
    else:
        stats["headshots"] = 0

    stats["HS%"] = (stats["headshots"] / stats["kills"].replace(0, 1)) * 100
    stats["HS%"] = stats["HS%"].round(2)

    # =========================
    # ADR ESTIMATE
    # =========================
    if "dmg_health" in df.columns:
        dmg_df = df.groupby("attacker_name")["dmg_health"].sum().reset_index(name="total_damage")

        if "round" in df.columns:
            rounds = df["round"].nunique()
        else:
            rounds = 1

        dmg_df["ADR"] = dmg_df["total_damage"] / rounds

        stats = pd.merge(
            stats,
            dmg_df[["attacker_name", "ADR"]],
            left_on="player",
            right_on="attacker_name",
            how="left"
        )

        stats["ADR"] = stats["ADR"].fillna(0).round(2)
    else:
        stats["ADR"] = 0

    # =========================
    # CLEAN FINAL STATS TABLE
    # =========================
    final_stats = stats[["player", "kills", "deaths", "K/D", "headshots", "HS%", "ADR"]]
    final_stats = final_stats.sort_values(by="kills", ascending=False)

    print("\n=== Player Stats ===")
    print(final_stats.to_string(index=False))

    # =========================
    # SAVE TO CSV
    # =========================
    final_stats.to_csv("player_stats.csv", index=False)
    print("\n📁 Stats saved to player_stats.csv")

    # =========================
    # GRAPHS
    # =========================
    top = final_stats.head(5)

    # Kills graph
    plt.figure(figsize=(8, 5))
    plt.bar(top["player"], top["kills"])
    plt.title("Top 5 Players by Kills")
    plt.xlabel("Player")
    plt.ylabel("Kills")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("top_5_kills.png")
    plt.show()

    # K/D graph
    plt.figure(figsize=(8, 5))
    plt.bar(top["player"], top["K/D"])
    plt.title("Top 5 Players by K/D")
    plt.xlabel("Player")
    plt.ylabel("K/D")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("top_5_kd.png")
    plt.show()

    # Headshot % graph
    plt.figure(figsize=(8, 5))
    plt.bar(top["player"], top["HS%"])
    plt.title("Top 5 Players by Headshot %")
    plt.xlabel("Player")
    plt.ylabel("Headshot %")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("top_5_headshot_percent.png")
    plt.show()

    print("\n📊 Graphs saved as PNG files:")
    print("- top_5_kills.png")
    print("- top_5_kd.png")
    print("- top_5_headshot_percent.png")


if __name__ == "__main__":
    main()
