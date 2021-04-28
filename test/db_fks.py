

# IMPORT THIRD PARTY LIBRARIES
import sqlalchemy
import dotenv
import flask
dotenv.load_dotenv()

# IMPORT LOCAL LIBRARIES
# from lorgs.app import create_app
# from lorgs.models.encounters import RaidZone, RaidBoss
# from lorgs.models.specs import WowRole, WowClass, WowSpec, WowSpell
# from lorgs.models.reports import Report, Fight, Player, Cast
from lorgs.db import db


# create app instance
app = flask.Flask(__name__)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"

db.init_app(app)


class Report(db.Model):

    __tablename__ = "ReportTable"

    report_id = db.Column(db.String(64), primary_key=True)

    fights = sqlalchemy.orm.relationship("Fight", back_populates="report")
    players = sqlalchemy.orm.relationship("Player", back_populates="report")


class Fight(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    __tablename__ = "FightTable"

    fight_id = db.Column(db.Integer, primary_key=True)

    report_id = db.Column(db.String(64), db.ForeignKey('ReportTable.report_id'), primary_key=True)
    report = sqlalchemy.orm.relationship("Report", back_populates="fights")

    players = sqlalchemy.orm.relationship("Player", back_populates="fight")


class Player(db.Model):

    __tablename__ = "PlayerTable"

    report_id = db.Column(db.String(64), db.ForeignKey("ReportTable.report_id", ondelete="cascade"), primary_key=True)
    report = sqlalchemy.orm.relationship(
        "Report",
        back_populates="players",
    )

    fight_id = db.Column(db.Integer, primary_key=True)
    fight = sqlalchemy.orm.relationship(
        "Fight",
        back_populates="players",
    )

    source_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(12)) # names can be max 12 chars

    __table_args__ = (
        # constraint to make sure
        # we only map players to the correct fight inside the correct report
        sqlalchemy.schema.ForeignKeyConstraint(
            columns=["report_id", "fight_id"],
            refcolumns=["FightTable.report_id", "FightTable.fight_id"],
            ondelete="cascade"
        ),
    )



with app.app_context():
    db.create_all()

    report_b = Report(report_id="B")
    report_a = Report(report_id="A")

    fight_a1 = Fight(report=report_a, fight_id=1)
    fight_a2 = Fight(report=report_a, fight_id=2)
    fight_b1 = Fight(report=report_b, fight_id=1)

    Player(fight=fight_a1, source_id=5, name="Player A1.5")
    Player(fight=fight_a1, source_id=6, name="Player A1.6")
    Player(fight=fight_a2, source_id=5, name="Player A2.5")

    db.session.add(report_b)
    db.session.add(report_a)
    # db.session.commit()


    print("##########")
    for report in Report.query.all():
        print(f"report={report.report_id}")
        for fight in report.fights:
            print(f"report={fight.report_id} fight={fight.fight_id}")
            for player in fight.players:
                print(f"report={player.report_id} fight={player.fight_id} player={player.source_id}")
        print("===")


    # Delete
    # Report.__table__.drop()
    # Fight.__table__.drop()

    # db.session.commit()


# recreate
# db.create_all()
print("done")
