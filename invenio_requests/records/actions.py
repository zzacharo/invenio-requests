# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 TU Wien.
#
# Invenio-Requests is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.


class RequestAction:
    def __init__(self, request):
        self.request = request

    def available_for(self, who):
        return True

    def execute(self, executor):
        # probably want to do something with self.request.subject
        if not self.available_for(executor):
            raise Exception()
