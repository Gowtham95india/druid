# Druid Cluster Setup

Druid cluster can scale horizontally. It has individual nodes like broker, coordinator, overlord, middlemanager, historical. For our convience, we will club the components to use the resources effectively.


### Basic understanding about Druid Cluster:
<hr>

Master server contains Overlord and Coordinator running which manages and handovers the task to middlemanager and historical nodes. 
* The **Overlord node** is responsible for accepting tasks, coordinating task distribution, creating locks around tasks, and returning statuses to callers.
* The **Coordinator node** is responsible for loading new segments, dropping outdated segments, managing segment replication, and balancing segment load.
* Each **historical** node maintains a constant connection to Zookeeper and watches a configurable set of Zookeeper paths for new segment information. 
* The **middle manager** node is a worker node that executes submitted tasks. 
* The **Broker node** is to route queries to if you want to run a distributed cluster. This node also merges the result sets from all of the individual nodes together 


Using 1000 GB HDD as network file sharing for common purpose among all the servers to store and process the segments. Using Supervisor to automatically start the serverse whenever the server boots and node killed. 

>Master Servers  &nbsp;&nbsp;&nbsp;&nbsp; Overlord + Coordinator - 1st boot priority
><br>
>Data Servers   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  MiddleManager + Historical - 2nd boot priority
><br>
>Query Servers  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Broker  Node + Pivot - 3rd boot priority


![Druid Cluster Setup](https://blog.codecentric.de/files/2016/08/Druid.png "Druid Cluster")


<br>
### Configuration and Setup
<hr>

Add 1000 GB volume to master server and using nfs share mount it to other clusters. You can read more about the nfs mounting and sharing [ here ](http://docs.aws.amazon.com/efs/latest/ug/mounting-fs.html#mounting-fs-nfs-info).  
This is [on GitHub](https://github.com/jbt/markdown-editor) so let me know if I've b0rked it somewhere.

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

### Checks and Commands:
<hr>

* Ensure nfs is mounted in all the servers except capeve serevr.
* If not, mount nfs and then restart supervisor using the commands given below.
* Kafka all brokers should be up and running. Make sure all the 3 brokers are running. If not check for the error file in /var/lib/kafka directory. Generally error file starts with **hs_**

```bash
# Mount nfs volume
sudo mount 10.2.1.98:/vol/druid/ /vol/druid/

# Check Tranquility Kafka consuming events more than 10k in ms.
cat /vol/druid/imply-2.0.0/var/mk_node/sv/tranquility-kafka.log | grep -E "Flushed {vnk-clst={receivedCount=[1][9][0-9]{3}" | grep "2017-01-17"

# Check Tranquility Kafka offset (Consumed so far).
cd /var/lib/kakfa
./bin/kafka-run-class.sh kafka.tools.ConsumerOffsetChecker --topic vnk-clst --zookeeper localhost:2181 --group tranquility-kafka

# Check topic configs. Replication factor 3 in our case. All brokers should be in sync.
cd /var/lib/kafka
./bin/kafka-topics.sh --describe --zookeeper localhost --topic vnk-clst

# To increase replication factor of existing topic.
cd /var/lib/kafka
./bin/kafka-reassign-partitions.sh --zookeeper localhost:2181 --reassignment-json-file increase-replication-factor.json --execute

# Using kafkat tool. Command line utility for Kafka.
# Increasing replication factor. Not reliable way.
kafkat set-replication-factor vnk-clst --newrf 3 --brokers  [0,1,2]

# Creating topic in kafka.
cd /var/lib/kafka
./bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 3 --partitions 1 --topic vnk-clst

# To change retention period of a topic.
./bin/kafka-topics.sh --zookeeper localhost:2181 --alter --topic vnk-clst --config retention.ms=10

# Deleting a config. 
./bin/kafka-topics.sh --zookeeper localhost:2181 --alter --topic vnk-clst --delete-config retention.ms

# Creating NodeJS server with pm2.
pm2 start /var/lib/capeve/server.js --name capeve -i 100 --max-memory-restart 100M --node-args="--max_old_space_size=200"

# Scaling up/down pm2 instance
pm2 scale capeve 100
```

### References:
<hr>

* Kafka Setup [here](https://www.digitalocean.com/community/tutorials/how-to-install-apache-kafka-on-ubuntu-14-04)
* nfs-mount [here](https://www.digitalocean.com/community/tutorials/how-to-set-up-an-nfs-mount-on-ubuntu-12-04)
* Kafka MultiBroker [here](http://www.michael-noll.com/blog/2013/03/13/running-a-multi-broker-apache-kafka-cluster-on-a-single-node/)
* Druid White Paper [here](http://static.druid.io/docs/druid.pdf)
* Imply Archtecture [here](https://imply.io/docs/latest/)
* Imply Cluster [here](https://imply.io/docs/latest/cluster)
