from service import Job104Spider, PyMongo

db_driver = PyMongo.db_driver()
mongoClient = db_driver.connection

def get_job_data():
    """取得職缺資料"""
    job104_spider = Job104Spider.Job104Spider()
    keyWord = ''
    max_mun= 100000
    filter_params = {
        # 'area': '6001001000,6001016000',  # (地區) 台北市,高雄市
        # 's10': '1,2,4,8',  # 這是什麼
        # 's9': '1,2,4,8',  # (上班時段) 日班,夜班,大夜班,假日班
        # 's5': '0',  # 0:不需輪班 256:輪班
        # 'wktm': '1',  # (休假制度) 週休二日
        # 'isnew': '0',  # (更新日期) 0:本日最新 3:三日內 7:一週內 14:兩週內 30:一個月內
        # 'jobexp': '1,3,5,10,99',  # (經歷要求) 1年以下,1-3年,3-5年,5-10年,10年以上
        # 'newZone': '1,2,3,4,5',  # (科技園區) 竹科,中科,南科,內湖,南港
        # 'zone': '16',  # (公司類型) 16:上市上櫃 5:外商一般 4:外商資訊
        # 'wf': '1,2,3,4,5,6,7,8,9,10',  # (福利制度) 年終獎金,三節獎金,員工旅遊,分紅配股,設施福利,休假福利,津貼/補助,彈性上下班,健康檢查,團體保險
        # 'edu': '1,2,3,4,5,6',  # (學歷要求) 高中職以下,高中職,專科,大學,碩士,博士
        # 'remoteWork': '1',  # (上班型態) 1:完全遠端 2:部分遠端
        # 'excludeJobKeyword': '科技',  # 排除關鍵字
        # 'kwop': '1',  # 只搜尋職務名稱
    }
    total_count,jobs = job104_spider.search(keyWord, max_mun=max_mun, filter_params=filter_params)
    return jobs

def save_job_data(jobs):
    """儲存職缺資料"""    
    # DB
    jobDB = mongoClient["job"]
    # Collection
    jobCol = jobDB["softJob"]
    # Insert
    jobCol.insert_many(jobs)


if __name__ == "__main__":
    try:
        # 爬softJob
        total_count,jobs = get_job_data()
        # 寫入DB
        save_job_data(jobs)
    except Exception as e:
        print(e)
