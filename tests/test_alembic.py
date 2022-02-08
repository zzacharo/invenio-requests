# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016-2021 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Test alembic recipes for Invenio-RDM-Records."""

import pytest
from invenio_db.utils import drop_alembic_version_table


def test_alembic(base_app, database):
    """Test alembic recipes."""
    db = database
    ext = base_app.extensions['invenio-db']

    if db.engine.name == 'sqlite':
        raise pytest.skip('Upgrades are not supported on SQLite.')

    # Check that this package's SQLAlchemy models have been properly registered
    tables = [x.name for x in db.get_tables_for_bind()]
    assert 'request_metadata' in tables
    assert 'request_events' in tables

    # Check that Alembic agrees that there's no further tables to create.
    # NOTE: This is *TEMPORARY* solution because of the SQLAlchemy dicsussion
    # <https://github.com/sqlalchemy/sqlalchemy/discussions/7597> and the issue
    # <https://github.com/sqlalchemy/sqlalchemy/issues/7631>. The issue was
    # introduced in https://github.com/inveniosoftware/invenio-files-rest/pull/276
    assert len(ext.alembic.compare_metadata()) == 1

    # Drop everything and recreate tables all with Alembic
    db.drop_all()
    drop_alembic_version_table()
    ext.alembic.upgrade()

    # NOTE: This is *TEMPORARY* solution because of
    # https://github.com/inveniosoftware/invenio-db/commit/4aa83066a4505c82ed5f758a8b807c56cec3b51b#diff-5fc4bdeec4cb30a0edb0bb7a3ffbc436302362f1ef2a92b0bd98e5578e30f91bR94
    # introduced to solve the SQLAlcehmy issue mentioned above
    assert len(ext.alembic.compare_metadata()) == 43

    # Try to upgrade and downgrade
    ext.alembic.stamp()
    ext.alembic.downgrade(target='96e796392533')
    ext.alembic.upgrade()
    # NOTE: This is *TEMPORARY* solution because of
    # https://github.com/inveniosoftware/invenio-db/commit/4aa83066a4505c82ed5f758a8b807c56cec3b51b#diff-5fc4bdeec4cb30a0edb0bb7a3ffbc436302362f1ef2a92b0bd98e5578e30f91bR94
    # introduced to solve the SQLAlcehmy issue mentioned above
    assert len(ext.alembic.compare_metadata()) == 43

    drop_alembic_version_table()
