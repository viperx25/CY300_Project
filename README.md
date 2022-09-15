# CY300_Project

## Setup
To set up the namespace environment, run the following command:\
`# ./setup.sh`

## Utilizing Namespaces
To run a command from a given namespace, use the following:\
`# ./ns1 "[cmd in ns1]"`\
`# ./ns2 "[cmd in ns2]"`

### Example
To ping from ns1 to ns2:\
`# ./ns1 "ping 10.10.10.2"`\
\
To ping from ns2 to ns1:\
`# ./ns2 "ping 10.10.10.1"`\
\
To run packet sniffer on veth1 (ns1):\
`# ./ns1 "./sniffer.py"`\
