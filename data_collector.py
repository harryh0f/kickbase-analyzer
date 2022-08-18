

def update_player_data():
    import pandas as pd
    from datetime import datetime
    from kickbase_api.kickbase import Kickbase
    import os

    kickbase = Kickbase()
    user, leagues = kickbase.login("fibi.mayr@gmail.com", "bYmtev-0qarcu-gykwij")

    sep = os.sep
    datetime = datetime.now()
    dt_string = datetime.strftime("%d.%m.%Y %H:%M:%S")

    players = {
        "first_name":[],
        "last_name":[],
        "id":[],
        "market_value":[],
        "market_value_trend":[],
        "team_id":[],
        "time":[]
        # "totalPoints":[],
        # "average_points":[]
        }

    for team_id in range(100):
        try:
            team_players = kickbase.team_players(str(team_id))
            for player in team_players:
                players["first_name"].append(player.first_name)
                players["last_name"].append(player.last_name)
                players["id"].append(player.id)
                players["market_value"].append(player.market_value)
                players["market_value_trend"].append(player.market_value_trend)
                players["team_id"].append(player.team_id)
                players["time"].append(pd.to_datetime(datetime))
                # players["totalPoints"].append(player.totalPoints)
                # players["average_points"].append(player.average_points)
        except:
            pass

    players_df = pd.DataFrame(players)

    if "player_data.csv" in os.listdir(f".{sep}data"):
        history_df = pd.read_csv(f".{sep}data{sep}player_data.csv")
        players_df = pd.concat([history_df, players_df], ignore_index=True)

    players_df["time"] = pd.to_datetime(players_df.time)
    players_df.date = players_df.time.dt.date

    players_df = players_df.drop_duplicates(subset=["first_name", "last_name", "date"], keep="last")
        
    players_df.to_csv(f".{sep}data{sep}player_data.csv", index=False)