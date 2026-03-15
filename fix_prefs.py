import os
import django
from django.template import Context, Template
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ansari_aluminium.settings')
django.setup()

from dynamic_preferences.registries import global_preferences_registry
from dynamic_preferences.models import GlobalPreferenceModel

print("--- Checking Database Entries ---")
prefs = GlobalPreferenceModel.objects.filter(section='stats')
for p in prefs:
    print(f"Deleting DB override: {p.section}__{p.name} = {p.raw_value}")
    p.delete()

print("\n--- Verifying New Defaults ---")
manager = global_preferences_registry.manager()
print(f"Stats Experience (Code Default): {manager['stats__experience']}")
print(f"Stats Projects (Code Default): {manager['stats__projects']}")

print("\n--- Testing Template Rendering ---")
# Simulating the context processor
from dynamic_preferences.processors import global_preferences
request = None # Context processors usually take a request, but this one might not Strict dependency
# actually, allow me to just manually construct the context dictionary that the processor would return
ctx_dict = global_preferences(request)

t = Template("Experience: {{ global_preferences.stats__experience }}")
c = Context(ctx_dict)
print(f"Rendered: {t.render(c)}")
