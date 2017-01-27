<br>
### Benchmark and Report:
<hr>

Machine configuration follows here:


|  Cluster Name 	|   Public IP   	|     Instance ID     	|  Machine 	| Private IP 	|
|:-------------:	|:-------------:	|:-------------------:	|:--------:	|:----------:	|
| Master Server 	|  52.77.7.243  	| i-0cd6fed0db062e59f 	| m4.large 	|  10.2.1.98 	|
|  Data Servers 	| 52.220.96.213 	| i-062654d423a3acc1f 	| r3.large 	| 10.2.1.229 	|
| Query Servers 	|  52.74.85.207 	| i-0a98a683398eceffd 	| m4.large 	|  10.2.2.42 	|
| Capeve Server 	|  52.77.35.85  	| i-083eb4965531ab5df 	| m4.xlarge 	| 10.2.1.239 	|

_As we are getting  realtime data and less quering data, we grouped historical node and query servers and running them in query servers._

Using 1000 GB HDD as network file sharing for common purpose among all the servers to store and process the segments. Using Supervisor to automatically start the serverse whenever the server boots and node killed. 

Using Jmeter to generate the traffic. [Here](https://github.com/Voonik/dssquad/blob/druid-beast/benchmark/druid.jmx) is jmx file used to generate dynamic traffic. 

> * Total number of events fired on 2017-01-16: 5717275 (with Peak traffic for 2 hours, over a period of 6 hours) <br>
> * Total number of events fired on 2017-01-17: 4592895 (10:00AM IST to 2:00PM IST) <br>
> * Max lag of Consumer: 406237 <br>
> * Avg lag observed: lessthan 2K <br> (On Realtime traffic)
> * Throughput Avg ~ 40K

<br>
###### All Servers CPU:
![All Servers CPU](https://s29.postimg.org/g541q5gqv/All_Servers_CPU.png "CPU Usage")  

###### All Servers Load:
![All Servers CPU](https://s29.postimg.org/kfiplqltz/All_Servers_Load.png "Load")

###### All Servers Memory:
![All Servers CPU](https://s29.postimg.org/co1zn6hon/All_Servers_Memory.png "Memory Usage")

###### Application Apdex Score:
![Apdex Score](https://s29.postimg.org/or7baqsqv/apdex_score.png "APDEX SCore") ![App Throughput](https://s29.postimg.org/n3hcnktmv/Throughput.png "Troughput")

###### Application Response Time:
![App Response Time](https://s29.postimg.org/hchzid6vb/Application_Response_Time.png "App Response Time")

###### Error Rate
![App Error Rate](https://s29.postimg.org/va4r1eubr/Error_Rate.png "Error Rate")

######  Nginx Connections
![Nginx C ](https://s29.postimg.org/67xmatyiv/Nginx.png "Nginx Connnections")

![Nginx RR ](https://s29.postimg.org/kjh4fqgp3/Nginx_Request_Rate.png "Nginx Request Rate")

![Nginx AR ](https://s29.postimg.org/sl5cxmzgn/Nginx_Accept_Rate.png "Nginx Accept Rate")

###### PM2 Stats
![Capeve CPU](https://s29.postimg.org/fm3jumepz/Capeve_CPU.png "Capeve CPU") ![Master CPU](https://s29.postimg.org/kbthj85qf/Master_CPU.png "Master CPU")

![Capeve Memory](https://s29.postimg.org/wb4zqjbbb/Capeve_Memory.png "Capeve Memory") ![Capeve Memory](https://s29.postimg.org/66nohewp3/Master_Memory.png "Master Memory")

###### On 2017-01-17
![Throughput](https://s28.postimg.org/6miisxhzx/Screen_Shot_2017_01_17_at_3_27_23_PM.png) ![Error Rate](https://s28.postimg.org/f61wqoqcd/Screen_Shot_2017_01_17_at_3_27_34_PM.png)




<br>
### Infrastructure Cost
<hr>

As per the above mentioned setup, following is the calculated price as per dollar value on 17th Jan 2017.

| Machine Type 	| Hourly Cost  	| Daily Cost 	| Monthly Cost 	| No of Units 	| Total Cost in $ 	| Total Cost in Rupees 	|
|:------------:	|:------------:	|:----------:	|:------------:	|:-----------:	|:---------------:	|:--------------------:	|
|   m4.large   	|    0.1340    	|    3.216   	|     96.48    	|      2      	|      192.96     	|      13117.4208      	|
|   m4.xlarge  	|     0.266    	|    6.384   	|    191.52    	|      1      	|      191.52     	|      13019.5296      	|
|   r3.large   	|      0.2     	|     4.8    	|      144     	|      1      	|       144       	|        9789.12       	|
|  Elastic Ip  	|              	|            	|      3.6     	|      4      	|       14.4      	|        978.912       	|
|    Volume    	|              	|            	|     0.125    	|    1000GB   	|       125       	|        8497.5        	|
|              	|              	|            	|              	|             	|      667.88     	|       45402.48       	|

<br>
### Recommendaitons:
<hr>

* We can reduce 1000GB Volume to 100 GB. Amount utilised till now - 7.9GB
* Increasing the capacity of CapV Cluster. 
* Data server needs more CPU. 


