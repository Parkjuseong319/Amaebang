import json
import requests
import pandas as pd
import time
import retrying

df = pd.read_csv('C:/budongsan/budongsan_project/budongsan/firstapp/static/csv/apartment_saleinfo.csv')
# print(df.head(3))
# match_addr = df.loc[:,['지역구','lat', 'lng']]

df = df.drop('Unnamed: 0', axis=1)
df = df.dropna(axis=0)
df = df.sort_index(ascending=True)
df = df.reset_index(drop=True)



# 임시 파일 변환용. 나중에 주석처리해서 다시 데이터 재구성 할 것.
# match_addr = match_addr.loc[(match_addr['지역구']=="강남구") | (match_addr['지역구']=="강서구")]
# print(match_addr['지역구'].unique)
# match_addr = match_addr.dropna(axis=0)
# match_addr = match_addr.sort_index(ascending=True)
# match_addr = match_addr.reset_index(drop=True)
# print(len(match_addr))
# df = df.loc[(df['지역구']=="강남구") | (df['지역구']=="강서구")]
# print(df[:3])

# api_key = "7a6b8cc9d05c363b9a7856051e0d03f6"
api_key = 'f4f22e2382b7cc32bd051cd075350fca'

# def addr_to_lat_lon(addr):
#     url = 'https://dapi.kakao.com/v2/local/search/address.json?query={address}'.format(address=addr)
#     headers = {"Authorization": "KakaoAK " + api_key}
#     result = json.loads(str(requests.get(url, headers=headers).text))
#     match_first = result['documents'][0]['address']
#     return float(match_first['y']), float(match_first['x'])

# print(addr_to_lat_lon('강남구 역삼동'))

# 상세 주소 구하기
@retrying.retry(
    stop_max_attempt_number=30000,  # 최대 재시도 횟수
    wait_fixed=3000,  # 재시도 사이의 대기 시간 (밀리초 단위)
    retry_on_exception=lambda exc: isinstance(exc, requests.Timeout)  # 재시도할 예외 조건
)
def getaddress(lat, lng):
    url = 'https://dapi.kakao.com/v2/local/geo/coord2regioncode.json?x={x}&y={y}'.format(x=lng, y=lat)
    headers = {"Authorization": "KakaoAK " + api_key}
    result = json.loads(str(requests.get(url, headers=headers).text))
    address = result['documents'][0]["region_3depth_name"]
    return address

# print(getaddress(37.4953666908089, 127.03306536185), type(getaddress(37.4953666908089, 127.03306536185)))
try:
    count = 0
    data = []
    for i in range(len(df)):
        # print(df.iloc[i])
        # time.sleep()
        count +=1
        print(count)
        data.append(getaddress(df.loc[i,'lat'], df.loc[i,'lng']))

    df['동명'] = pd.Series(data=data) 

    df.to_csv('addr.csv')
   
except requests.Timeout:
    print('Timeout error occurred.')
except Exception as e:
    print(f'An error occurred: {str(e)}')