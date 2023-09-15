from ads.models import FbGroup
from ads.serializers import FbGroupSerializer


data = {'raw_url': 'https://facebook.com/123/',
        'ads': {
            'id': '859762788802222',
            'name': 'All Language Translator',
            'time_text': 'Показ начат 23 ноя 2022 г.',
            'status': 'Активно',
        }
        }

serializer = FbGroupSerializer(data=data)
print(serializer.is_valid())
print(serializer.errors)
