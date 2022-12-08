from crontab import CronTab
import os

cwd = os.getcwd()
command_one = f'python3 {cwd}/crons/test1.py'
command_two = f'python3 {cwd}/crons/test2.py'

cron = CronTab(user=os.getlogin())

# for job in cron:
#         cron.remove(job)
#         cron.write()

job1 = cron.new(command=command_one)
job1.minute.every(2)

job2 = cron.new(command=command_two)
job2.minute.every(3)

cron.write()

os.system(command_two)
