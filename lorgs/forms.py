# IMPORT THIRD PARTY LIBRARIES
from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms import validators
from wtforms.fields import html5


#:str: regex expression to match warcraftlogs-link
WCL_LINK_REGEX = (

    r"(https?\:\/\/www\.warcraftlogs\.com\/reports\/)?"
    r"(?P<code>\w{16})"
)


class CustomReportForm(FlaskForm):
    """Form to load a custom Report."""

    report_link = html5.URLField(
        "report_link",
        validators=[
            validators.DataRequired(),
            validators.Regexp(
                regex=WCL_LINK_REGEX,
                message="invalid link."
            )
        ],

        render_kw={
            "placeholder": "https://www.warcraftlogs.com/reports/...",
        }
    )

    load_report = SubmitField()
