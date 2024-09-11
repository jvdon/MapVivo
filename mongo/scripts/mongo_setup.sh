#!/bin/bash
sleep 15

mongosh --host mongo1:27017 <<EOF
  var cfg = {
    "_id": "rs0",
    "version": 1,
    "members": [
      {
        "_id": 0,
        "host": "mongo1:27017",
        "priority": 2
      },
      {
        "_id": 1,
        "host": "mongo2:27017",
        "priority": 0
      },
      {
        "_id": 2,
        "host": "mongo3:27017",
        "priority": 0
      }
    ]
  };
  rs.initiate(cfg);

  // Wait for the replica set to become primary
  while (rs.status().members[0].stateStr !== 'PRIMARY') {
    print('Waiting for replica set to become primary...');
    sleep(500);
  }

  // Create the database and collections
  const db = db.getSiblingDB("MapVIVO");
  db.createCollection("cache");
  db.createCollection("updatable");

  print('Database and collections created successfully.');

EOF