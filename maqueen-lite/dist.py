

import ast
import sys
import os
import time
import os.path
from serial.tools.list_ports import comports as list_serial_ports
from serial import Serial

from typing import List



def find_microbit():
    """
    Returns a tuple representation of the port and serial number for a
    connected micro:bit device. If no device is connected the tuple will be
    (None, None).
    """
    ports = list_serial_ports()
    for port in ports:
        if "VID:PID=0D28:0204" in port[2].upper():
            return (port[0], port.serial_number)
    return (None, None)


def get_all_microbit_ports():
    return [port for port in list_serial_ports()
                if 'VID:PID=0D28:0204' in port.usb_info().upper()]


def raw_on(serial):
    """
    Puts the device into raw mode.
    """

    def flush_to_msg(serial, msg):
        """Read the rx serial data until we reach an expected message."""
        data = serial.read_until(msg)
        if not data.endswith(msg):
            if COMMAND_LINE_FLAG:
                print(data)
            raise IOError("Could not enter raw REPL.")

    def flush(serial):
        """Flush all rx input without relying on serial.flushInput()."""
        n = serial.inWaiting()
        while n > 0:
            serial.read(n)
            n = serial.inWaiting()

    raw_repl_msg = b"raw REPL; CTRL-B to exit\r\n>"
    # Send CTRL-B to end raw mode if required.
    serial.write(b"\x02")
    # Send CTRL-C three times between pauses to break out of loop.
    for i in range(3):
        serial.write(b"\r\x03")
        time.sleep(0.01)
    flush(serial)
    # Go into raw mode with CTRL-A.
    serial.write(b"\r\x01")
    flush_to_msg(serial, raw_repl_msg)
    # Soft Reset with CTRL-D
    serial.write(b"\x04")
    flush_to_msg(serial, b"soft reboot\r\n")
    # Some MicroPython versions/ports/forks provide a different message after
    # a Soft Reset, check if we are in raw REPL, if not send a CTRL-A again
    data = serial.read_until(raw_repl_msg)
    if not data.endswith(raw_repl_msg):
        serial.write(b"\r\x01")
        flush_to_msg(serial, raw_repl_msg)
    flush(serial)


def raw_off(serial):
    """
    Takes the device out of raw mode.
    """
    serial.write(b"\x02")  # Send CTRL-B to get out of raw mode.
    
def clean_error(err):
    """
    Take stderr bytes returned from MicroPython and attempt to create a
    non-verbose error message.
    """
    if err:
        decoded = err.decode("utf-8")
        try:
            return decoded.split("\r\n")[-2]
        except Exception:
            return decoded
    return "There was an error."
    
def get_serial(port=None):
    """
    Detect if a micro:bit is connected and return a serial object to talk to
    it.
    """
    if port is None:
        port, serial_number = find_microbit()
    
    if port is None:
        raise IOError("Could not find micro:bit.")
    return Serial(port, SERIAL_BAUD_RATE, timeout=1, parity="N")
    
def execute(commands, serial=None):
    """
    Sends the command to the connected micro:bit via serial and returns the
    result. If no serial connection is provided, attempts to autodetect the
    device.
    For this to work correctly, a particular sequence of commands needs to be
    sent to put the device into a good state to process the incoming command.
    Returns the stdout and stderr output from the micro:bit.
    """
    close_serial = False
    if serial is None:
        serial = get_serial()
        close_serial = True
        time.sleep(0.1)
    result = b""
    raw_on(serial)
    time.sleep(0.1)
    # Write the actual command and send CTRL-D to evaluate.
    for command in commands:
        command_bytes = command.encode("utf-8")
        for i in range(0, len(command_bytes), 32):
            serial.write(command_bytes[i: min(i + 32, len(command_bytes))])
            time.sleep(0.01)
        serial.write(b"\x04")
        response = serial.read_until(b"\x04>")  # Read until prompt.
        out, err = response[2:-2].split(b"\x04", 1)  # Split stdout, stderr
        result += out
        if err:
            return b"", err
    time.sleep(0.1)
    raw_off(serial)
    if close_serial:
        serial.close()
        time.sleep(0.1)
    return result, err

