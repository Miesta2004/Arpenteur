#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

# Set spatial library paths before Django imports (required for GIS/PostGIS on macOS)
# These allow Django's GIS module to find GEOS and GDAL libraries
homebrew_lib_path = '/opt/homebrew/opt'
if not os.environ.get('GEOS_LIBRARY_PATH'):
    os.environ.setdefault('GEOS_LIBRARY_PATH', f'{homebrew_lib_path}/geos/lib/libgeos_c.dylib')
if not os.environ.get('GDAL_LIBRARY_PATH'):
    os.environ.setdefault('GDAL_LIBRARY_PATH', f'{homebrew_lib_path}/gdal/lib/libgdal.dylib')
# Add Homebrew lib directory to dynamic linker search path (macOS)
if not os.environ.get('DYLD_LIBRARY_PATH'):
    os.environ['DYLD_LIBRARY_PATH'] = f'{homebrew_lib_path}/geos/lib:{homebrew_lib_path}/gdal/lib'
else:
    dyld_path = os.environ['DYLD_LIBRARY_PATH']
    if f'{homebrew_lib_path}/geos/lib' not in dyld_path:
        os.environ['DYLD_LIBRARY_PATH'] = f'{homebrew_lib_path}/geos/lib:{dyld_path}'
    if f'{homebrew_lib_path}/gdal/lib' not in dyld_path:
        os.environ['DYLD_LIBRARY_PATH'] = f'{homebrew_lib_path}/gdal/lib:{os.environ["DYLD_LIBRARY_PATH"]}'


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
