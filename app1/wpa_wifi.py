import re

class Network(object):

    """Represents a single network block in wpa_supplicant.conf."""

    def __init__(self, ssid, **opts):
        self.ssid = ssid
        self.opts = opts

    def __repr__(self):
        string = 'network={\n'
        string += '\tssid="{}"\n'.format(self.ssid)
        for opt, val in self.opts.items():
            string += '\t{}={}\n'.format(opt, val)
        string += '}'
        return string

    @classmethod
    def from_string(cls, string):
        """Create a new network object by parsing a string."""
        lines = string.split("\n")
        # throw away the first and last lines, and remove indentation
        lines = [line.strip() for line in lines[1:-1]]
        opts = {}
        for line in lines:
            split = line.split("=")
            opt = split[0]
            if len(split) == 2:
                value = split[1]
            else:
                value = "=".join(split[1:])
            opts[opt] = value
        # remove the SSID from the other options and strip the quotes from it.
        ssid = opts["ssid"][1:-1]
        del opts["ssid"]
        return cls(ssid, **opts)
    

class Fileconf(object):

    """Represents the conf file wpa_supplicant.conf."""

    def __init__(self, head, network_list, path):
        self.head = head
        self.network_list = network_list
        self.path = path

    @classmethod
    def from_file(cls, path):
        """Extract head and all network blocks from a file.
    
        Returns a list of Network objects.
    
        """
        #extract head
        with open(path) as netfile:
            config = netfile.read()
        head=[]
        for line in config.split("\n"):
            if line == "network={" :
                break
            else :
                head.append(line)
        
        #extract networks
        networks = []
        in_block = False
        netblock = []
        for line in config.split("\n"):
            line = line.strip()
            if line.startswith("#"):
                continue
            # this is really crappy "parsing" but it should work
            if line == "network={" and not in_block:
                in_block = True
            if in_block:
                netblock.append(line)
            if line == "}" and in_block:
                in_block = False
                nb = "\n".join(netblock)
                networks.append(Network.from_string(nb))
                netblock = []
        return cls(head,networks,path)
    
    def add(self, ssid, **opts):
        if not re.match("^[a-zA-Z0-9_-]+$", ssid): return (False, 'ssid')
        if 'psk' in opts : 
            if not re.match('[A-Za-z0-9@#$%^&+=]{8,}', opts['psk']) : return (False, 'psk')
            else : opts['psk'] = '"'+opts['psk']+'"'
        else :
            opts['key_mgmt']= "NONE"
        self.network_list.append(Network(ssid, **opts))
        return (True, 'ok')
        
    def suppr(self,ssid):
        index = None
        for netw in self.network_list:
            if netw.ssid == ssid : 
                index = self.network_list.index(netw)
                self.network_list.pop(index) 
        if index : return True
        else : return False
    
    
    def make_new(self):
        with open(self.path + ".bkp", "w") as bkp_file, open(self.path) as orig_file:
            bkp_file.write(orig_file.read())
        new_config = ""
        for line in self.head :
            new_config+= line
            new_config+= '\n'
        #new_config+= '\n'
        for net in self.network_list :
            new_config+=repr(net)
            new_config+= '\n\n'
        
        try :
            with open(self.path, "w") as cfile:
                cfile.write(new_config)
        except :
            return "Couldn't write config file"
        
        return new_config