def version(serial=None):
    """
    Returns version information for MicroPython running on the connected
    device.
    If such information is not available or the device is not running
    MicroPython, raise a ValueError.
    If any other exception is thrown, the device was running MicroPython but
    there was a problem parsing the output.
    """
    try:
        out, err = execute(
            [
                "import os",
                "print(os.uname())",
            ],
            serial,
        )
        if err:
            raise ValueError(clean_error(err))
    except ValueError:
        # Re-raise any errors from stderr raised in the try block.
        raise
    except Exception:
        # Raise a value error to indicate unable to find something on the
        # microbit that will return parseable information about the version.
        # It doesn't matter what the error is, we just need to indicate a
        # failure with the expected ValueError exception.
        raise ValueError()
    raw = out.decode("utf-8").strip()
    raw = raw[1:-1]
    items = raw.split(", ")
    result = {}
    for item in items:
        key, value = item.split("=")
        result[key] = value[1:-1]
    return result
    
def rm(filename, serial=None):
    """
    Removes a referenced file on the micro:bit.
    If no serial object is supplied, microfs will attempt to detect the
    connection itself.
    Returns True for success or raises an IOError if there's a problem.
    """
    commands = [
        "import os",
        "os.remove('{}')".format(filename),
    ]
    out, err = execute(commands, serial)
    if err:
        raise IOError(clean_error(err))
    return True

def ls(serial=None):
    """
    List the files on the micro:bit.
    If no serial object is supplied, microfs will attempt to detect the
    connection itself.
    Returns a list of the files on the connected device or raises an IOError if
    there's a problem.
    """
    out, err = execute(
        [
            "import os",
            "print(os.listdir())",
        ],
        serial,
    )
    if err:
        raise IOError(clean_error(err))
    return ast.literal_eval(out.decode("utf-8"))

def put(filename, target=None, serial=None):
    """
    Puts a referenced file on the LOCAL file system onto the
    file system on the BBC micro:bit.
    If no serial object is supplied, microfs will attempt to detect the
    connection itself.
    Returns True for success or raises an IOError if there's a problem.
    """
    if not os.path.isfile(filename):
        raise IOError("No such file.")
    with open(filename, "rb") as local:
        content = local.read()
    filename = os.path.basename(filename)
    if target is None:
        target = filename
    commands = [
        "fd = open('{}', 'wb')".format(target),
        "f = fd.write",
    ]
    while content:
        line = content[:64]
        if PY2:
            commands.append("f(b" + repr(line) + ")")
        else:
            commands.append("f(" + repr(line) + ")")
        content = content[64:]
    commands.append("fd.close()")
    out, err = execute(commands, serial)
    if err:
        raise IOError(clean_error(err))
    return True

    
def update_from_dist_folder(dist_folder: str) -> None:
    ports = get_all_microbit_ports()
    
    for filename in os.listdir(dist_folder):  
        for port in ports:      
            serial = get_serial(port[0])
            path = os.path.join(dist_folder, filename)
            print(f'Uploading file {path} to micro:bit connected on port {port[0]}', end=" ...")
            try:
                put(path, filename, serial)
                print('Success')
            except Exception as e:
                print(f'Failed. Reason: {e}')
        
        
def ls_all(ports=None):
    if ports is None:
        ports = get_all_microbit_ports()
        
    for port in ports:
        title = f"Listing files on micro:bit ({port[0]}):"
        print(title)
        print(len(title) * "=")
        try:
            serial = get_serial(port[0])
            files = ls(serial)
            show_files = '\n'.join(files)
            print(f"{show_files}")
        except Exception as e:
            print(f"Unable to complete ({str(e)})")
        
def rm_all(ports=None):
    if ports is None:
        ports = get_all_microbit_ports()
        
    for port in ports:
        title = f"Removing all files on micro:bit ({port[0]}):"
        print(title)
        # print(len(title) * "=")

        serial = get_serial(port[0])
        files = ls(serial)
        for f in files:
            print(f"{f}", end="... ")
            try:
                rm(f, serial)
                print("Success")
            except Exception as e:
                print(f"Unable to complete ({str(e)})")
    
PY2 = sys.version_info < (3,)
SERIAL_BAUD_RATE = 115200


def update_all():
    rm_all()
    update_from_dist_folder('dist')
    
    