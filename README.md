# vmipmisim

A fake ipmi server for testing purposes both as a tool and a library.
The code is forked from [Conpot](http://conpot.org/) and based on `pyghmi`.

This fork called vmipmisim is targeted at the goal of enabling testing IPMI workflows with vm infrastructure.

The tool ships with default sets of users for ease of use:

    ID  Name       Callin  Link Auth  IPMI Msg   Channel Priv Limit
    1   admin            true    true       true       ADMINISTRATOR
    2   operator         true    false      false      OPERATOR
    3   user             true    true       true       USER

The default passwords are:

    admin  : password
    opuser : oppassword
    user   : userpassword

Installation:

Work in progress

Running: 

    ipmisim 3000 testvm01 vmware vcsa01.dev.local administrator@vsphere.local Test1234! 
    # Runs on custom port 3000, else 9001 by default
    # Performs IPMI action on testvm01
    # VM type of VMware, libvirt, hyperv so know what type of infrastructure to connect to. Hyperv and libvirt are work ing progress
    # vcsa01.dev.local the vcenter or other management host with api to connect to, should work with esxi host directly also.
    # administrator@vsphere.local, username to conenct to infrastructure with
    # Test1234!, password for the username.
    # All of the above should be passed as environment variables or fetched at run time in ideal circumstances, commandline switches present for testing and prototyping.

Updated make file to use python 3 although this should probably be set through the path instead. 
If you want to test on 623 the default ipmi port then you may have to adjust permissions on the destination system. 

Testing with ipmitool:

    ipmitool -I lanplus -H localhost -p 9001 -R1 -U admin -P password chassis power status
