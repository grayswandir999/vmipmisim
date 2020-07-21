# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# ipmisim - Fake IPMI simulator for testing, forked from Conpot
# Maintainer - Rohit Yadav <bhaisaab@apache.org>
# Original Author: Peter Sooky <xsooky00@stud.fit.vubtr.cz>
# Brno University of Technology, Faculty of Information Technology

import logging
import sys
import time
import time
import atexit
import argparse
from pyVmomi import vim, vmodl
from pyVim import connect
from pyVim.connect import Disconnect, SmartConnect, GetSi
import ssl

from pyghmi.ipmi.bmc import Bmc

logger = logging.getLogger('ipmisim')

inputs = {'vcenter_ip': '192.168.255.20',
  'vcenter_password': 'Test1234!',
  'vcenter_user': 'administrator@vsphere.local',
  'vm_name' : 'test01',
  'operation' : 'stop',
  'force' : True,
  }

def get_obj(content, vimtype, name):
    objct = None
    container = content.viewManager.CreateContainerView(content.rootFolder, vimtype, True)
    for c in container.view:
        if c.name == name:
            objct = c
            break
    return objct

si = connect.SmartConnectNoSSL(host=inputs['vcenter_ip'],port=443,user=inputs['vcenter_user'],pwd=inputs['vcenter_password'])
content = si.RetrieveContent()
vm = get_obj(content, [vim.VirtualMachine], inputs['vm_name'])

class FakeBmc(Bmc):

    def __init__(self, authdata):
        self.authdata = authdata
        # Initialize fake BMC config
        self.deviceid = 0x24
        self.revision = 0x10
        self.firmwaremajor = 0x10
        self.firmwareminor = 0x1
        self.ipmiversion = 2
        self.additionaldevices = 0
        self.mfgid = 0xf
        self.prodid = 0xe

        self.powerstate = 'off'
        self.bootdevice = 'default'
        logger.info('IPMI BMC initialized.')



    def get_boot_device(self):
        logger.info('IPMI BMC Get_Boot_Device request.')
        return self.bootdevice

    def set_boot_device(self, bootdevice):
        logger.info('IPMI BMC Set_Boot_Device request.')
        logger.info(bootdevice)
        if bootdevice == 'network':
            bn = vim.option.OptionValue(key='bios.bootDeviceClasses',value='allow:net')
            vmconf = vim.vm.ConfigSpec()
            vmconf.extraConfig = [bn]
            vm.ReconfigVM_Task(vmconf)
        elif bootdevice == 'optical':
            bn = vim.option.OptionValue(key='bios.bootDeviceClasses',value='allow:cd,hd,fd,net')
            vmconf = vim.vm.ConfigSpec()
            vmconf.extraConfig = [bn]
            vm.ReconfigVM_Task(vmconf)
        elif bootdevice == 'floppy':
            bn = vim.option.OptionValue(key='bios.bootDeviceClasses',value='allow:fd,cd,hd,net')
            vmconf = vim.vm.ConfigSpec()
            vmconf.extraConfig = [bn]
            vm.ReconfigVM_Task(vmconf)
        elif bootdevice == 'hd':
            bn = vim.option.OptionValue(key='bios.bootDeviceClasses',value='allow:hd,cd,fd,net')
            vmconf = vim.vm.ConfigSpec()
            vmconf.extraConfig = [bn]
            vm.ReconfigVM_Task(vmconf)
        else:
            logger.info(bootdevice)
        self.bootdevice = bootdevice

    def cold_reset(self):
        logger.info('IPMI BMC Cold_Reset request.')
        self.powerstate = 'off'
        self.bootdevice = 'default'

    def get_power_state(self):
        logger.info('IPMI BMC Get_Power_State request.')
        return self.powerstate

    def power_off(self):
        logger.info('IPMI BMC Power_Off request.')
        vm.PowerOff()
        self.powerstate = 'off'

    def power_on(self):
        logger.info('IPMI BMC Power_On request.')
        vm.PowerOnVM_Task()
        self.powerstate = 'on'

    def power_reset(self):
        logger.info('IPMI BMC Power_Reset request.')
        vm.ResetVM_Task()
        self.powerstate = 'on'

    def power_cycle(self):
        logger.info('IPMI BMC Power_Cycle request.')
        # cold boot
        vm.ResetVM_Task()
        self.powerstate = 'off'
        self.powerstate = 'on'

    def power_shutdown(self):
        logger.info('IPMI BMC Power_Shutdown request.')
        vm.RebootGuest()
        self.powerstate = 'off'
