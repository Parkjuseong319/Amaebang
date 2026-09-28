from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import pandas as pd
import pickle
import datetime
import numpy as np
from ast import literal_eval
import json

# 메인 페이지
def front(request):
    global model
    model=pickle.load(open('./app/static/csv/RanForRegmodel.h5', 'rb'))
    
    return render(request, 'front-page.html')

# 예상 가격
def predict(request):
    if request.method == 'GET':
        # 평수 1평 들어왔을때 제한 걸기.
        gu = request.GET['gu']+'구'
        dong = request.GET['dong']
        width = request.GET['width']
        # data = pd.read_csv('./app/static/csv/실시간매물.csv')
        # pickle.dump(data, open('실시간매물.h5', 'wb')) 
        
        #라벨링 csv read
        label_data = pd.read_csv('./app/static/csv/라벨링데이터.csv',encoding='utf-8',index_col=0)

        구라벨 = label_data[label_data['자치구'] == gu]['자치구'].index.values[0]
        동라벨 = label_data[label_data['법정동'] == dong]['법정동'].index.values[0]

        # temp_data = pd.read_csv('app/static/csv/실시간매물.csv', index_col=0)
        # temp_data=temp_data[['지역구', '동명', 'spc2', '한강최소거리']]
        temp_data = pickle.load(open('./app/static/csv/실시간매물.h5', 'rb'))
        temp_data = temp_data[['지역구','동명','spc2','한강최소거리']]
        print(temp_data)
        # 현재 날짜 가져오기
        today = datetime.datetime.now()
        today_date = today.strftime("%Y%m%d")
        print(today_date)
        # print(label_data)
        
        temp_data = temp_data[temp_data['지역구'] == gu]
        temp_data = temp_data[temp_data['동명'] == dong]   

        # 평수 범위 내 가격 평균
        width = int(width)
        min_width = width * 3.3 - 5 * 3.3
        max_width = width * 3.3 + 5 * 3.3
        temp_data = temp_data[(temp_data['spc2'] >= min_width) & (temp_data['spc2'] <= max_width)]
        
        temp_data.insert(0, '계약일', str(today_date))
        temp_data.insert(5, '물가지수 ', 111)
        temp_data.insert(6, '매매지수 ', 93.51)
        temp_data.insert(7, '금리', 3.50)
        
        temp_data['지역구']=temp_data['지역구'].replace(temp_data['지역구'].values, 구라벨)
        temp_data['동명']=temp_data['동명'].replace(temp_data['동명'].values, 동라벨)
        
        temp_data.columns = ['계약일','자치구명','법정동명','건물면적(㎡)', '한강공원최소거리', '물가지수', '매매지수', '금리']
        print(temp_data)
        print(len(temp_data))

        y_pred = model.predict(temp_data)
        y_pred = np.expm1(y_pred)
        
        predict_data = (y_pred.mean() / (temp_data['건물면적(㎡)'].mean() / 3.305785)) * int(width)
        
        select_boxes = {
            # 'mean_price':y_pred.mean().round(0),
            'mean_price':format(int(predict_data.round(0)), ','),
        }        
        # print(select_boxes)
    else:
        select_boxes = {}  # 빈 딕셔너리 할당
    return JsonResponse(select_boxes, safe=False)


