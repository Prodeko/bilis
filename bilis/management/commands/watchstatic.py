from django.core.management.base import NoArgsCommand, CommandError
from django.core.management import call_command
from django.conf import settings
from pipeline.exceptions import CompilerError
import os
import sys
import sched, time


class Command(NoArgsCommand):
    help = 'Watches the static folder for changes, and runs the collectstatic-command if something is changed'

    def handle_noargs(self, **options):
        
        def get_time(filename):
            stat = os.stat(filename)
            mtime = stat.st_mtime
            #if sys.platform == "win32":
            #    mtime -= stat.st_ctime
            return mtime
        
        def files_and_times(directory):
            files = []
            files_dict = {}
            for (dirpath, dirname, filenames) in os.walk(directory):
                for name in filenames:
                    files.append(dirpath + '/' + name)
            for filename in files:
                files_dict[filename] = get_time(filename)
            return files_dict
        
        def read_all():
            all_files = {}
            for key, sets in settings.WATCH_STATIC_FOLDERS.items():
                folder_dict = files_and_times(sets['folder'])
                all_files[key] = folder_dict
            return all_files
        
        def files_changed(sc, old_files={}):
            # Read new files and their modification times
            new_files = read_all()
            if new_files != old_files:
                print('Files changed!')
                try:
                    call_command('collectstatic', interactive=False)
                    # Delete the useless files created by django-pipeline
                    # See: https://github.com/cyberdelia/django-pipeline/issues/202
                    for key, sets in settings.WATCH_STATIC_FOLDERS.items():
                        for filename in sets['delete']:
                            filepath = sets['folder'] + '/' + filename
                            os.remove(filepath)
                            print('Deleted ' + filepath)
                except CompilerError:
                    print('Failed to compile!')
                    pass
                old_files = read_all()
            else:
                print('Files not changed!')
            sc.enter(settings.WATCH_INTERVAL, 1, files_changed, (sc, old_files))
            
        s = sched.scheduler(time.time, time.sleep)
        s.enter(settings.WATCH_INTERVAL, 1, files_changed, (s,))
        s.run()