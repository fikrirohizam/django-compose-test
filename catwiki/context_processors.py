from django.apps import apps
from .models import Home

catwiki_tables = [m._meta.db_table for c in apps.get_app_configs() for m in c.get_models() if "catwiki" in m._meta.db_table]
catwiki_tables_name = [name.replace('catwiki_','') for name in catwiki_tables]

def all_table_name(request):
    return {'all_tables':catwiki_tables_name}