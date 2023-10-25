import os
from pathlib import Path

from omnidia.db import Neo4jHTTP
from omnidia.exclusion import excluded


def create_file(db, path):
    path = str(path.resolve())
    if not excluded(path):
        db.exec(f"MERGE (n:File {{path: \"{path}\"}})")


def create_directory(db, path):
    path = str(path.resolve())
    if not excluded(path):
        db.exec(f"MERGE (n:Directory {{path: \"{path}\"}})")


def create_files(db, parent, files):
    parent_path = str(parent.resolve())
    for file_name in files:
        file_path = str((parent / file_name).resolve())
        if not excluded(file_path):
            db.exec(
                f"""
                MATCH (d:Directory {{path: \"{parent_path}\"}})
                MERGE (d) <-[:In]- (f:File {{path: \"{file_path}\"}})
                """
            )


def create_directories(db, parent, dirs):
    parent_path = str(parent.resolve())
    for dir_name in dirs:
        dir_path = str((parent / dir_name).resolve())
        if not excluded(dir_path):
            db.exec(
                f"""
                MATCH (d1:Directory {{path: \"{parent_path}\"}})
                MERGE (d1) <-[:In]- (d2:Directory {{path: \"{dir_path}\"}})
                """
            )


def scan(path):
    neo4j = Neo4jHTTP("http://localhost:7474", "neo4j", "s3cr3t")
    for root, dirs, files in os.walk(path):
        root = Path(root)
        create_directory(neo4j, root)
        create_directories(neo4j, root, dirs)
        create_files(neo4j, root, files)
