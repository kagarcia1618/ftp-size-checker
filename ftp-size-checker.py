import sys
import signal
import argparse
from ftplib import FTP, error_perm
from io import StringIO
from contextlib import contextmanager
from humanize import naturalsize
from socket import gaierror, timeout


class TimeoutException(Exception): pass

class FtpSizeChecker(object):
    def __init__(
        self,
        host: str,
        timeout: int,
        username: str,
        password: str = None,
        directory: str = None,
    ) -> None:
        self.host = host
        self.username = username
        self.password = password
        self.directory = directory
        self.timeout = timeout
        self.error = None

    @contextmanager
    def time_limit(self):
        def signal_handler(signum, frame):
            raise TimeoutException("Timed out!")
        signal.signal(signal.SIGALRM, signal_handler)
        signal.alarm(self.timeout)
        try:
            yield
        finally:
            signal.alarm(0)

    def fetch_total_bytes(self):
        try:
            ftp = FTP(self.host, timeout=10)
            if self.username == 'anonymous':
                ftp.login()
            else:
                ftp.login(
                    user = self.username,
                    passwd = self.password
                )
            if self.directory:
                ftp.cwd(self.directory)
        except (TimeoutError, gaierror, error_perm, timeout) as e:
            self.error = f"[ERROR] {e}"
            return
        
        # Create the in-memory "file"
        temp_out = StringIO()

        # Replace default stdout (terminal) with our stream
        sys.stdout = temp_out

        try:
            with self.time_limit():
                ftp.dir('-Rt')
        except TimeoutException:
            sys.stdout = sys.__stdout__
            self.error = f"[ERROR] Max timeout of {self.timeout} seconds reached!"
            return

        # Restore the original output stream to the terminal.
        sys.stdout = sys.__stdout__
        
        #Remove empty lines
        a = [ i for i in temp_out.getvalue().splitlines() if len(i) != 0 ]
        #Remove lines that belongs to a directory or symbolic link
        b = [ i for i in a if i[0] not in ['l','d','.']]

        total_bytes = 0
        for line in b:
            total_bytes += int([i for i in line.split(' ') if i != '' ][4])

        return naturalsize(total_bytes)

if __name__ == '__main__':
    #Create Command Line Arguments
    parser = argparse.ArgumentParser(description='FTP directory total file size checker.')
    parser.add_argument('--host', help='FTP hostname or IP address')
    parser.add_argument('--username', '-u', default = 'anonymous', help='FTP Username')
    parser.add_argument('--password', '-p', help='FTP Password')
    parser.add_argument('--directory', '-d', help='FTP Directory')
    parser.add_argument('--timeout',
        '-t',
        default = 60,
        type = int,
        help = 'Max timeout for fetching the FTP directory list')
    args = parser.parse_args()

    ftp_size = FtpSizeChecker(
        host = args.host,
        username = args.username,
        password = args.password,
        directory = args.directory,
        timeout = args.timeout,
    )
    context = '\n'.join([
        f"[INFO] FTP Host: {args.host}",
        f"[INFO] FTP Username: {args.username}" if args.username else "[INFO] FTP Username: anonymous",
        f"[INFO] FTP Directory: {args.directory}" if args.directory else "[INFO] FTP Directory: '/'",
        f"[INFO] FTP Timeout: {args.timeout} secs" if args.timeout else "[INFO] FTP Timeout: 60 secs",
    ])
    print(context)
    total_bytes = ftp_size.fetch_total_bytes()


    if total_bytes:
        print(f"[SUCCESS] Total File Size in Directory: {total_bytes}")
    else:
        print(ftp_size.error)
        # if args.timeout:
        #     print(f"[ERROR] Max timeout of {args.timeout} seconds reached!")
        # else:
        #     print(f"[ERROR] Max default timeout of 60 seconds reached!")