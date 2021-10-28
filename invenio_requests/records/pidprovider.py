# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 CERN.
# Copyright (C) 2021 TU Wien.
#
# Invenio-Requests is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Persistent identifier provider for requests."""


from invenio_pidstore.models import PIDStatus
from invenio_pidstore.providers.base import BaseProvider


# TODO probably not required, because what would requests need PIDs for?
class RequestIdProvider(BaseProvider):
    """Request identifier provider.

    It uses the value of the 'id' present in our data to generate the
    identifier.
    """

    pid_type = "reqid"
    """Type of persistent identifier."""

    pid_provider = None
    """Provider name."""

    object_type = "req"
    """Type of object."""

    default_status = PIDStatus.REGISTERED
    """Request IDs with an object are by default registered.

    Default: :attr:`invenio_pidstore.models.PIDStatus.REGISTERED`
    """

    # TODO check out what's really required and/or expected here
    @classmethod
    def create(cls, object_uuid=None, record=None):
        """Create a new request identifier.

        Relies on the a request record being

        Note: if the object_type and object_uuid values are passed, then the
        PID status will be automatically setted to
        :attr:`invenio_pidstore.models.PIDStatus.REGISTERED`.

        For more information about parameters,
        see :meth:`invenio_pidstore.providers.base.BaseProvider.create`.

        :param object_uuid: The object identifier. (Default: None).
        :param record: A request record.
        :returns: A :class:`RequestIdProvider` instance.
        """
        assert record is not None, "Missing or invalid 'record'."
        assert "id" in record and isinstance(
            record["id"], str
        ), "Missing 'id' key in record."

        # Retrieve pid value form record.
        pid_value = record["id"]
        object_uuid = object_uuid or record.model.id

        return super().create(
            pid_type=cls.pid_type,
            pid_value=pid_value,
            object_type=cls.object_type,
            object_uuid=object_uuid,
            status=cls.default_status,
        )
