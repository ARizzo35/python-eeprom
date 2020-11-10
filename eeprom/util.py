import subprocess


def check_device_exists(bus, addr):
    if not hasattr(check_device_exists, 'i2cdetect_bin'):
        check_device_exists.i2cdetect_bin = subprocess.getoutput('which i2cdetect')
    if check_device_exists.i2cdetect_bin:
        cp = subprocess.run(
            [check_device_exists.i2cdetect_bin, '-y', str(bus), str(addr), str(addr)],
            capture_output=True
        )
        if cp.returncode != 0:
            if "Permission denied" in cp.stderr.decode():
                raise PermissionError(cp.stderr.deocde())
            return False
        if '--' in cp.stdout.decode():
            return False
    return True
