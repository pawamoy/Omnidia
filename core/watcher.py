import os

from watchdog.events import FileSystemEventHandler
from graph.models import File


class OmnidiaEventHandler(FileSystemEventHandler):
    """Override the FileSystemEventHandler class from watchdog.
    The only event handler we override is the on_modified handler, used to
    recompute the hash of the file when it has been modified.
    """

    def on_deleted(self, event):
        print('watchdog: deleted')
        if event.is_directory:
            for file in File.in_path(event.src_path):
                print('  %s' % file.path)
                if os.path.exists(file.path):
                    print('  not deleted (still exists)')
                else:
                    file.delete(from_disk=False)
                    print('  deleted')
        else:
            print('  %s' % event.src_path)
            file = File.get(path=event.src_path)
            if file:
                if os.path.exists(file.path):
                    print('  not deleted (file exists, assumed rewriting)')
                else:
                    file.delete(from_disk=False)
                    print('  deleted')
            else:
                print('  not deleted (node does not exist in db)')

    def on_modified(self, event):
        """Event handler for modified files.

        :param event: the event object representing the file system event
        :type event: :class:`FileSystemEvent`
        """
        if event.is_directory:
            return
        print('watchdog: modified')
        modified_file = File.get(path=event.src_path)
        if modified_file:
            print('  %s' % modified_file.path)
            # Case 1: file has been modified
            old_hash = modified_file.file_hash
            new_hash = modified_file.get_file_hash()
            if old_hash != new_hash:
                modified_file.file_hash = new_hash
                modified_file.save()
                print('  new hash computed')
            else:
                print('  same hash')
        else:
            # Case 2: file has been added
            print('  %s' % event.src_path)
            if os.path.exists(event.src_path):
                File.add(event.src_path)
                print('  created')
            else:
                print('  not created (not existing anymore, assumed temp file)')

    def on_moved(self, event):
        if not event.is_directory:
            print('watchdog: moved')
            print('  %s -> %s' % (event.src_path, event.dest_path))
            file = File.get(path=event.src_path)
            if file:
                file.path = event.dest_path
                file.apply_node_name_from_filename()
                file.save()
                print('  renamed')
            else:
                File.add(event.dest_path)
                print('  created')
