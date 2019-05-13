import os
from django.core.management import BaseCommand
import ujson as json
from django.apps import apps
from django.conf import settings
from django.contrib.auth.models import Permission
from core.models import QuoteItemType

BASE_PATH = os.path.join(settings.BASE_DIR, 'core/fixtures')


def load_data(filenames):
    assert isinstance(filenames, list)
    for filename in filenames:
        print(filename)
        assert os.path.isfile(filename)

        with open(filename) as f:
            fyl = json.load(f)
            for record in fyl:
                app, model_name = record['model'].split('.', 1)  # split only once
                model_cls = apps.get_model(app_label=app, model_name=model_name)
                try:
                    model_cls.objects.get(pk=record['pk'])
                except model_cls.DoesNotExist:
                    try:
                        if model_name == 'group':
                            grp = model_cls.objects.create(name=record['fields']['name'])
                            grp.permissions.add(Permission.objects.get(pk=perm) for perm in record['fields']['permissions'])
                        elif model_name == 'quoteitemdefault':
                            qouteItemType = QuoteItemType.objects.get(pk=record['fields']['quote_item_type'])
                            info = record['fields']
                            info['quote_item_type'] = qouteItemType

                            model_cls.objects.create(**info)
                        else:
                            model_cls.objects.create(**record['fields'])
                    except Exception as e:
                        print e
                        print "Error processing file: {}".format(fyl)


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass
        # Positional arguments
        # parser.add_argument('data_file', nargs='+', type=str)

    def handle(self, *args, **options):
        files = [
            'move_status.json', 'move_type.json', 'groups.json',
            'checklist_item.json', 'move_type_details.json',
            'quote_item_type.json', 'quote_item.json', 'room.json',
            'settings.json', 'source.json', 'vehicle.json',
            'branch.json']
        files = ['quote_item.json']
        load_data([
            os.path.join(BASE_PATH, f) for f in files
        ])
        # for suggestion in options['data_file']:
        #     if os.path.exists(suggestion) and os.path.isfile(suggestion):
        #         process_json_files([suggestion])
        #     else:
        #         process_json_files(sorted(glob.glob(suggestion)))

        self.stdout.write("Done loading")
