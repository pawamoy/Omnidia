from watchdog.events import FileSystemEventHandler
from omnidia.models import File

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
        modified_file = File.get(event.src_path)
        if not modified_file:
            return
        old_hash = modified_file.hash
        new_hash = modified_file.compute_hash()
        if old_hash != new_hash:
            modified_file.hash = new_hash
            modified_file.save()
