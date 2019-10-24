# -*- coding: utf-8 -*-
# MinIO Python Library for Amazon S3 Compatible Cloud Storage, (C)
# 2015, 2016, 2017, 2018, 2019 MinIO, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from .credentials import Provider, Value

class Chain(Provider):
    def __init__(self, providers):
        super(Provider, self).__init__()
        self._providers = providers
        self._current = None

    def retrieve(self):
        for provider in self._providers:
            #TODO: Go code collects provider's errors 
            #      should python collect execptions?
            creds = provider.retrieve()
            self._current = provider
            return creds
        self._current = None
        #TODO: Go code returns erros when no provider is found
        #      should python raise error?
        return Value()

    def is_expired(self):
        if self._current == None:
            return True
        return self._current.is_expired()
