from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger


import signal

sched = BlockingScheduler()

@sched.scheduled_job(trigger=IntervalTrigger(seconds=30))
def connect():
    import populate

    populate.main()


def shutdown_scheduler(signum, frame):
    print("Shutting down scheduler...")
    sched.shutdown()


# Register the signal handler for SIGINT (Ctrl+C)
signal.signal(signal.SIGINT, shutdown_scheduler)

# sched.configure(options_from_ini_file)
try:
    sched.start()
except (KeyboardInterrupt, SystemExit):
    # Handle the shutdown cleanly in case of Ctrl+C or other exit signals
    sched.shutdown()
    exit()
