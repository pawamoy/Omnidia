from pathlib import Path

from watchdog.events import FileSystemEventHandler
from watchdog.observers.polling import PollingObserver as Observer

from omnidia.db import Neo4jHTTP
from omnidia.exclusion import excluded


class Handler(FileSystemEventHandler):
    def __init__(self, db) -> None:
        super().__init__()
        self.db = db

    def on_moved(self, event):
        if not event.is_directory:
            old_path = Path(event.src_path).resolve()
            new_path = Path(event.dest_path).resolve()
            if excluded(str(new_path)):
                self.on_deleted(event)
            else:
                self.db.exec(f"MERGE (n:File {{path: \"{old_path}\"}}) SET n = {{path: \"{new_path}\"}}")
                if old_path.parent != new_path.parent:  # changed directory
                    self.db.exec(
                        f"""
                        MATCH (f:File {{path: \"{new_path}\"}}),
                            (d_old:Directory {{path: \"{str(old_path.parent)}\"}}),
                            (d_new:Directory {{path: \"{str(new_path.parent)}\"}}),
                            (f) -[r_old:In]-> (d_old)
                        DELETE r_old
                        CREATE (f) -[:In]-> (d_new)
                        """
                    )

    def on_created(self, event):
        label = "Directory" if event.is_directory else "File"
        file_path = Path(event.src_path).resolve()
        parent_path = str(file_path.parent)
        file_path = str(file_path)
        if not excluded(file_path):
            self.db.exec(
                f"""
                MATCH (d:Directory {{path: \"{parent_path}\"}})
                CREATE (d) <-[:In]- (:{label} {{path: \"{file_path}\"}})
                """
            )

    def on_deleted(self, event):
        label = "Directory" if event.is_directory else "File"
        path = str(Path(event.src_path).resolve())
        self.db.exec(f"MATCH (n:{label} {{path: \"{path}\"}}) DETACH DELETE n")


def watch(path):
    neo4j = Neo4jHTTP("http://localhost:7474", "neo4j", "s3cr3t")
    handler = Handler(db=neo4j)
    observer = Observer()
    observer.schedule(handler, path=path, recursive=True)
    observer.start()
    try:
        while True:
            observer.join(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
