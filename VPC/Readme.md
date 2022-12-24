# VPC

Try to explain the basics of VPC.

What is VPC?

A virtual private cloud (VPC) is a private cloud computing environment contained within a public cloud. Essentially, VPC provisions logically isolated sections of a public cloud in order to provide a virtual private environment.

![VPC Architecture!](/VPC/doc/vpc.png "VPC Architecture")

## VPC Analogy

1. VPC = Society
2. Private IP = Private Address
3. Public IP = Public Address
4. Route Table = Different-2 way to building of Society
5. Security Group = Building Guard
6. Network ACLs = Security checkpoint @ block level

### VPC = Society

If you want to protect your society from outside attacks then you create an isolated environment/keep security. This is called VPC.

### Private IP

1. Private Address for internal service/Private Address for a flat like "Block-A-Building-A-101".
2. Not for everyone, only for internal usage/society.

### Public IP -

1. Public Address for internal service/Public Address for a flat like flat No - "101"
2. For everyone/outside world.

### Route Table - Different-2 ways to the Building Society

A routing table contains a set of rules, called routes, that determine where network traffic from your subnet or gateway is directed.

In a Simple world, Which IP Addresses/Routes(Society) are allowed to access other services of cloud/society block address?

> Each RT has a VPC address likewise all society members can go into each building from each route of society.

Suppose There is one main table RT. Each routing table contains VPC Address as local, you can not remove it. Now you can enter which IP Addresses/Routes(Society)/Routes to the Outside world(Like zomanto/swiggy service/It can be IGW) are allowed.

> If the machine/building wants to talk to the outside world it should have public IP/public address and IGW(Like zomanto/swiggy service). It is called a public subnet/society block. Another hand society's office is private because it only allows a specific person.

You can create different RTs. Why do you want to create a different - 2 RT?

> Because you don't want to allow access to the outside world/another part of buildings/services. Basically, you want to keep it private. Like society office is private, you don't want that everyone should know details about society if they do not have permission. OR Maybe different-2 building wants to maintain different-2 routes. Maybe fights b/w 2 buildings, who knows :stuck_out_tongue_closed_eyes: .

> If you attach another RT(Maintained different route and closed common route) that is other than the main RT to the subnet/society then Main RT will be disconnected.

### Security Group = Building Guard

SG is applied on the instance level/building level. So whenever you enter the building security will check. Filter traffic @ instance level. SG is a stateful firewall. A stateful firewall allows the return of traffic automatically. Likewise, when you enter the building, the building guard will check but when you exit from the building guard will not check. It needs an inbound rule.

### Networl ACLs = Security checkpoint @ block level

It is applied on the subnet level/block level of society. It will apply only to traffic entering/exiting of subnet. Each time security checks vehicles when it goes and when it comes. Filter traffic @ block level. NACLs is a stateless firewall. A stateless firewall does not allow the return traffic automatically. Likewise, when you enter the building, the Security checkpoint will check the vehicle and when you go out also it will check that you are taking the correct vehicle. It needs inbound & outbound rules both. Order matters.

#### Documents

1. [Create VPC & Subnet(Public & Private)](<https://github.com/varunajmera0/AWS/tree/main/vpc/doc/AWS_VPC_Subnet(Public&Private).pdf>)

2. [Route Table (Public & Private)](<https://github.com/varunajmera0/AWS/tree/main/vpc/doc/VPC_route_table(public&privatesubnets).pdf>)

3. [IGW](https://github.com/varunajmera0/AWS/tree/main/vpc/doc/public_ipv4&internet_gateway_vpc.pdf)

4. [SG](https://github.com/varunajmera0/AWS/tree/main/vpc/doc/vpc_security_group.pdf)

5. [EC2](https://github.com/varunajmera0/AWS/tree/main/vpc/doc/ec2_public_private.pdf)

6. [EC2 Login](https://github.com/varunajmera0/AWS/tree/main/vpc/doc/login_connect_public_priavte&ping_ec2.pdf)

7. [Reference](https://github.com/varunajmera0/AWS/tree/main/vpc/doc/vpc_security_group.pdf)

Credits -
https://www.udemy.com/course/networking-in-aws/ - [Reference](https://github.com/varunajmera0/AWS/tree/main/vpc/doc/vpc_security_group.pdf)

> Happy Coding! :v:
