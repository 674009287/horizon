# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
import json

from django.core.urlresolvers import reverse  # noqa
from django import http  # noqa
from mox import IsA  # noqa

from openstack_dashboard import api
from openstack_dashboard.dashboards.admin.metering import tabs
from openstack_dashboard.test import helpers as test

INDEX_URL = reverse("horizon:admin:metering:index")


class MeteringViewTests(test.APITestCase, test.BaseAdminViewTests):
    @test.create_stubs({api.keystone: ('tenant_list',)})
    def test_disk_usage(self):
        statistics = self.statistics.list()

        api.keystone.tenant_list(IsA(http.HttpRequest),
                                 domain=None,
                                 marker='tenant_marker',
                                 paginate=True) \
            .AndReturn([self.tenants.list(), False])

        ceilometerclient = self.stub_ceilometerclient()
        ceilometerclient.statistics = self.mox.CreateMockAnything()
        # check that list is called twice for one resource and 2 meters
        ceilometerclient.statistics.list(meter_name=IsA(str),
                                         period=None, q=IsA(list)).\
            MultipleTimes().\
            AndReturn(statistics)

        self.mox.ReplayAll()

        # getting all resources and with statistics
        res = self.client.get(reverse('horizon:admin:metering:index'))
        self.assertTemplateUsed(res, 'admin/metering/index.html')
        table_stats = res.context['table'].data

        first = table_stats[0]
        self.assertEqual(first.id, 'test_tenant')
        self.assertEqual(first.disk_write_requests, 4.55)
        self.assertEqual(first.disk_read_bytes, 4.55)
        self.assertEqual(first.disk_write_bytes, 4.55)
        self.assertEqual(first.disk_read_bytes, 4.55)

        second = table_stats[1]
        self.assertEqual(second.id, 'disabled_tenant')
        self.assertEqual(second.disk_write_requests, 4.55)
        self.assertEqual(second.disk_read_bytes, 4.55)
        self.assertEqual(second.disk_write_bytes, 4.55)
        self.assertEqual(second.disk_read_bytes, 4.55)

        # check there is as many rows as tenants
        self.assertEqual(len(table_stats),
                         len(self.tenants.list()))
        self.assertIsInstance(first, api.ceilometer.ResourceAggregate)

    @test.create_stubs({api.keystone: ('tenant_list',)})
    def test_global_network_traffic_usage(self):
        statistics = self.statistics.list()

        api.keystone.tenant_list(IsA(http.HttpRequest),
                                 domain=None,
                                 marker='tenant_marker',
                                 paginate=True) \
            .AndReturn([self.tenants.list(), False])

        ceilometerclient = self.stub_ceilometerclient()
        ceilometerclient.statistics = self.mox.CreateMockAnything()
        # check that list is called twice for one resource and 2 meters
        ceilometerclient.statistics.list(meter_name=IsA(str),
                                         period=None, q=IsA(list)).\
            MultipleTimes().\
            AndReturn(statistics)

        self.mox.ReplayAll()

        # getting all resources and with statistics
        res = self.client.get(reverse('horizon:admin:metering:index') +
            "?tab=ceilometer_overview__global_network_traffic_usage")
        self.assertTemplateUsed(res, 'admin/metering/index.html')
        table_stats = res.context['table'].data

        first = table_stats[0]
        self.assertEqual(first.id, 'test_tenant')
        self.assertEqual(first.network_incoming_bytes, 4.55)
        self.assertEqual(first.network_incoming_packets, 4.55)
        self.assertEqual(first.network_outgoing_bytes, 4.55)
        self.assertEqual(first.network_outgoing_packets, 4.55)

        second = table_stats[1]
        self.assertEqual(second.id, 'disabled_tenant')
        self.assertEqual(second.network_incoming_bytes, 4.55)
        self.assertEqual(second.network_incoming_packets, 4.55)
        self.assertEqual(second.network_outgoing_bytes, 4.55)
        self.assertEqual(second.network_outgoing_packets, 4.55)

        # check there is as many rows as tenants
        self.assertEqual(len(table_stats),
                         len(self.tenants.list()))
        self.assertIsInstance(first, api.ceilometer.ResourceAggregate)

    @test.create_stubs({api.keystone: ('tenant_list',)})
    def test_global_network_usage(self):
        statistics = self.statistics.list()

        api.keystone.tenant_list(IsA(http.HttpRequest),
                                 domain=None,
                                 marker='tenant_marker',
                                 paginate=True) \
            .AndReturn([self.tenants.list(), False])

        ceilometerclient = self.stub_ceilometerclient()
        ceilometerclient.statistics = self.mox.CreateMockAnything()
        # check that list is called twice for one resource and 2 meters
        ceilometerclient.statistics.list(meter_name=IsA(str),
                                         period=None, q=IsA(list)).\
            MultipleTimes().\
            AndReturn(statistics)

        self.mox.ReplayAll()

        # getting all resources and with statistics
        res = self.client.get(reverse('horizon:admin:metering:index') +
            "?tab=ceilometer_overview__global_network_usage")
        self.assertTemplateUsed(res, 'admin/metering/index.html')
        table_stats = res.context['table'].data

        first = table_stats[0]
        self.assertEqual(first.id, 'test_tenant')
        self.assertEqual(first.network, 4.55)
        self.assertEqual(first.network_create, 4.55)
        self.assertEqual(first.subnet, 4.55)
        self.assertEqual(first.subnet_create, 4.55)
        self.assertEqual(first.port, 4.55)
        self.assertEqual(first.port_create, 4.55)
        self.assertEqual(first.router, 4.55)
        self.assertEqual(first.router_create, 4.55)
        self.assertEqual(first.ip_floating, 4.55)
        self.assertEqual(first.ip_floating_create, 4.55)

        second = table_stats[1]
        self.assertEqual(second.id, 'disabled_tenant')
        self.assertEqual(second.network, 4.55)
        self.assertEqual(second.network_create, 4.55)
        self.assertEqual(second.subnet, 4.55)
        self.assertEqual(second.subnet_create, 4.55)
        self.assertEqual(second.port, 4.55)
        self.assertEqual(second.port_create, 4.55)
        self.assertEqual(second.router, 4.55)
        self.assertEqual(second.router_create, 4.55)
        self.assertEqual(second.ip_floating, 4.55)
        self.assertEqual(second.ip_floating_create, 4.55)

        # check there is as many rows as tenants
        self.assertEqual(len(table_stats),
                         len(self.tenants.list()))
        self.assertIsInstance(first, api.ceilometer.ResourceAggregate)

    @test.create_stubs({api.ceilometer.CeilometerUsage: ("get_user",
                                                         "get_tenant")})
    def test_global_object_store_usage(self):
        resources = self.resources.list()
        statistics = self.statistics.list()
        user = self.ceilometer_users.list()[0]
        tenant = self.ceilometer_tenants.list()[0]

        ceilometerclient = self.stub_ceilometerclient()
        ceilometerclient.resources = self.mox.CreateMockAnything()
        ceilometerclient.resources.list(q=None).AndReturn(resources)

        ceilometerclient.statistics = self.mox.CreateMockAnything()
        ceilometerclient.statistics.list(meter_name=IsA(str),
                                         period=None, q=IsA(list)).\
            MultipleTimes().\
            AndReturn(statistics)

        api.ceilometer.CeilometerUsage\
                .get_user(IsA(str)).MultipleTimes().AndReturn(user)
        api.ceilometer.CeilometerUsage\
                .get_tenant(IsA(str)).MultipleTimes().AndReturn(tenant)

        self.mox.ReplayAll()

        # getting all resources and with statistics
        res = self.client.get(reverse('horizon:admin:metering:index') +
            "?tab=ceilometer_overview__global_object_store_usage")
        self.assertTemplateUsed(res, 'admin/metering/index.html')
        table_stats = res.context['table'].data

        first = table_stats[0]
        self.assertEqual(first.id, 'fake_project_id__fake_user_id__'
                                   'fake_resource_id')
        self.assertEqual(first.user.name, 'user')
        self.assertEqual(first.tenant.name, 'test_tenant')
        self.assertEqual(first.resource, 'fake_resource_id')

        self.assertEqual(first.storage_objects, 4.55)
        self.assertEqual(first.storage_objects_size, 4.55)
        self.assertEqual(first.storage_objects_incoming_bytes, 4.55)
        self.assertEqual(first.storage_objects_outgoing_bytes, 4.55)

        # There are only 2 resources regarding object storage in test data
        self.assertEqual(len(table_stats), 2)
        self.assertIsInstance(first, api.ceilometer.GlobalObjectStoreUsage)

    def test_stats_page(self):
        resources = self.resources.list()
        ceilometerclient = self.stub_ceilometerclient()
        ceilometerclient.resources = self.mox.CreateMockAnything()
        # I am returning only 1 resource
        ceilometerclient.resources.list(q=IsA(list)).AndReturn(resources[:1])

        self.mox.ReplayAll()

        # getting all resources and with statistics
        res = self.client.get(reverse('horizon:admin:metering:index') +
            "?tab=ceilometer_overview__stats")
        self.assertTemplateUsed(res, 'admin/metering/index.html')
        self.assertTemplateUsed(res, 'admin/metering/stats.html')

    def _verify_series(self, series, value, date, expected_names):
        expected_names.reverse()
        data = json.loads(series)
        self.assertTrue('series' in data)
        self.assertEqual(len(data['series']), len(expected_names))
        for d in data['series']:
            self.assertTrue('data' in d)
            self.assertEqual(len(d['data']), 1)
            self.assertAlmostEqual(d['data'][0].get('y'), value)
            self.assertEqual(d['data'][0].get('x'), date)
            self.assertEqual(d.get('name'), expected_names.pop())
            self.assertEqual(d.get('unit'), '')

        self.assertEqual(data.get('settings'), {})

    @test.create_stubs({api.keystone: ('tenant_list',)})
    def test_stats_for_line_chart(self):
        statistics = self.statistics.list()

        api.keystone.tenant_list(IsA(http.HttpRequest),
                                 domain=None,
                                 marker='tenant_marker',
                                 paginate=True) \
            .AndReturn([self.tenants.list(), False])

        ceilometerclient = self.stub_ceilometerclient()
        ceilometerclient.statistics = self.mox.CreateMockAnything()
        # check that list is called twice for one resource and 2 meters
        ceilometerclient.statistics.list(meter_name="memory",
                                         period=IsA(int), q=IsA(list)).\
            MultipleTimes().\
            AndReturn(statistics)

        self.mox.ReplayAll()

        # get all statistics of project aggregates
        res = self.client.get(reverse('horizon:admin:metering:samples') +
            "?meter=memory&group_by=project&stats_attr=avg&date_options=7")

        self.assertEqual(res._headers['content-type'],
                         ('Content-Type', 'application/json'))
        expected_names = ['test_tenant',
                          'disabled_tenant',
                          u'\u4e91\u89c4\u5219']
        self._verify_series(res._container[0], 4.55, '2012-12-21T11:00:55',
                            expected_names)

    @test.create_stubs({api.keystone: ('tenant_list',)})
    def test_stats_for_line_chart_attr_max(self):
        statistics = self.statistics.list()

        api.keystone.tenant_list(IsA(http.HttpRequest),
                                 domain=None,
                                 marker='tenant_marker',
                                 paginate=True) \
            .AndReturn([self.tenants.list(), False])

        ceilometerclient = self.stub_ceilometerclient()
        ceilometerclient.statistics = self.mox.CreateMockAnything()
        # check that list is called twice for one resource and 2 meters
        ceilometerclient.statistics.list(meter_name="memory",
                                         period=IsA(int), q=IsA(list)).\
            MultipleTimes().\
            AndReturn(statistics)

        self.mox.ReplayAll()

        # get all statistics of project aggregates
        res = self.client.get(reverse('horizon:admin:metering:samples') +
            "?meter=memory&group_by=project&stats_attr=max&date_options=7")

        self.assertEqual(res._headers['content-type'],
                         ('Content-Type', 'application/json'))
        expected_names = ['test_tenant',
                          'disabled_tenant',
                          u'\u4e91\u89c4\u5219']
        self._verify_series(res._container[0], 9.0, '2012-12-21T11:00:55',
                            expected_names)

    def test_stats_for_line_chart_no_group_by(self):
        resources = self.resources.list()
        statistics = self.statistics.list()

        ceilometerclient = self.stub_ceilometerclient()
        ceilometerclient.resources = self.mox.CreateMockAnything()
        ceilometerclient.resources.list(q=[]).AndReturn(resources)

        ceilometerclient.statistics = self.mox.CreateMockAnything()
        ceilometerclient.statistics.list(meter_name="storage.objects",
                                         period=IsA(int), q=IsA(list)).\
            MultipleTimes().\
            AndReturn(statistics)

        self.mox.ReplayAll()

        # getting all resources and with statistics, I have only
        # 'storage.objects' defined in test data
        res = self.client.get(reverse('horizon:admin:metering:samples') +
            "?meter=storage.objects&stats_attr=avg&date_options=7")

        self.assertEqual(res._headers['content-type'],
                         ('Content-Type', 'application/json'))
        expected_names = ['fake_resource_id',
                          'fake_resource_id2']
        self._verify_series(res._container[0], 4.55, '2012-12-21T11:00:55',
                            expected_names)


