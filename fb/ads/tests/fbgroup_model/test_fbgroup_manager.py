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
        self.assertEqual(qs.count(), 1)
        self.assertTrue(self.full in qs)


class FbGroupDownloadManagerTest(TestCase):
    def setUp(self):
        self._create_mail_services()
        self._create_groups()

        self.not_loaded_group = FbGroup.objects.get(group_id='not_loaded_group')
        self.loaded_no_mail = FbGroup.objects.get(group_id='loaded_no_mail', )
        self.loaded_no_title = FbGroup.objects.get(group_id='loaded_no_title', )
        self.full_not_detect_mail = FbGroup.objects.get(group_id='full_not_detect_mail', )
        self.full_google = FbGroup.objects.get(group_id='full_google', )
        self.full_outlook = FbGroup.objects.get(group_id='full_outlook', )
        self.full_yandex = FbGroup.objects.get(group_id='full_yandex', )
        self.full_mailru = FbGroup.objects.get(group_id='full_mailru', )

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
        FbGroup.objects.create(group_id='loaded_no_mail', name='123', status=FbGroup.COLLECTED,
                               is_main_service_mark=True)
        FbGroup.objects.create(group_id='loaded_no_title', email='123@123.com', status=FbGroup.COLLECTED,
                               is_main_service_mark=True)
        FbGroup.objects.create(group_id='full_not_detect_mail', name='xxx', email='123@123.com',
                               status=FbGroup.COLLECTED,
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
        self.assertEqual(groups_count, 8, msg='Количество групп не совпадает')

        FbGroup.mark_ignored_domain_zones()

    def test_google(self):
        self.assertEqual(self.full_google.is_ignored_domain_zone, False)

    def test_is_ignored_mail_zones_marked(self):
        self.assertFalse(self.full_google.is_ignored_domain_zone)
        not_marked = FbGroup.objects.filter(is_ignored_domain_zone__isnull=True)
        self.assertEqual(not_marked.count(), 3)
        for group in (self.not_loaded_group, self.loaded_no_mail, self.loaded_no_title):
            self.assertTrue(not_marked.contains(group))

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


class FbGroupUsedTest(TestCase):
    """
    Тест менеджера на отдачу новых, заюзаных
    отдачу копров и не некорпов
    """

    def setUp(self):
        self._create_mail_service()
        self._create_groups()

    def _create_mail_service(self):
        self.mail_service = MailService.objects.create(name='xxx', pattern='xxx')
        self.assertEqual(MailService.objects.count(), 1)

    def _create_groups(self):
        self.not_collected = FbGroup.objects.create(group_id='not_collected')
        self.collected_no_email = FbGroup.objects.create(
            group_id='collected_no_email',
            status=FbGroup.COLLECTED,
            name='some name',
            email='',
        )
        self.collected_no_email_bug_flags = FbGroup.objects.create(
            group_id='collected_no_email_bug_flags',
            status=FbGroup.COLLECTED,
            name='some name',
            email='',
            is_main_service_mark=True,
            email_service=None,
            is_ignored_domain_zone=False,
        )
        # collected with full data

        # new
        self.new_not_corp = FbGroup.objects.create(
            group_id='new_not_corp',
            status=FbGroup.COLLECTED,
            name='some name',
            email='some@some.com',
            is_main_service_mark=True,
            email_service=self.mail_service,
            is_ignored_domain_zone=False,
            used_count=0,
        )
        self.new_corp = FbGroup.objects.create(
            group_id='new_corp',
            status=FbGroup.COLLECTED,
            name='some name',
            email='some@some.com',
            is_main_service_mark=True,
            email_service=None,
            is_ignored_domain_zone=False,
            used_count=0,
        )
        # not new
        self.used_not_corp = FbGroup.objects.create(
            group_id='used_not_corp',
            status=FbGroup.COLLECTED,
            name='some name',
            email='some@some.com',
            is_main_service_mark=True,
            email_service=self.mail_service,
            is_ignored_domain_zone=False,
            used_count=1,
        )
        self.used_corp = FbGroup.objects.create(
            group_id='used_corp',
            status=FbGroup.COLLECTED,
            name='some name',
            email='some@some.com',
            is_main_service_mark=True,
            email_service=None,
            is_ignored_domain_zone=False,
            used_count=1,
        )

        self.assertEqual(FbGroup.objects.count(), 7, msg='Число созданых групп неправильно')

    def test_correct_download_manager(self):
        qs = FbGroup.download_objects.all()

        self.assertFalse(qs.contains(self.not_collected), msg='Не обработаная группа не должна попадать в вугрузку')
        self.assertFalse(qs.contains(self.collected_no_email),
                         msg='Группы с неполными данными не должна попадать в вугрузку')
        self.assertFalse(qs.contains(self.collected_no_email_bug_flags),
                         msg='Группы без мыло но спроставлеными флагами быть не должно'
                             ' (фильт менеджера full_objects не сработал)')

    def test_download_all(self):
        qs = FbGroup.download_objects.all()
        self.assertEqual(qs.count(), 4)

    def test_new_groups(self):
        qs = FbGroup.download_objects.new()
        self.assertEqual(qs.count(), 2)
        self.assertTrue(self.new_not_corp in qs)
        self.assertTrue(self.new_corp in qs)

    def test_used_raise_error_negative_value(self):
        with self.assertRaises(ValueError):
            qs = FbGroup.download_objects.used(-1)

    def test_used_raise_error_zero_value(self):
        with self.assertRaises(ValueError):
            qs = FbGroup.download_objects.used(0)

    def test_used_groups(self):
        qs = FbGroup.download_objects.used(1)
        self.assertEqual(qs.count(),2)
        self.assertTrue(qs.contains(self.used_not_corp))
        self.assertTrue(qs.contains(self.used_corp))

    def test_used_groups_empty_qs(self):
        qs = FbGroup.download_objects.used(2)
        self.assertEqual(qs.count(),0)

    def test_corp_mails(self):
        qs = FbGroup.download_objects.corp_mails()
        self.assertEqual(qs.count(), 2)
        self.assertTrue(qs.contains(self.new_corp), msg='Новый корп должен быть в выборке')
        self.assertTrue(qs.contains(self.used_corp), msg='Юзаный корп должен быть в выборке')

    def test_not_corps_mails(self):
        qs = FbGroup.download_objects.not_corp_mails()
        self.assertEqual(qs.count(),2)
        self.assertTrue(qs.contains(self.new_not_corp))
        self.assertTrue(qs.contains(self.used_not_corp))

    def test_chain_new_corp(self):
        qs = FbGroup.download_objects.new().corp_mails()
        self.assertEqual(qs.count(), 1)
        self.assertTrue(qs.contains(self.new_corp))

    def test_chain_new_not_corp(self):
        qs = FbGroup.download_objects.new().not_corp_mails()
        self.assertEqual(qs.count(), 1)
        self.assertTrue(qs.contains(self.new_not_corp))

    def test_chain_used_corp(self):
        qs = FbGroup.download_objects.used(1).corp_mails()
        self.assertEqual(qs.count(), 1)
        self.assertTrue(qs.contains(self.used_corp))

    def test_chain_used_not_corp(self):
        qs = FbGroup.download_objects.used(1).not_corp_mails()
        self.assertEqual(qs.count(), 1)
        self.assertTrue(qs.contains(self.used_not_corp))
