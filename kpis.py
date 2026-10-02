import pandas as pd

from database import engine


def load_chats():
    df = pd.read_sql_table(
        "chat_sessions",
        engine,
        parse_dates=["started_at", "ended_at", "received_at"],

    )
    return df


def add_handle_time(df):
    df["handle_minutes"] = (df["ended_at"] - df["started_at"]  # vectorizacia
                            ).dt.total_seconds() / 60
    return df


def overall_kpis(df):
    return {
        "volume": len(df),
        "aht_minutes": float(round(df["handle_minutes"]. mean(), 1)),
        "median_minutes": float(round(df["handle_minutes"].median(), 1)),
    }


def kpis_by(df, column):
    return (
        df.groupby(column).agg(  # agregacia
            volume=("chat_id", "count"),
            aht_minutes=("handle_minutes", "mean"),

        )
        .round(1)
        .sort_values("aht_minutes")
    )


# (IANA timezone) i know EU but, international time zone database-asia
def add_locat_time(df, tz="Asia/Tbilisi"):
    df["started_local"] = df["started_at"].dt.tz_localize(
        "UTC").dt.tz_convert(tz)
    df["date"] = df["started_local"].dt.date
    df["hour"] = df["started_local"].dt.hour

    return df


if __name__ == "__main__":
    df = add_locat_time(add_handle_time(load_chats()))
    print(df[["chat_id", "agent_name", "handle_minutes",]].head())
    print()
    print(overall_kpis(df))
    print()
    print(kpis_by(df, "agent_name"))
    print()
    print(kpis_by(df, "channel"))
    print()
    print(kpis_by(df, "date").sort_index())
    print()
    print(kpis_by(df, "hour").sort_index())
