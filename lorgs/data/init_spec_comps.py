PALADIN_HOLY          = specs.WowSpec.query.get(65)
PRIEST_DISCIPLINE     = specs.WowSpec.query.get(256)
PRIEST_HOLY           = specs.WowSpec.query.get(257)
SHAMAN_RESTORATION    = specs.WowSpec.query.get(264)
DRUID_RESTORATION     = specs.WowSpec.query.get(105)
MONK_MISTWEAVER       = specs.WowSpec.query.get(269)


comp = warcraftlogs_comps.SpecCombination()
comp.specs = [PALADIN_HOLY, PRIEST_DISCIPLINE, SHAMAN_RESTORATION, DRUID_RESTORATION]

db.Base.metadata.create_all(db.engine)
db.session.add(comp)
db.session.commit()