# Network Metrology Project

The objective of our project is to lead a metrological study over the website weather.com, known worldwide with a high attendance and a major social impact. We will mainly focus on the 3rd and 4th layers (network and transport). Firstly, we will look at a few basic ping instructions, which will lead us to the concept of CDN. Then, we will approach seasonality and the impact of the means of connection. Finally, we will be interested in the routes that the packets take to reach the server. All the scripts and data files are available on our GitHub repository. During the experiments, we used different kinds of means of connections: Wi-Fi, Ethernet, 4G and 5G on our two laptops.

## I - Basic ping, where is the weather.com server?

Let us start by sending basic ping instructions to the weather.com server to observe elementary information. The associated IP address is either **23.217.186.82** if launched from the campus (Eduroam) or **2a02:26f0:b80:784::2e03** if launched from our apartments in Villeurbanne (Bouygues’s and SFR’s Wi-Fi). The IP Address Lookup website reveals that the IPv4 address is in Paris and the IPv6 address is in Marseille. However, this is a local approach. Testing elsewhere in France could yield different results. Weather.com is owned by The Weather Company, an American corporation, but the servers are in France because they belong to Akamai Technologies. Akamai is an American company that provides Content Delivery Network (CDN), cybersecurity, DDoS mitigation, and cloud services.

A CDN involves the original server (weather.com in America) and edge servers (belonging to Akamai and perhaps others) deployed in multiple locations, where content is replicated. The advantages of using a CDN include improving load times, enhancing security, and ensuring high availability by delivering content from servers closest to users. In our case, it might also be for personalizing data; for example, the server in Paris may only hold meteorological data for France and nearby countries. The caching policy used in this contract is also in question. Is it a pull CDN? Push CDN? Cache purging? Further tests may help us determine this.

## II - Seasonality

![MET pictures/rtt_image.png](https://github.com/Kactus29/MET_Project/blob/961e70bea22e5b2eea6952367f9e6b7d5d966d4c/MET%20pictures/rtt_image.png)

### Figure 1: RTT evolution during the day of 10/11/2024

Now that we know where the packets are sent, let’s focus on the time they take to travel. We coded a python script to send a ping request to the website every 20 minutes for 24 hours. We used Bouygues's Wi-Fi (with fiber).  All the packets we looked at during the measurement have been routed to the server in Marseille. So, let’s assume they all went there. Any small spikes could represent either a connection problem on my Wi-Fi or small congestion in the network. The large peak could represent a very large congestion or a sending to the original server in the United States, the order of magnitude of the RTT time corresponds. Both explanations are possible.

We expected to see more congestion in the early morning or the late evening. These are the times when people watch the weather the most. But that's not really the case here in the morning. On the other hand, between 3pm and 8pm is when the spikes are concentrated, which is predictable. The measurements were taken over a 3-day weekend, a weekday might be closer to our assumptions. If this intuition proves to be correct, it would be possible to adapt the allocation of resources to the server so that more are available at peak times and less at off-peak times. Or maybe this is already implemented. It's an ecological and economic approach.

## III - Impact of the mean of connection

During this part we will focus on the impacts of the means of connection. To do so, we sent 100 pings to the website every hour the 12/11/2024 between 14 and 18 with 4 means of connection: Ethernet, Wi-Fi, 5G and 4G. The graph below represents the means RTT (in ms) for each demand. The command line used was in the form of **ping weather.com -n 100 > "name of the file”**.

![Latency/RTT evolution between 14h and 18h the 12/11/2024 with 4 means of connection](https://github.com/Kactus29/MET_Project/blob/8fa4066d191ce9f88b89791aa89a985350b70b98/MET%20pictures/latency_image.png)

### Figure 2: Latency/RTT evolution between 14h and 18h the 12/11/2024 with 4 means of connection

The network latency experiment results clearly show the speed order as Ethernet, Wi-Fi, 5G, and 4G, which is predictable given the characteristics of each connection. Ethernet was the fastest and most stable with a constant 8 ms latency, but it is restrictive as it requires a fixed PC. Wi-Fi had slightly higher but stable latency around 10-11 ms, offering practical and acceptable performance for most uses. 5G and 4G showed higher and more variable latencies, with 5G ranging from 37-44 ms and 4G from 42-51 ms, likely influenced by mobile plans and location. Each connection type has its pros and cons: Ethernet offers optimal speed and stability but lacks mobility, Wi-Fi provides good performance and flexibility, while 5G and 4G offer mobility with acceptable but variable performance. The choice of connection depends on specific needs for speed, stability, and mobility.

## IV – Path Evolution & Traceroute

In this last section, we attend to represent the path of our ping packet by topography methodology. Using the traceroute command and other similar tools (pathping, Zenmap, trt online, ping.pe and mtr on wsl), we captured and compared the routing path from different locations, aiming to map common paths and identify key interconnection zones within the network infrastructure.

![Paths from physical laptop to CDN](https://github.com/Kactus29/MET_Project/blob/main/MET%20pictures/Zenmap%20vf.png)

### Figures 3: Paths from physical laptop to CDN 

![Paths from virtual machines to server in USA](https://github.com/Kactus29/MET_Project/blob/main/MET%20pictures/Mtr%20virtuel%20vf.png)

### Figure 4: Paths from virtual machines to server in USA

First, we tried to map the network paths between our laptops (connected with either Eduroam, 4G or personal Wi-fi) and the Ankamai CDN, located in Marseille. The first problem we encountered was the difficulty dealing with the protection against the ICMP requests of a usual traceroute: even pathping, super traceroute and all the other tools we found on Ubuntu by wsl were blocked.

Then, we switched to plenty of solutions using TCP or UDP instead of ICMP, as tcp traceroute, mtr on wsl and nmap on Zenmap (cf. Fig.3, **cmd. nmap -sS -Pn --traceroute www.weather.com** ). Finally, we were not able to obtain any data (address & location) about the key points in the topography (cf. “web” Fig.3), but we got a great vision of the whole path with Zenmap.

As it was impossible for us to travel nor obtain data about exchanges between physical machines in foreign countries and the server of the website, in the last part of our project we used ping.pe to simulate mtr from various locations all over the world. Analyzing the collected traceroute data, we observed a set of consistent “pathways” through the network that represent regional or ISP-based interconnection bands. These nodes act as critical points where traffic is routed between major network infrastructures.

To sum things up, by questioning a network topography, it is possible to reveal occasional deviations, indicating alternate paths potentially influenced by network congestion, routing policies, or maintenance. By observing when these deviations occur, we can hypothesize correlations with network load, time of day, and possible peering agreements affecting route selection.
