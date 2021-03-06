# Copyright (c) 2015 Hewlett-Packard Development Company, L.P.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import openstack
from openstack.tests.unit import base


class TestOpenStackCloudOperatorNoAuth(base.RequestsMockTestCase):
    def setUp(self):
        """Setup Noauth OperatorCloud tests

        Setup the test to utilize no authentication and an endpoint
        URL in the auth data.  This is permits testing of the basic
        mechanism that enables Ironic noauth mode to be utilized with
        Shade.

        Uses base.RequestsMockTestCase instead of IronicTestCase because
        we need to do completely different things with discovery.
        """
        super(TestOpenStackCloudOperatorNoAuth, self).setUp()
        # By clearing the URI registry, we remove all calls to a keystone
        # catalog or getting a token
        self._uri_registry.clear()
        self.register_uris([
            dict(method='GET',
                 uri=self.get_mock_url(
                     service_type='baremetal', base_url_append='v1',
                     resource='nodes'),
                 json={'nodes': []}),
        ])

    def test_ironic_noauth_none_auth_type(self):
        """Test noauth selection for Ironic in OperatorCloud

        The new way of doing this is with the keystoneauth none plugin.
        """
        # NOTE(TheJulia): When we are using the python-ironicclient
        # library, the library will automatically prepend the URI path
        # with 'v1'. As such, since we are overriding the endpoint,
        # we must explicitly do the same as we move away from the
        # client library.
        self.cloud_noauth = openstack.operator_cloud(
            auth_type='none',
            baremetal_endpoint_override="https://bare-metal.example.com/v1")

        self.cloud_noauth.list_machines()

        self.assert_calls()

    def test_ironic_noauth_admin_token_auth_type(self):
        """Test noauth selection for Ironic in OperatorCloud

        The old way of doing this was to abuse admin_token.
        """
        self.cloud_noauth = openstack.operator_cloud(
            auth_type='admin_token',
            auth=dict(
                endpoint='https://bare-metal.example.com/v1',
                token='ignored'))

        self.cloud_noauth.list_machines()

        self.assert_calls()
