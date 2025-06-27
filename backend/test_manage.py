#!/usr/bin/env python
"""Minimal Django management utility for testing."""
import os
import sys

if __name__ == '__main__':
    # Simple test
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_platform.settings_dev')
    try:
        from django.core.management import execute_from_command_line
        print("Django imports working!")
        # Just check version
        execute_from_command_line(['manage.py', '--version'])
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Error: %s" % exc
        ) from exc
