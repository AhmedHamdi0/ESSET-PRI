import subprocess


class Programming:
    def __init__(self, svf_file):
        self.file_name = f"/home/esset/FTP/files/svf/top_level.svf"
        self.command = [
            "openocd",
            "-f", "/usr/share/openocd/scripts/interface/altera-usb-blaster.cfg",
            "-f", "/home/esset/FTP/files/openocd/cyclon4.cfg",
            "-c", "init",
            "-c", "svf {}".format(self.file_name),
            "-c", "shutdown"
        ]
    
    def run(self):
        print("\nFPGA Programming Started...\n")
        subprocess.run(self.command)
        print("\nFPGA Programming Finished...\n")
