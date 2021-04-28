from wowtimeline import client
from wowtimeline import models
from wowtimeline import wow_data


import os
import asyncio
import dotenv
dotenv.load_dotenv()


WCL_CLIENT_ID = os.getenv("WCL_CLIENT_ID")
WCL_CLIENT_SECRET = os.getenv("WCL_CLIENT_SECRET")

WCL_CLIENT = client.WarcraftlogsClient(client_id=WCL_CLIENT_ID, client_secret=WCL_CLIENT_SECRET)



async def main():
    await WCL_CLIENT.update_auth_token()

    report = models.Report(report_id="2MjBG9AkwcTYhCbx")
    fights = await report.fetch_fights(WCL_CLIENT)

    import datetime

    for fight in fights:
        await fight.fetch(WCL_CLIENT, spells=None)
        player_by_id = {p.source_id: p for p in fight.players}

        query = f"""
        reportData
        {{
            report(code: "2MjBG9AkwcTYhCbx")
            {{
                events (
                    fightIDs: {fight.fight_id}
                    dataType: DamageDone
                    startTime: 0
                    endTime: 999999999999
                )
                {{
                    data
                }}
            }}
        }}
        """
        data = await WCL_CLIENT.query(query)

        events = data.get("reportData", {}).get("report", {}).get("events", {}).get("data", {})
        events = events[:3]

        for event in events:

            source = event.get("sourceID")

            spell_id = event.get("abilityGameID")
            time = event.get("timestamp", 0) - fight.start_time
            time = datetime.timedelta(milliseconds=time)
            time = str(time)
            time = time[5:11]

            player = player_by_id.get(source)
            if player:
                print(
                    f"PULL: {fight.fight_id:02d} | {time} | {player.name:15s} | Spell ID: {spell_id}"
                )
                break
        else:
            print(f"PULL: {fight.fight_id:02d} | ¯\\_(ツ)_/¯")




if __name__ == '__main__':
    asyncio.run(main())
