# reverse_nmap

this is a framework so test client's behavior when server acts unexpectedly. 

## setting up GNS3 Topology
1. Download and import the portable project **[reverse_nmap.gns3project](https://drive.google.com/file/d/1599P12rLW_n3KJeWFQzMj6rq1WD9RRMI/view?usp=sharing)** 
2. Use https://hub.docker.com/r/khalid14hakami/basic_vm  for basic_vm images
3. Clone this repository at the root folder in all machines 
4. Run `prep_launch.sh` in all clients, servers and sniffers. This will run daemons listening for controller orders to start testing 
5. At the controller run `python3 controller_socket.py basic_scenario.json` to start the experiment
6. You can find the captured packets at `/root/reverse_nmap/test_capture.pcap` in the sniffer machine 
