# Druid Configuration
<br>
### Benchmarking Configuraiton
<hr>

This configuration , we are using to benchmark the druid with approximately 10X more data then the realtime event data (~15 Lacs events per day) we captured from **AppsFlyer** through push api.

 * Core Engine running on **m4.large** machine.
 * Coordination Engine running on **m4.large** machine.
 * Compute Engine running on **r3.large** machine.
 * Dependencies zookeeper, Kafka, Node Js running on **m4.large** machine.
 
The same configuration can be used for **staging environment** with lower machine confiugrations.


<br>
### Directory Structure
<h>

```
./druid-staging/benchmarking
├── bin
├── conf
│   ├── druid
│   │   ├── _common
│   │   ├── broker
│   │   ├── coordinator
│   │   ├── historical
│   │   ├── middleManager
│   │   └── overlord
│   └── tranquility
├── conf-quickstart
│   ├── druid
│   │   ├── _common
│   │   ├── broker
│   │   ├── coordinator
│   │   ├── historical
│   │   ├── middleManager
│   │   └── overlord
│   └── tranquility
├── extensions
│   ├── druid-avro-extensions
│   ├── druid-caffeine-cache
│   ├── druid-datasketches
│   ├── druid-examples
│   ├── druid-hdfs-storage
│   ├── druid-histogram
│   ├── druid-kafka-eight
│   ├── druid-kafka-extraction-namespace
│   ├── druid-kafka-indexing-service
│   ├── druid-lookups-cached-global
│   ├── druid-lookups-cached-single
│   ├── druid-s3-extensions
│   ├── druid-stats
│   └── postgresql-metadata-storage
├── hadoop-dependencies
│   └── hadoop-client
│       └── 2.3.0
├── lib
└── quickstart
```

###### These are the following directories important for configuring nodes of Druid. You can read more about druid configuraiton [here](http://druid.io/docs/latest/configuration/index.html). 
* conf directory contains the common configuratios for all the nodes in druid for cluster setup.
* conf-quickstart contains the common configurations for the all the nodes running in one machine.
* extensions contains all the extensions that are packed by **druid-io**. If you want to have additional extensions that are not packed by **Druid Team**  because of licensing, you need to manually download or download them using pulldeps and put them in extension library. 

*Druid nodes benefit greatly from being tuned to the hardware they run on.*
