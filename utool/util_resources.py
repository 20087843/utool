from __future__ import absolute_import, division, print_function
# Python
import os
from utool.util_inject import inject
from utool.util_str import byte_str2
print, print_, printDBG, rrr, profile = inject(__name__, '[print]')

try:
    # Resource does not exist in win32
    import resource

    def time_in_usermode():
        stime = resource.getrusage(resource.RUSAGE_SELF).ru_stime
        return stime

    def time_in_systemmode():
        utime = resource.getrusage(resource.RUSAGE_SELF).ru_utime
        return utime

    def peak_memory():
        """Returns the resident set size (the portion of
        a process's memory that is held in RAM.)
        """
        # MAXRSS is expressed in kilobytes. Convert to bytes
        maxrss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024
        return maxrss

    def get_resource_limits():
        #rlimit_keys = [key for key in six.iterkeys(resource.__dict__) if key.startswith('RLIMIT_')]
        #print('\n'.join(['(\'%s\', resource.%s),' % (key.replace('RLIMIT_', ''), key) for key in rlimit_keys]))
        rlim_keytups = [
            ('MEMLOCK', resource.RLIMIT_MEMLOCK),
            ('NOFILE', resource.RLIMIT_NOFILE),
            ('CPU', resource.RLIMIT_CPU),
            ('DATA', resource.RLIMIT_DATA),
            ('OFILE', resource.RLIMIT_OFILE),
            ('STACK', resource.RLIMIT_STACK),
            ('FSIZE', resource.RLIMIT_FSIZE),
            ('CORE', resource.RLIMIT_CORE),
            ('NPROC', resource.RLIMIT_NPROC),
            ('AS', resource.RLIMIT_AS),
            ('RSS', resource.RLIMIT_RSS),
        ]
        rlim_valtups = [(lbl, resource.getrlimit(rlim_key)) for (lbl, rlim_key) in rlim_keytups]
        def rlimval_str(rlim_val):
            soft, hard = rlim_val
            softstr = byte_str2(soft) if soft != -1 else 'None'
            hardstr = byte_str2(hard) if hard != -1 else 'None'
            return '%12s, %12s' % (softstr, hardstr)
        rlim_strs = ['%8s: %s' % (lbl, rlimval_str(rlim_val)) for (lbl, rlim_val) in rlim_valtups]
        print('Resource Limits: ')
        print('%8s  %12s  %12s' % ('id', 'soft', 'hard'))
        print('\n'.join(rlim_strs))
        return rlim_strs

    #def rusage_flags():
        #0	ru_utime	time in user mode (float)
        #1	ru_stime	time in system mode (float)
        #2	ru_maxrss	maximum resident set size
        #3	ru_ixrss	shared memory size
        #4	ru_idrss	unshared memory size
        #5	ru_isrss	unshared stack size
        #6	ru_minflt	page faults not requiring I/O
        #7	ru_majflt	page faults requiring I/O
        #8	ru_nswap	number of swap outs
        #9	ru_inblock	block input operations
        #10	ru_oublock	block output operations
        #11	ru_msgsnd	messages sent
        #12	ru_msgrcv	messages received
        #13	ru_nsignals	signals received
        #14	ru_nvcsw	voluntary context switches
        #15	ru_nivcsw	involuntary context switches
except ImportError:
    def time_in_usermode():
        raise NotImplementedError('unavailable in win32')

    def time_in_systemmode():
        raise NotImplementedError('unavailable in win32')

    def peak_memory():
        """Returns the resident set size (the portion of
        a process's memory that is held in RAM.)
        """
        raise NotImplementedError('unavailable in win32')

    def get_resource_limits():
        raise NotImplementedError('unavailable in win32')


def time_str2(seconds):
    return '%.2f sec' % (seconds,)


def print_resource_usage():
    print(get_resource_usage_str())


def get_resource_usage_str():
    usage_str_list = [
        ('+______________________'),
        ('|    RESOURCE_USAGE    '),
        ('|  * current_memory = %s' % byte_str2(current_memory_usage())),
    ]
    try:
        usage_str_list.extend([
            ('|  * peak_memory    = %s' % byte_str2(peak_memory())),
            ('|  * user_time      = %s' % time_str2(time_in_usermode())),
            ('|  * system_time    = %s' % time_str2(time_in_systemmode())),
        ])
    except Exception:
        pass
    usage_str_list.append('L______________________')
    usage_str = '\n'.join(usage_str_list)
    return usage_str


def current_memory_usage():
    import psutil
    meminfo = psutil.Process(os.getpid()).get_memory_info()
    rss = meminfo[0]  # Resident Set Size / Mem Usage
    vms = meminfo[1]  # Virtual Memory Size / VM Size  # NOQA
    return rss


def num_cpus():
    import psutil
    return psutil.NUM_CPUS


def available_memory():
    import psutil
    return psutil.virtual_memory().available


def total_memory():
    import psutil
    return psutil.virtual_memory().total


def used_memory():
    return total_memory() - available_memory()


def memstats():
    print('[psutil] total     = %s' % byte_str2(total_memory()))
    print('[psutil] available = %s' % byte_str2(available_memory()))
    print('[psutil] used      = %s' % byte_str2(used_memory()))
    print('[psutil] current   = %s' % byte_str2(current_memory_usage()))


#psutil.virtual_memory()
#psutil.swap_memory()
#psutil.disk_partitions()
#psutil.disk_usage("/")
#psutil.disk_io_counters()
#psutil.net_io_counters(pernic=True)
#psutil.get_users()
#psutil.get_boot_time()
#psutil.get_pid_list()