class MeteringStatsTabTests(test.APITestCase):

    @test.create_stubs({api.nova: ('flavor_list',),
                        })
    def test_stats_hover_hints(self):

        class Struct(object):
            def __init__(self, d):
                self.__dict__.update(d)

        def _get_link(meter):
            link = ('http://localhost:8777/v2/meters/%s?'
                    'q.field=resource_id&q.value=fake_resource_id')
            return dict(href=link % meter, rel=meter)

        resources = [
            Struct(dict(resource_id='fake_resource_id',
                        project_id='fake_project_id',
                        user_id='fake_user_id',
                        timestamp='2013-10-22T12:42:37',
                        metadata=dict(ramdisk_id='fake_image_id'),
                        links=[_get_link('instance:m1.massive'),
                               _get_link('instance'),
                               _get_link('cpu')])),
        ]
        request = self.mox.CreateMock(http.HttpRequest)
        api.nova.flavor_list(request, None).AndReturn(self.flavors.list())

        ceilometerclient = self.stub_ceilometerclient()
        ceilometerclient.resources = self.mox.CreateMockAnything()
        ceilometerclient.resources.list(q=IsA(list)).AndReturn(resources)

        self.mox.ReplayAll()

        tab = tabs.GlobalStatsTab(None)
        context_data = tab.get_context_data(request)

        self.assertTrue('meters' in context_data)
        meter_hints = {}
        for d in context_data['meters']:
            meter_hints[d.name] = d.title

        for meter in ['instance:m1.massive', 'instance', 'cpu']:
            self.assertTrue(meter in meter_hints)
            self.assertNotEqual(meter_hints[meter], '')
