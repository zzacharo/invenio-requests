# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 CERN.
#
# Invenio-Requests is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.
"""User moderation requests."""

from invenio_i18n import lazy_gettext as _

from invenio_requests.customizations import RequestType, actions


class BlockUserAction(actions.DeclineAction):
    """Represents a decline action used to block an user."""

    def execute(self, identity, uow):
        """Executes block action."""
        # TODO add specific user block actions
        super().execute(identity, uow)


class ApproveUserAction(actions.AcceptAction):
    """Represents an accept action used to aprove an user."""

    def execute(self, identity, uow):
        """Executes aprove action."""
        # TODO add specific user block actions
        super().execute(identity, uow)


class UserModeration(RequestType):
    """Request to moderate an user."""

    type_id = "user-moderation"
    name = _("User moderation")

    creator_can_be_none = False
    topic_can_be_none = False
    allowed_creator_ref_types = ["user"]
    allowed_receiver_ref_types = ["user"]
    allowed_topic_ref_types = ["user"]

    # TODO missing permissions
    # AdminNeed = RoleNeed("admin")
    # needs_context = {"user.role": AdminNeed, "user.role": AdminNeed}

    available_actions = {
        "delete": actions.DeleteAction,
        "submit": actions.SubmitAction,
        "create": actions.CreateAction,
        "cancel": actions.CancelAction,
        # Custom implemented actions
        "accept": ApproveUserAction,
        "decline": BlockUserAction,
    }
