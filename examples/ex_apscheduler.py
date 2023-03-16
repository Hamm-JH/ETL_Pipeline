from apscheduler.schedulers.blocking import BlockingScheduler

def job():
    print('Hello, world!')

if __name__ == '__main__':
    scheduler = BlockingScheduler()
    job_id = scheduler.add_job(job, 'interval', seconds=5)
    scheduler.start()
    # Abort the job after 10 seconds
    scheduler.remove_job(job_id) # 앞의 start() 함수에서 그 뒤로 코드가 동작하지 않는 문제 있음.