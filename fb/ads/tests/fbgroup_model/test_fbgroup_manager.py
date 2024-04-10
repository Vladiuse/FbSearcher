from django.test import TestCase
from ads.models import FbGroup, MailService


class FbGroupFullObjectsManagerTest(TestCase):

    def setUp(self):
        self.not_loaded_group = FbGroup.objects.create(group_id='1111')
        self.loaded_no_mail = FbGroup.objects.create(group_id='2222', name='123', status=FbGroup.COLLECTED)
        self.loaded_no_title = FbGroup.objects.create(group_id='3333', email='123@123.com', status=FbGroup.COLLECTED)
        self.full = FbGroup.objects.create(group_id='4444', name='xxx', email='123@123.com', status=FbGroup.COLLECTED)
        self._check_groups_created()

    def _check_groups_created(self):
        count = FbGroup.objects.count()
        self.assertEqual(count, 4)

    def test_no_not_loaded_in_qs(self):
        qs = FbGroup.full_objects.all()
        self.assertEqual(qs.count(),1)
        self.assertTrue(self.full in qs)


class FbGroupDownloadManagerTest(TestCase):
    def setUp(self):
        self._create_mail_services()
        self._create_groups()


        self.not_loaded_group = FbGroup.objects.get(group_id='not_loaded_group')
        self.loaded_no_mail = FbGroup.objects.get(group_id='loaded_no_mail',)
        self.loaded_no_title = FbGroup.objects.get(group_id='loaded_no_title',)
        self.full_not_detect_mail = FbGroup.objects.get(group_id='full_not_detect_mail', )
        self.full_google = FbGroup.objects.get(group_id='full_google', )
        self.full_outlook = FbGroup.objects.get(group_id='full_outlook',)
        self.full_yandex = FbGroup.objects.get(group_id='full_yandex',)
        self.full_mailru = FbGroup.objects.get(group_id='full_mailru',)


    def _create_mail_services(self):
        self.google = MailService.objects.create(
            name='google',
            pattern='123',
            ignore=False,
        )
        self.outlook = MailService.objects.create(
            name='outlook',
            pattern='123',
            ignore=False,
        )
        self.yandex = MailService.objects.create(
            name='yandex',
            pattern='123',
            ignore=True,
        )
        self.mailru = MailService.objects.create(
            name='mailru',
            pattern='123',
            ignore=True,
        )
        count = MailService.objects.count()
        self.assertEqual(count, 4)

    def _create_groups(self):
        FbGroup.objects.create(group_id='not_loaded_group')
        FbGroup.objects.create(group_id='loaded_no_mail', name='123', status=FbGroup.COLLECTED, is_main_service_mark=True)
        FbGroup.objects.create(group_id='loaded_no_title', email='123@123.com', status=FbGroup.COLLECTED, is_main_service_mark=True)
        FbGroup.objects.create(group_id='full_not_detect_mail', name='xxx', email='123@123.com', status=FbGroup.COLLECTED,
                                                           email_service=None, is_main_service_mark=False)
        FbGroup.objects.create(group_id='full_google', name='xxx', email='123@123.com',
                                                           status=FbGroup.COLLECTED,
                                                           email_service=self.google, is_main_service_mark=True)
        FbGroup.objects.create(group_id='full_outlook', name='xxx', email='123@123.com',
                                                           status=FbGroup.COLLECTED,
                                                           email_service=self.outlook, is_main_service_mark=True)

        FbGroup.objects.create(group_id='full_yandex', name='xxx', email='123@123.com',
                                                           status=FbGroup.COLLECTED,
                                                           email_service=self.yandex, is_main_service_mark=True)
        FbGroup.objects.create(group_id='full_mailru', name='xxx', email='123@123.com',
                                                           status=FbGroup.COLLECTED,
                                                           email_service=self.mailru, is_main_service_mark=True)

        groups_count = FbGroup.objects.count()
        self.assertEqual(groups_count,8, msg='Количество групп не совпадает')

        FbGroup.mark_ignored_domain_zones()


    def test_google(self):
        self.assertEqual(self.full_google.is_ignored_domain_zone, False)

    def test_join_in_download_manager(self):
        with self.assertNumQueries(1):
            qs = FbGroup.download_objects.all()
            for i in qs:
                pass

    def test_not_loaded_not_in_dowsload_manager(self):
        qs = FbGroup.download_objects.all()
        self.assertTrue(self.not_loaded_group not in qs)
        self.assertTrue(self.loaded_no_mail not in qs, msg='Шруппы без мыла не должно быть в ыюорке на скачку')
        self.assertTrue(self.loaded_no_title not in qs, msg='Шруппы без названия не должно быть в ыюорке на скачку')

    def test_not_marked_mail_not_in_qs(self):
        qs = FbGroup.download_objects.all()
        self.assertTrue(self.full_not_detect_mail not in qs)

    def test_ignored_mails_not_in_qs(self):
        qs = FbGroup.download_objects.all()
        self.assertTrue(self.full_yandex not in qs)
        self.assertTrue(self.full_mailru not in qs)

    def test_correct_work_of_download_manager(self):
        qs = FbGroup.download_objects.all()
        self.assertEqual(self.full_google.is_ignored_domain_zone, False)
        self.assertTrue(self.full_google in qs)
        self.assertTrue(self.full_outlook in qs)
        self.assertEqual(qs.count(), 2)



