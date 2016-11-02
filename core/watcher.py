import hashlib
from watchdog.events import FileSystemEventHandler
from graph.models import File


class OmnidiaEventHandler(FileSystemEventHandler):
    """Override the FileSystemEventHandler class from watchdog.
    The only event handler we override is the on_modified handler, used to
    recompute the hash of the file when it has been modified.
    """

    def on_modified(self, event):
        """Event handler for modified files.

        :param event: the event object representing the file system event
        :type event: :class:`FileSystemEvent`
        """

        if event.is_directory:
            return
        modified_file = File.get(path=event.src_path)
        if modified_file:
            print('watcher: edited file "%s"' % modified_file)
            # Case 1: file has been modified
            old_hash = modified_file.hash
            new_hash = modified_file.compute_hash()
            if old_hash != new_hash:
                modified_file.hash = new_hash
                modified_file.save()
        else:
            with open(event.src_path, 'rb') as f:
                file_hash = File.hash_file(f, hashlib.sha256())
            renamed_file = File.get(hash=file_hash)
            # Case 2: file has been renamed
            if renamed_file:
                print('watcher: renamed file "%s"' % renamed_file)
                renamed_file.set_path(event.src_path)
            # Case 3: file has been added
            else:
                print('watcher: added file "%s"' % event.src_path)
                File.add(event.src_path)

