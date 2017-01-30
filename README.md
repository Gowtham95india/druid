<br>
### Benchmark and Report:
<hr>

Machine configuration follows here:


|  Cluster Name 	|   Public IP   	|     Instance ID     	|  Machine 	| Private IP 	|
|:-------------:	|:-------------:	|:-------------------:	|:--------:	|:----------:	|
| Master Server 	|  52.77.7.243  	| i-0cd6fed0db062e59f 	| m4.large 	|  10.2.1.98 	|
|  Data Servers 	| 52.220.96.213 	| i-062654d423a3acc1f 	| r3.xlarge 	| 10.2.1.229 	|
| Query Servers 	|  52.74.85.207 	| i-0a98a683398eceffd 	| m4.xlarge 	|  10.2.2.42 	|
| Capeve Server 	|  52.77.35.85  	| i-083eb4965531ab5df 	| t2.micro 	| 10.2.1.239 	|
|  Kafka Server 	|  52.74.151.229  	| i-0bc71df9ed6078b30 	| m4.large 	| 10.2.1.157 	|
|  NodeJs Server 	|  52.220.195.68  	| i-0d39c8daf7ce756aa 	| m4.large 	| 10.2.1.171 	|

_As we are getting  realtime data and less quering data, we grouped historical node and query servers and running them in query servers._

Using 1000 GB HDD as network file sharing for common purpose among all the servers to store and process the segments. Using Supervisor to automatically start the serverse whenever the server boots and node killed. 

Using Jmeter to generate the traffic. [Here](https://github.com/Voonik/dssquad/blob/druid-beast/benchmark/druid.jmx) is jmx file used to generate dynamic traffic. 