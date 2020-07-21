#!/usr/bin/python
import time
import sys
import atexit
import pyVmomi
from pyVmomi import vim, vmodl
from pyVim import connect
from pyVim.connect import Disconnect, SmartConnect, GetSi

#system = sys.argv[1]

inputs = {'vcenter_ip': '192.168.255.20',
  'vcenter_password': 'Test1234!',
  'vcenter_user': 'administrator@vsphere.local',
  'vm_name' : 'test01',
  'operation' : 'stop',
  'force' : True,
  }

# Functions

def get_obj(content, vimtype, name):
    objct = None
    container = content.viewManager.CreateContainerView(content.rootFolder, vimtype, True)
    for c in container.view:
        if c.name == name:
            objct = c
            break
    return objct

#sslContext = ssl.SSLContext(ssl.PROTOCOL_TLS)
#sslContext.verify_mode = ssl.CERT_NONE
si = connect.SmartConnectNoSSL(
                               host=inputs['vcenter_ip'],
                               port=443,
                               user=inputs['vcenter_user'],
                               pwd=inputs['vcenter_password'])
#si = SmartConnect(inputs['vcenter_ip'], 443, inputs['vcenter_user'], inputs['vcenter_password'],sslContext=sslContext)
#si = connect.Connect(inputs['vcenter_ip'], 443, inputs['vcenter_user'], inputs['vcenter_password'])
content = si.RetrieveContent()
vm = get_obj(content, [vim.VirtualMachine], inputs['vm_name'])
vm.PowerOff()


# Set to boot from cd/network. #'d out is what you'd use for network/pxe booting

#bn                  = vim.option.OptionValue(key='bios.bootDeviceClasses',value='allow:cd')
bn                  = vim.option.OptionValue(key='bios.bootDeviceClasses',value='allow:net')
vmconf              = vim.vm.ConfigSpec()
vmconf.extraConfig  = [bn]
vm.ReconfigVM_Task(vmconf)
time.sleep(10)
vm.PowerOnVM_Task()
time.sleep(30)


# Set system to boot from hdd again

bn                  = vim.option.OptionValue(key='bios.bootDeviceClasses',value='allow:hd,cd,fd,net')
vmconf              = vim.vm.ConfigSpec()
vmconf.extraConfig  = [bn]
vm.ReconfigVM_Task(vmconf)
