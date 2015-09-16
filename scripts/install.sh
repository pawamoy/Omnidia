#!/usr/bin/env bash

# download neo4j, extract and launch it
sudo apt-get install maven2
# install jdk 7, export java home
git clone https://github.com/tinkerpop/gremlin.git
cd gremlin
mvn clean install
