from service import Job104Spider, PyMongo
import datetime
import traceback
import re
from tqdm import tqdm
import json
import os
import pandas as pd

# 若環境變數沒有MONGO_URL,則import envSetting.py
try:
    os.environ['MONGO_URL']
except:
    import envSetting

db_driver = PyMongo.db_driver()
mongoClient = db_driver.connection

# TODO: 
# uer dotenv to load .env file to fix the [cant run in debug mode ] problem

# 設定檔
settings = {
# TODO: load DB and COLLECTION FROM .env
'DB':{
    'DB': 'job',
    'Collection': 'tSoftJob',
    'insert_batch_size': 2000,
},
'search_config' : {
    'keyWord': '',
    'max_mun': 100,
    'filter_params' : {
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
}
}

def get_job_data():
    """取得職缺資料"""
    search_config = settings['search_config']
    job104_spider = Job104Spider.Job104Spider()
    keyWord = search_config.get('keyWord')
    max_mun= search_config.get('max_mun')
    filter_params = search_config.get('filter_params')
    total_count,jobs = job104_spider.search(keyWord, max_mun=max_mun, 
    filter_params=filter_params)
    print('total_count: ', total_count)
    # TODO: 用公司ID爬公司資料(e.g. 資本額,)
    return jobs

def clean_job_data(jobs):
    def clean_job(job):
        result = job
        now = datetime.datetime.now()
        # 整理job, 1. 新增timestamp(從_id抓) 2. 字串轉數字 3. 去除不必要欄位
        result['jobType'] = int(job['jobType'])
        result['jobNo'] = int(job['jobNo'])
        result['jobRole'] = int(job['jobRole'])
        result['jobRo'] = int(job['jobRo'])
        result['period'] = int(job['period'])
        result['salaryLow'] = int(job['salaryLow'])
        result['salaryHigh'] = int(job['salaryHigh'])
        result['lon'] = float(job['lon'])
        result['lat'] = float(job['lon'])
        result['createdAt'] = now
        result['updatedAt'] = now
        # 若tags 內的emp desc欄位有值, 則將其轉成數字
        # print("job['tags']",job['tags'])
        # if (len(job['tags'])>0):
        #     if(job['tags']['emp']['desc']):
        #         numbers = re.findall(r'\d+', job['tags']['emp']['desc'])
        #         if(len(numbers)>0):
        #             result['emp'] = int(numbers[0])
        return result
    result = map(clean_job, jobs)
    return list(result)
    
# 存到檔案
def save_file_job_data(jobs):
    db_name= settings['DB']['DB']
    collection_name = settings['DB']['Collection']
    # Serializing json
    json_object = json.dumps(jobs, indent=4,default=str)
    # Writing to sample.json
    file_name = f'{db_name}_{collection_name}.json'
    # 若存入檔案失敗，則錯誤訊息
    with open(file_name, "w") as outfile:
        outfile.write(json_object)
        print(f'存到檔案: {file_name}')

# 寫入DB
def insert_db_job_data(jobs):
    db_name= settings['DB']['DB']
    collection_name = settings['DB']['Collection']
    """儲存職缺資料"""    
    db = mongoClient[db_name]
    collection = db[collection_name]
    insert_batch_size = settings['DB']['insert_batch_size']
    print("寫入資料庫中...")
    for i in tqdm(range(0, len(jobs), insert_batch_size)):
        last_index = i + insert_batch_size
        if(last_index>len(jobs)):
            last_index = len(jobs)
        collection.insert_many(jobs[i:last_index])

# 轉excel
def make_excel(jobs):
    try:
        df = pd.DataFrame(jobs)
        df.to_excel("softJob.xlsx", index=False)
    except Exception as e:
        print(e)


# TODO: VSCODE DEBUG 模式
if __name__ == "__main__":
    try:
        jobs = get_job_data()

        jobs = clean_job_data(jobs)

        save_file_job_data(jobs)

        insert_db_job_data(jobs)

        make_excel(jobs)
    except Exception as e:
        print(e)
        traceback.print_exc()