# 추천 매물
# 지도상에 좌표를 찍어줘야함. 
def recommand(request):
    if request.method == 'GET':
        select_boxes = {
            'gu':request.GET['gu'],
            'dong':request.GET['dong'],
            'width':request.GET['width'],
        }
    else:
        select_boxes = {}  # 빈 딕셔너리 할당
        
    # print(select_boxes['gu'])
    gu = select_boxes['gu'] + '구'
    dong = select_boxes['dong']

    # 평수를 구하기 위해 width를 정수로 변환
    width = int(select_boxes['width'])
    min_width = (width * 3.3) - (5 * 3.3)
    max_width = (width * 3.3) + (5 * 3.3)
    
    # df = pd.read_csv('app/static/csv/sale_addr.csv', index_col=0)
    # df = pickle.load(open('./app/static/csv/temp_data.h5', 'rb'))
    df = pickle.load(open('./app/static/csv/실시간매물.h5', 'rb'))
    df = df[df['지역구'] == gu]
    df = df[df['동명'] == dong]

    # 여기서 범위에 맞는 아파트 width 필터링
    df_data = df[(df['spc2'] >= min_width) & (df['spc2'] <= max_width)]

    # print(df.iloc[0])
    # if len(df_data) == 0:
    #     df_data = df.iloc[0]
    
    # print(len(df))
    json_data =[]
    for i in range(len(df_data)):
        address = gu +' ' + dong + ' ' + df_data['bildNm'].iloc[i]
        json_data.append({"title": df_data['atclNm'].iloc[i], "price": df_data['hanPrc'].iloc[i], "desc": df_data["tagList"].str[1:-1].iloc[i], "location": address, 'lat':df_data['lat'].iloc[i], 'lng': df_data['lng'].iloc[i], 'spec':df_data['spc2'].iloc[i]//3.3 })
    
    # print(json_data[:1])
    return JsonResponse(json_data, safe=False)

def convenient_marker(request):
    if request.method == 'GET':
        select_boxes = {
            'lat': request.GET.get('lat'),
            'lng': request.GET.get('lng'),
        }
        
    else:
        select_boxes = {}  # 빈 딕셔너리 할당
    헬스 = request.GET.get('health')
    백화점 = request.GET.get('mart')
    스벅 = request.GET.get('starbucks')
   
    print(헬스)
    print(백화점)
    print(스벅)
    
    print(select_boxes['lat'], select_boxes['lng'])
    lat = float(select_boxes['lat'])
    lng = float(select_boxes['lng'])
    df = pickle.load(open('./app/static/csv/실시간매물.h5', 'rb'))

    df = df[df['lat']==lat]
    df = df[df['lng']==lng]


    df["체육시설"] = df["체육시설"].apply(literal_eval)
    df["스타벅스"] = df["스타벅스"].apply(literal_eval)
    df["백화점/대형마트"] = df["백화점/대형마트"].apply(literal_eval)

    health = {}
    star = {}
    mart = {}
    for i in range(5):
        if f'이름{i}' in df["체육시설"].iloc[0]["사업장명"]:
            health[f"체육시설{i}"] = {"이름": df["체육시설"].iloc[0]["사업장명"][f'이름{i}'],
                                '주소': df["체육시설"].iloc[0]["주소"][f'주소{i}'],
                                '위도': df["체육시설"].iloc[0]["위도"][f'위도{i}'],
                                '경도': df["체육시설"].iloc[0]["경도"][f'경도{i}']}
            
        if f'이름{i}' in df["스타벅스"].iloc[0]["사업장명"]:
            star[f"스타벅스{i}"] = {"이름": df["스타벅스"].iloc[0]["사업장명"][f'이름{i}'],
                                '주소': df["스타벅스"].iloc[0]["주소"][f'주소{i}'],
                                '위도': df["스타벅스"].iloc[0]["위도"][f'위도{i}'],
                                '경도': df["스타벅스"].iloc[0]["경도"][f'경도{i}']}
        if f'이름{i}' in df["백화점/대형마트"].iloc[0]["사업장명"]:
            mart[f"백화점/대형마트{i}"] = {"이름": df["백화점/대형마트"].iloc[0]["사업장명"][f'이름{i}'],
                                    '주소': df["백화점/대형마트"].iloc[0]["주소"][f'주소{i}'],
                                    '위도': df["백화점/대형마트"].iloc[0]["위도"][f'위도{i}'],
                                    '경도': df["백화점/대형마트"].iloc[0]["경도"][f'경도{i}']}

    json_data = []
    json_data.append({
        'lat': lat, 'lng': lng,
        'health': health, 'starbucks': star, 'mart': mart
    })
    json_data = json.dumps(json_data, ensure_ascii=False)
    data = json.loads(json_data)

    addr = df['지역구'].iloc[0] + df['동명'].iloc[0] + df['bildNm'].iloc[0]
    js_data = []
    js_data.append({
        'addr': addr, 'name': df['atclNm'].iloc[0],
        'spec': df['spc2'].iloc[0]//3.3 , 'price':df['hanPrc'].iloc[0]
    })
    print(addr, js_data[0]['name'])


    js_data = json.dumps(js_data, ensure_ascii=False)
    meamul = json.loads(js_data)
    print(meamul)
    # print(data)
    health_data = []
    health_addr = []
    health_lat = []
    health_lon = []
    
    mart_data = []
    mart_addr = []
    mart_lat = []
    mart_lon = []
    
    starbucks_data = []
    starbucks_addr = []
    starbucks_lat = []
    starbucks_lon = []
    for i in range(len(data[0])):
        if 헬스:
            health_data.append(data[0]['health'][f'체육시설{i}']['이름'])
            health_addr.append(data[0]['health'][f'체육시설{i}']['주소'])
            health_lat.append(data[0]['health'][f'체육시설{i}']['위도'])
            health_lon.append(data[0]['health'][f'체육시설{i}']['경도'])

        if 백화점:
            mart_data.append(data[0]['mart'][f'백화점/대형마트{i}']['이름'])
            mart_addr.append(data[0]['mart'][f'백화점/대형마트{i}']['주소'])
            mart_lat.append(data[0]['mart'][f'백화점/대형마트{i}']['위도'])
            mart_lon.append(data[0]['mart'][f'백화점/대형마트{i}']['경도'])

        if 스벅:
            starbucks_data.append(data[0]['starbucks'][f'스타벅스{i}']['이름'])
            starbucks_addr.append(data[0]['starbucks'][f'스타벅스{i}']['주소'])
            starbucks_lat.append(data[0]['starbucks'][f'스타벅스{i}']['위도'])
            starbucks_lon.append(data[0]['starbucks'][f'스타벅스{i}']['경도'])
    
    # print(health_data)
    # atclNm,tradTpNm,flrInfo,prc,hanPrc,spc1,spc2,lat,lng,tagList,지역구,bildNm
    
    co_data = [[lat, lng],
        health_data, health_addr, health_lat, health_lon,mart_data, mart_addr, mart_lat, mart_lon,
        starbucks_data, starbucks_addr, starbucks_lat, starbucks_lon, meamul[0] 
    ]

    print(co_data)
    return JsonResponse(co_data, safe=False)


# 통계 출력
def chart(request):
    if request.method == 'GET':
        gu = request.GET['gu']+'구'
    cctv_df=pd.read_csv('./app/static/csv/pre_cctv_data.csv',index_col=0)
    cctv_data=cctv_df[gu][:-1].values
    lamp_df=pd.read_csv('./app/static/csv/pre_lamp_data.csv',index_col=0)
    lamp_data=lamp_df[gu][:-1].values
    criminal_df=pd.read_csv('./app/static/csv/pre_criminal_data.csv',index_col=0)
    criminal_data=criminal_df[gu].values
    # child_df=pd.read_csv('./app/static/csv/.csv',index_col=0)
    # child_all=child_df[0:]
    # child_data=child_df[gu].values

    # 지역구 연도별 평균 매매가
    hprice= pd.read_csv('./app/static/csv/최종_매매데이터_전처리자료_한강공원.csv')
    hprice = hprice[hprice['자치구명'] == gu]
    hprice=hprice[['계약일', '물건금액(만원)']]
    hprice['계약일'] = hprice['계약일'].astype(str).str[:4]
    apartchart = hprice.groupby('계약일')['물건금액(만원)'].mean()
    # print(apartchart)

    chartdata={
        'cctv':list(cctv_data),
        'lamp':list(lamp_data),
        'criminal':list(criminal_data),
        'hprice':list(apartchart)
    }
    print(chartdata)
    return render(request, 'chart-page.html', chartdata)

# 조건 데이터 리셋
def resetdata(request):
    rdata = {
        "initialGuValue": "",
        "initialDongOptions": "<option value=''>동명</option>", 
        "initialWidthValue": 6,
        "initialPredictPrice": ""
    }
    return JsonResponse(rdata, safe=False)

# Create your views here.
def main(request):
    return render(request, 'index.html')