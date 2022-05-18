# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 CERN.
# Copyright (C) 2021 TU Wien.
#
# Invenio-Requests is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Base class for customizable actions on requests."""

from flask_babelex import gettext as _

from ..errors import NoSuchActionError
from ..proxies import current_events_service
from .event_types import LogEventType


class RequestAction:
    """Base class for actions on requests."""

    status_from = None
    """Required status of a request to run this action."""

    status_to = 'created'
    """Status after execution of the action."""

    event_type = None
    """Defines an event which will be logged if defined."""

    log_event = True
    """Define if the action should be logged through a `LogEventType`."""

    name = None
    """Defines the readable name of the action.

    This marks the name of the action class as translatable.
    """

    def __init__(self, request):
        """Constructor."""
        self.request = request

    def can_execute(self):
        """Check whether the action can be executed.

        This checks if a given state transition for a request is allowed or
        not.

        :return: True if the action can be executed, False otherwise.
        """
        if self.status_from is None:
            return self.request.status is None
        else:
            return self.request.status in self.status_from

    def execute(self, identity, uow):
        """Execute the request action.

        :param identity: The identity of the executor.
        :param data: The passed input to the action.
        """
        self.request.status = self.status_to
        if self.log_event:
            event = LogEventType(
                payload=dict(
                    event=self.status_to
                )
            )
            _data = dict(payload=event.payload)
            current_events_service.create(
                identity, self.request.id, _data, event, uow=uow)


class RequestActions:
    """Namespace for RequestActions static calls."""

    @classmethod
    def get_action(cls, request, action_name):
        """Get the action registered under the given name.

        :param action_name: The registered name of the action.
        :return: The action registered under the given name.
        """
        try:
            return request.type.available_actions[action_name](request)
        except KeyError:
            raise NoSuchActionError(action=action_name)

    @classmethod
    def can_execute(cls, request, action_name):
        """Check whether an action can be executed.

        Perhaps data is sometimes useful for that check, so also included.
        """
        return cls.get_action(request, action_name).can_execute()

    @classmethod
    def execute(cls, identity, request, action_name, uow):
        """Have identity execute on request the action with the data."""
        return cls.get_action(request, action_name).execute(identity, uow)


#
# Specific actions
#
class CreateAction(RequestAction):
    """Create a request."""

    status_from = None
    status_to = 'created'
    log_event = False
    name = _('Create')

class CreateAndSubmitAction(RequestAction):
    """Create and submit a request."""

    status_from = None
    status_to = 'submitted'
    log_event = False
    name = _('Create')


class DeleteAction(RequestAction):
    """Delete a request."""

    status_from = ['created']
    status_to = 'deleted'
    name = _('Delete')


class SubmitAction(RequestAction):
    """Submit a request."""

    status_from = ['created']
    status_to = 'submitted'
    log_event = False
    name = _('Submit')


class AcceptAction(RequestAction):
    """Decline a request."""

    status_from = ['submitted']
    status_to = 'accepted'
    name = _('Accept')


class DeclineAction(RequestAction):
    """Decline a request."""

    status_from = ['submitted']
    status_to = 'declined'
    name = _('Decline')


class CancelAction(RequestAction):
    """Cancel a request."""

    status_from = ['submitted']
    status_to = 'cancelled'
    name = _('Cancel')


class ExpireAction(RequestAction):
    """Expire a request."""

    status_from = ['submitted']
    status_to = 'expired'
    name = _('Expire')
