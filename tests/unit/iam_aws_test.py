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

import mock
import json
from unittest import TestCase
from minio.credentials.aws_iam import IamEc2MetaData
from nose.tools import eq_

class TestIamEc2MetaData(TestCase):
    @mock.patch('urllib3.PoolManager.urlopen')
    def test_iam(self, mock_connection):
        # get provider
        mock_cred_list = {
            "status" : 200,
            "data" : "test-s3-full-access-for-minio-ec2"
        }
        request_cred_data = json.dumps({
            "Code" : 'Success',
            "Type" : 'AWS-HMAC',
            "AccessKeyId" : 'accessKey',
            "SecretAccessKey" : 'secret',
            "Token" : 'token',
            "Expiration" : '2014-12-16T01:51:37Z',
            "LastUpdated" : '2009-11-23T0:00:00Z'
        })
        mock_request_cred = {
            "status" : 200,
            "data": request_cred_data
        }
        mock_connection.side_effect = [mock_cred_list, mock_request_cred]
        provider = IamEc2MetaData()
        # retrieve credentials
        creds = provider.retrieve()
        eq_(creds.access_key, "accessKey")
        eq_(creds.secret_key, "secret")
        eq_(creds.session_token, "token")
