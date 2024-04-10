from django.test import TestCase
from ads.models import FbGroup, IgnoredDomainZone

class IgnoredDomainZoneNoZonesTest(TestCase):
    def setUp(self):
        self.zones = ['ru', 'by', 'ua', 'com', 'de', 'pl', 'fr']
        self._create_groups()
        self.ru = FbGroup.objects.get(pk='ru')
        self.by = FbGroup.objects.get(pk='by')
        self.ua = FbGroup.objects.get(pk='ua')
        self.com = FbGroup.objects.get(pk='com')
        self.de = FbGroup.objects.get(pk='de')
        self.pl = FbGroup.objects.get(pk='pl')
        self.fr = FbGroup.objects.get(pk='fr')
        self.not_collected = FbGroup.objects.get(pk='xxx')
        self.ignored = (self.ru, self.by, self.ua)
        self.not_ignored = (
            self.com,
            self.de,
            self.pl,
            self.fr,
        )

        self.assertEqual(
            IgnoredDomainZone.objects.count(),0
        )

    def _create_groups(self):
        groups = []

        for zone in self.zones:
            email = 'xxx@xxx.' + zone
            group = FbGroup(group_id=zone, email=email, name='xxx',status=FbGroup.COLLECTED)
            groups.append(group)
        FbGroup.objects.create(group_id='xxx', )
        FbGroup.objects.bulk_create(groups)
        self.assertEquals(FbGroup.objects.count(), len(self.zones) + 1)
        self.assertEqual(FbGroup.objects.filter(is_ignored_domain_zone__isnull=True).count(), len(self.zones) + 1)
        self.assertEqual(FbGroup.full_objects.filter(is_ignored_domain_zone__isnull=True).count(), len(self.zones))

    def test_no_groups_marked(self):
        FbGroup.mark_ignored_domain_zones()
        qs = FbGroup.objects.filter(is_ignored_domain_zone__isnull=True)
        self.assertEqual(qs.count(),1)
        qs = FbGroup.objects.filter(is_ignored_domain_zone=True)
        self.assertEqual(qs.count(), 0)
        not_ignored = FbGroup.objects.filter(is_ignored_domain_zone=False)
        self.assertEqual(not_ignored.count(), 7)
        for group in self.ignored:
            self.assertTrue(group in not_ignored)
        for group in self.not_ignored:
            self.assertTrue(group in not_ignored)


class IgnoredDomainZoneTest(TestCase):

    def setUp(self):
        self.zones = ['ru', 'by', 'ua', 'com', 'de', 'pl', 'fr']
        self._create_ignored_zones()
        self._create_groups()
        self.ru = FbGroup.objects.get(pk='ru')
        self.by = FbGroup.objects.get(pk='by')
        self.ua = FbGroup.objects.get(pk='ua')
        self.com = FbGroup.objects.get(pk='com')
        self.de = FbGroup.objects.get(pk='de')
        self.pl = FbGroup.objects.get(pk='pl')
        self.fr = FbGroup.objects.get(pk='fr')
        self.not_collected = FbGroup.objects.get(pk='xxx')

        self.ignored = (self.ru, self.by, self.ua)
        self.not_ignored = (
            self.com,
            self.de,
            self.pl,
            self.fr,
        )

    def _create_ignored_zones(self):
        zones = ['ru', 'by', 'ua']
        objecst = []
        for zone_name in zones:
            zone = IgnoredDomainZone(name=zone_name)
            objecst.append(zone)
        IgnoredDomainZone.objects.bulk_create(objecst)

        self.assertEquals(IgnoredDomainZone.objects.count(),len(zones))

    def _create_groups(self):
        groups = []

        for zone in self.zones:
            email = 'xxx@xxx.' + zone
            group = FbGroup(group_id=zone, email=email, name='xxx',status=FbGroup.COLLECTED)
            groups.append(group)
        FbGroup.objects.create(group_id='xxx', )
        FbGroup.objects.bulk_create(groups)
        self.assertEquals(FbGroup.objects.count(), len(self.zones) + 1)
        self.assertEqual(FbGroup.objects.filter(is_ignored_domain_zone__isnull=True).count(), len(self.zones) + 1)
        self.assertEqual(FbGroup.full_objects.filter(is_ignored_domain_zone__isnull=True).count(), len(self.zones))

    def test_not_collected_not_marked(self):
        FbGroup.mark_ignored_domain_zones()
        not_collected_group = FbGroup.objects.get(group_id='xxx')
        self.assertIsNone(not_collected_group.is_ignored_domain_zone)

    def test_collected_groups_marked(self):
        FbGroup.mark_ignored_domain_zones()
        marked_groups = FbGroup.objects.filter(is_ignored_domain_zone__isnull=False)
        self.assertEquals(marked_groups.count(), len(self.zones))

    def test_marked_groups_count(self):
        FbGroup.mark_ignored_domain_zones()
        not_ignored = FbGroup.objects.filter(is_ignored_domain_zone=False)
        self.assertEquals(not_ignored.count(), 4)
        not_ignored = FbGroup.objects.filter(is_ignored_domain_zone=True)
        self.assertEquals(not_ignored.count(), 3)


class IgnoredDomainZoneDownloadManagerTest(IgnoredDomainZoneTest):

    def test_not_collected_not_in_download(self):
        FbGroup.mark_ignored_domain_zones()
        FbGroup.mark_mail_services()
        download_groups = FbGroup.download_objects.all()
        self.assertTrue(self.not_collected not in  download_groups)

    def test_not_ignored_zones_in_download(self):
        FbGroup.mark_ignored_domain_zones()
        FbGroup.mark_mail_services()
        download_groups = FbGroup.download_objects.all()
        self.assertEquals(download_groups.count(), 4)
        for group in self.not_ignored:
            self.assertTrue(group in download_groups)


    def test_ignored_groups_not_in_download(self):
        FbGroup.mark_ignored_domain_zones()
        FbGroup.mark_mail_services()
        download_groups = FbGroup.download_objects.all()
        self.assertEquals(download_groups.count(), 4)
        for group in self.ignored:
            self.assertTrue(group not in download_groups)


