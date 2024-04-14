import os
import subprocess

class SystemChanger:
    def __init__(self,boot_path, root_path):
        self.boot_path = boot_path
        self.root_path = root_path
        self.autostart_path =os.path.join(self.root_path, 'etc/xdg/lxsession/LXDE-pi/autostart')
      
    
    def check_system_version(self):
        
        check_os_path = os.path.join(self.root_path, 'etc/os-release')

        with open(check_os_path, 'r') as f:
            
            return f.readlines()[0].replace("\n","").replace("\"","").split('=')[1]
    
    def change_ip(self, ip):
        dhcpcd_path = os.path.join(self.root_path, 'etc/dhcpcd.conf')
        static_ip_template = f'''interface eth0
static ip_address={ip}/24
static routers=192.168.101.251
static domain_name_servers=192.168.101.251'''

        with open(dhcpcd_path, 'a') as f:
            f.write(static_ip_template)
            
    def set_snd(self,snd):
        with open(self.autostart_path, 'a')as file:
            file.write(f'@lxterminal -e sudo /home/pi/Desktop/json_connector {snd}\n')
    
    def set_program(self, program_path):
        last_part_of_path = '/'.join(program_path.split('/')[-2:])
        with open(self.autostart_path, 'a')as file:
            if 'python3' in program_path:
                file.write(f'@lxterminal -e sudo python3 /home/pi/Desktop/{last_part_of_path}\n')              
            elif "python2" in program_path:
                file.write(f'@lxterminal -e sudo python2 /home/pi/Desktop/{last_part_of_path}\n')

    def change_hostname(self,ip):
        hostname = f'rpi{ip.split(".")[-1]}'
        hostname_path = os.path.join(self.root_path,'etc/hostname')
        hosts_path = os.path.join(self.root_path,'etc/hosts')       
        
        with open(hostname_path,'w') as file:
            file.write(hostname)
        
        new_hosts_content = []
        with open (hosts_path, 'r') as file:
            
            for line in file :
                if '127.0.1.1' in line and 'rpi' in line:
                    new_hosts_content.append(f'127.0.1.1       {hostname}\n')
                else:
                    new_hosts_content.append(line)

            print(new_hosts_content)
            
        with open (hosts_path, 'w') as file:
            file.writelines(new_hosts_content)


class Validator:

    @staticmethod
    def validate_root(path):
        try:
            result = subprocess.run(
                ["cat", os.path.join(path, 'etc/os-release')],
                text=True,
                capture_output=True,
                check=True
            )
            print(result.stdout)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Błąd: {e}")
            return False

    @staticmethod
    def validate_boot(path):
        try:
            result = subprocess.run(
                ["cat", os.path.join(path, 'config.txt')],
                text=True,
                capture_output=True,
                check=True
            )
            print(result.stdout)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Błąd: {e}")
            return False
    
if __name__ == '__main__':
    system = SystemChanger('/media/pawel/boofs', '/media/pawel/roofs')
    print(system.check_system_version())