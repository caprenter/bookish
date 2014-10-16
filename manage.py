#!/usr/bin/env python
import os
import sys
import environ

if __name__ == "__main__":
    environ.Env.read_env()  # reading .env file

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bookish.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
