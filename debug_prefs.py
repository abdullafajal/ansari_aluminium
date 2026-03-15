import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ansari_aluminium.settings')
django.setup()

from dynamic_preferences.registries import global_preferences_registry

try:
    global_preferences = global_preferences_registry.manager()
    print("--- Dynamic Preferences Debug ---")
    print(f"Stats Experience: {global_preferences.get('stats__experience', 'NOT FOUND')}")
    print(f"Stats Projects: {global_preferences.get('stats__projects', 'NOT FOUND')}")
    print(f"Stats Warranty: {global_preferences.get('stats__warranty', 'NOT FOUND')}")
    print(f"Stats Delivery: {global_preferences.get('stats__delivery', 'NOT FOUND')}")
    
    print("\n--- All Preferences ---")
    print(global_preferences.all())

except Exception as e:
    print(f"Error: {e}")
