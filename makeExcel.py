import pandas as pd
from service import PyMongo

db_driver = PyMongo.db_driver()
mongoClient = db_driver.connection

def get_job_data():
    """取得職缺資料"""
    # DB
    jobDB = mongoClient["job"]
    # Collection
    jobCol = jobDB["softJob"]
    find_option = {

    }
    # Find
    jobs = jobCol.find()
    return jobs

if __name__ == "__main__":
    try:
        # 爬softJob
        jobs = get_job_data()
        # 轉成DataFrame
        df = pd.DataFrame(jobs)
        # 儲存成Excel
        df.to_excel("softJob.xlsx", index=False)
    except Exception as e:
        print(e)
