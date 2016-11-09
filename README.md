# Omnidia

File (and abstract object) manager using a graph database and a web interface.

## Why is that?

A tree structure is not always efficient to explore and exploit your data.  
For example, where do you put a track called `Foo - Bar (Baz Remix).ogg`?  
In `Foo`'s directory or in `Baz`'s one? Maybe you could add a symbolic link so it's in both?  
What if this track is also part of a movie's original soundtrack?  
And you want it in one or two playlists of your own?  
And use it in a special project?  

In this case it would be easier to have the track somewhere, an abstracted element that knows
its path on the disk, and other elements defining links to it (its abstracted form).

Well, this is a graph. As an abstract layer above your file system.

Omnidia does not aim to provide an alternative file system. Its goal is to offer an interface
to manipulate your files (and other abstract objects) with graphs. Each file / object is a node
that can be connected to other files / objects. You can then search for things, connect them
and discover common attributes between different entities.

## Progression

Omnidia is currently just in alpha version. There are many graph database solutions, many
languages, many drivers and many framework that could be used to achieve this. For now the
chosen technologies are the following:

- [Python](https://www.python.org/) language (v3.5)
- [Neo4j](https://neo4j.com/) graph database
- [Py2neo](http://py2neo.org/v3/) driver for neo4j
- [Django](https://www.djangoproject.com/) framework

The features available are the following:

- [watchdog](https://pypi.python.org/pypi/watchdog) handler to sync database with the content of a
  folder (i.e. copy files here -> nodes are created, delete/move/rename them -> same applied on db)
- basic web pages to manipulate datasets, files, and objects

Note: datasets are simple lists of values (ex: Country, Language, Music genre, ...),
but still stored as graph.

You can also visualize the nodes and edges
with Neo4j's web browser at [localhost:7474](localhost:7474).

## I need help

I used composition to benefit from py2neo's capabilities and add a Django-like behavior.
While it is quite easy to understand and use, it really is not performant. I am aware of
solutions like [neomodel](https://github.com/robinedwards/neomodel)
or [bulbs](https://github.com/espeed/bulbs),
but currently they only support Neo4j 2.x and py2neo 2.x.
Neo4j and py2neo 3.x support would be much appreciated, but I'm open to suggestions.

I also tried to set up a [Tinkerpop](http://tinkerpop.apache.org/)
[Gremlin](http://tinkerpop.apache.org/gremlin.html)
server and console, plus drivers, but failed to.

## Installation (and contribution)

You will first need to install [virtualenv](https://virtualenv.pypa.io/en/stable/)
and [Neo4j](https://neo4j.com/download/community-edition/).
Also start Neo4j.

```bash
git clone https://github.com/Pawamoy/Omnidia omnidia
cd omnidia
./scripts/install.sh
./scripts/run.sh USER PASSWORD
# Go to localhost:8000 to see Omnidia's website
# Go to localhost:7474 to see Neo4j's web browser
```

To load some fixtures:
```bash
./scripts/load_fixtures.sh
```

To empty the database:
```bash
./scripts/empty_database.sh
```
