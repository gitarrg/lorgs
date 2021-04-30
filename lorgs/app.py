#!/usr/bin/env python
"""Main Entrypoint to create the FlaskAPP."""

# IMPORT STANDARD LIBRARIES
import os

# IMPORT THIRD PARTY LIBRARIES
import flask

# IMPORT LOCAL LIBRARIES
from lorgs.routes import api
from lorgs.routes import views
from lorgs import utils
from lorgs import cache
from lorgs import models
from lorgs.logger import logger



def load_spell_icons():
    logger.info("[load spell icons] start")
    return
    spell_infos = cache.Cache.get("spell_infos") or []
    if not spell_infos:
        logger.warning("SPELL INFO NOT FOUND!")
        return

    # attach data to spells
    for spell in models.WowSpell.all:
        spell_info = spell_infos.get(spell.spell_id, {})
        if not spell_info:
            logger.warning("No Spell Info for: %s", spell.spell_id)
            continue

        # check for existing values so we keep manual overwrites
        spell.spell_name = spell.spell_name or spell_info.get("name")
        spell.icon_name = spell.icon_name or spell_info.get("icon")

    logger.info("[load spell icons] done")


def create_app(config_obj=None):
    """Create and return a new FlaskApp-Instance.

    Args:
        config_obj(obj, optional): Object used to load config values.
            default will call `config.get_config()`

    Returns:
        <Flask>: the new flask-app instance

    """
    # create APP
    app = flask.Flask(__name__)

    config_name = os.getenv("LORGS_CONFIG_NAME")
    app.config.from_object(config_name)

    # configure jina
    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True
    app.jinja_env.filters["format_time"] = utils.format_time
    app.jinja_env.filters["format_big_number"] = utils.format_big_number

    cache.init_app(app)
    load_spell_icons()

    app.register_blueprint(views.BP, url_prefix="/")
    app.register_blueprint(api.BP, url_prefix="/api")
    return app
