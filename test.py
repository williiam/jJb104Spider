from tqdm import tqdm
import time

times = 0
progress = tqdm(total=1000)
while times < 1000:
    times += 100
    progress.update(times)
    time.sleep(1)
