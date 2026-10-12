import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import LabelEncoder
import seaborn as sns
import numpy as np
plt.rcParams["axes.unicode_minus"]=False

#아파트 평균단가==========================================
#아파트 평균단가==========================================
#아파트 평균단가==========================================
#아파트 평균단가==========================================
plt.rc('font', family='malgun gothic')

path = "C:\\Users\\hsung\\OneDrive\\바탕 화면\\chart\\최종_매매데이터_전처리자료_한강공원.csv"
data = pd.read_csv(path, encoding='utf-8', index_col=0)

gu_input = "강남구"

data = data[data['자치구명'] == gu_input]
data['계약일'] = data['계약일'].astype(str).str[:4]
아파트차트 = data.groupby('계약일')['물건금액(만원)']

plt.figure(figsize=(8, 6))
plt.plot(list(아파트차트.groups.keys()), 아파트차트.mean())
plt.xticks(list(아파트차트.groups.keys()))
plt.xlabel("매매 연도")
plt.ylabel("월별 평균 전세(만원)")
plt.title("{} 물건금액(만원) 평균".format(gu_input))
plt.tight_layout()
plt.show()

#=============================상관관계 ====================================
#라벨링
data = data[(data['건물면적(㎡)'] < 300)]
le = LabelEncoder()
data['자치구명'] = le.fit_transform(data['자치구명'])
자치구명 = le.classes_
data['법정동명'] = le.fit_transform(data['법정동명'])
법정동명 = le.classes_
data['학교종류명'] = le.fit_transform(data['학교종류명'])
학교종류명 = le.classes_



print(data['건물면적(㎡)'][:100])
# 독립 변수
x_data = data[['계약일','자치구명', '법정동명','층', '건물면적(㎡)','한강공원포함개수(1km)','한강공원최소거리','학교종류명', '학교포함개수(1km)', '학교최소거리', '지하철포함개수(0.5km)', '지하철포함개수(1km)', '지하철최소거리']]

# 종속 변수 (보증금)
y_data = data['물건금액(만원)']

# 상관 관계 분석을 위한 데이터셋
correlation_data = data[['계약일', '건물면적(㎡)','한강공원포함개수(1km)','한강공원최소거리', '학교포함개수(1km)', '지하철포함개수(0.5km)', '지하철포함개수(1km)', '지하철최소거리','물건금액(만원)']]
correlation_matrix = correlation_data.corr()

# 히트맵 시각화
plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
plt.title('Correlation Matrix')
plt.tight_layout()
plt.show()

#CCTV 가로등==========================================
#CCTV 가로등==========================================
#CCTV 가로등==========================================
#CCTV 가로등==========================================
#CCTV 가로등==========================================

# ==============================================================================
# 연도별 / 지역별 방범용 "CCTV" 운영 현황 데이터 
# ==============================================================================

# 데이터 읽기
cctv_data=pd.read_csv('C:\\Users\\hsung\\OneDrive\\바탕 화면\\chart\\CCTV.csv', encoding='cp949')

# 2021, 2022 년 제외 년도의 데이터에서 ',' 없애기
cctv_data.iloc[:, :7] = cctv_data.iloc[:, :7].apply(lambda x: x.str.replace(',', ''))

# column에서 '년' 글자 제거
cctv_data.columns=cctv_data.columns.str.replace('년', '')
cctv_data=cctv_data.T       # 연도를 index 로 사용
cctv_data.columns=cctv_data.iloc[0]     # 지역을 column 명으로 사용
cctv_data=cctv_data.iloc[1:]       # 지역의 정보가 담긴 1번째 행을 제외

# 2018년 이후 데이터만 담기 (2018 ~ 2022)
cctv_data=cctv_data.loc['2018':]
# print(cctv_data.head(5))


# ==============================================================================
# 연도별 / 지역별 5대 "범죄 발생" 현황 데이터 
# ==============================================================================

# 데이터 읽기 : 범죄 발생 건수 ... '년도' 열의 
criminal_data=pd.read_csv('C:\\Users\\hsung\\OneDrive\\바탕 화면\\chart\\criminal.csv')
print(criminal_data.head(5), criminal_data.info())

# 지역별 / 연도별 전체 범죄 발생 건구 데이터만 남기기
criminal_data=criminal_data[['자치구별(2)', '2018', '2019', '2020', '2021']]
criminal_data=criminal_data[4:]

# 년도를 index로 지정 : transpose 이용
criminal_data=criminal_data.T
criminal_data.columns=criminal_data.iloc[0]
criminal_data=criminal_data.drop(criminal_data.index[0])


# ==============================================================================
# 연도별 / 지역별 가로등 개수 데이터 
# ==============================================================================

# 데이터 읽기
lamp_data=pd.read_csv('C:\\Users\\hsung\\OneDrive\\바탕 화면\\chart\\streetLamp.csv')

# 가로등 / 개수 / 소계를 알려주는 행 삭제 & 합계가 써져있는 열 삭제
lamp_data=lamp_data.iloc[3:, 1:]

# 년도를 index로 지정 : transpose 이용
lamp_data=lamp_data.T
lamp_data.columns=lamp_data.iloc[0]
lamp_data=lamp_data.drop(lamp_data.index[0])

###################################################################
### 년도별 cctv, 가로등, 범죄건수 데이터 튜플 형태로 저장 
###################################################################

total_data={}
for region in cctv_data.columns:
    total_data[region]={}
    for categori in (['cctv', 'lamp', 'criminal']):
        total_data[region][categori]={}
        for year in criminal_data.index:
            total_data[region][categori][year]=(cctv_data.loc[year, region] if categori=='cctv' else(lamp_data.loc[year, region] if categori=='lamp' else criminal_data.loc[year, region]))
  

###################################################################
# 그래프 - 시각화
###################################################################

# 지역을 선택하면 지역별 cctv / 가로등 / 범죄건수 그래프 출력


select_data=pd.DataFrame(total_data[gu_input].values(), index=total_data[gu_input].keys())
print(select_data)
print(select_data.info())
select_data=select_data.astype(int)
print(select_data.info())
print(select_data.values)

# 그래프 그리기 - y축 양쪽 사용
fig, ax1=plt.subplots(figsize=(7, 7))
ax1.set_title('CCTV, 가로등 운영대수와 범죄 발생 건수', pad=20)
ax1.plot(select_data.columns, select_data.loc['cctv'], 'g.-', alpha=0.5, label='CCTV') 
ax1.plot(select_data.columns, select_data.loc['criminal'], 'r.-', alpha=0.5, label='범죄건수') 
ax1.set_ylabel('CCTV, 범죄', color='grey')

ax2=ax1.twinx()
ax2.plot(select_data.columns, select_data.loc['lamp'], 'b.-', alpha=0.5, label='가로등')
ax2.set_ylabel('가로등', color='grey')
ax2.set_ylim(4000, 15000)  
# fig.legend(fontsize=7, loc='upper right', bbox_to_anchor=(1.0, 1.01)) # 범례 위치: 왼쪽 위
fig.legend(fontsize=7, loc='lower right', bbox_to_anchor=(0.9, 0.13))   # 범례 위치: 오른쪽 아래

plt.show()


###################################################################
# 상관관계 분석
###################################################################

select_data=select_data.T
print(select_data)
print(select_data.corr())
# ∴ cctv 대수가 많아질수록 범죄 발생 건수는 줄어듦 
# => 안전한 곳을 원한다면 cctv 대수가 많은 지역을 추천할 수 있음

# 상관관계 시각화
colormap = plt.cm.PuBu
plt.figure(figsize=(7, 7))
plt.title("cctv, 가로등, 범죄건수 간의 상관관계", y = 1.05, size = 15)
sns.heatmap(select_data.corr(), linewidths = 0.1, vmax = 1.0,
           square = True, cmap = colormap, linecolor = "white", annot = True, annot_kws = {"size" : 16})
plt.show()

#어린이 보호구역==========================================
#어린이 보호구역==========================================
#어린이 보호구역==========================================
#어린이 보호구역==========================================
#어린이 보호구역==========================================

# 어린이보호구역내 어린이 교통사고 발생건수 / 어린이 교통사고 발생수 구별로 분석
# (어린이보호구역, 어린이 교통사고 비율을 파이 차트로 시각화) - 헤드 10개 

df = pd.read_csv("C:\\Users\\hsung\\OneDrive\\바탕 화면\\chart\\교통사고.csv", header=[0, 1])

# 사망자수와 부상자수가 들어있는 열 삭제 (사고 인원수가 아닌 사고 비율을 보려고 전체 사고수로 계산함)
df = df.drop(columns=[('2018', '사망자수 (명)'), ('2018', '부상자수 (명)'), ('2019', '사망자수 (명)'), ('2019', '부상자수 (명)'), ('2020', '사망자수 (명)'), ('2020', '부상자수 (명)'), ('2021', '사망자수 (명)'), ('2021', '부상자수 (명)')])

# 첫 번째 행, 두 번째 행의 칼럼 이름 결합 
new_columns = [col[0] if col[0] == col[1] else f"{col[0]}_{col[1]}" for col in df.columns]

# 결합된 칼럼 이름으로 반영
df.columns = new_columns
# print(df)

# 어린이 교통사고와 어린이보호구역 내 어린이 교통사고 데이터만 선택
child_accidents = df[df["사고현황별(1)"] == "어린이 교통사고"].copy()
child_accidents_in_protection_zone = df[df["사고현황별(1)"] == "어린이보호구역내 어린이 교통사고"].copy()

# '-' 문자를 NaN으로 변환
child_accidents_in_protection_zone.replace('-', np.nan, inplace=True)
child_accidents.replace('-', np.nan, inplace=True)

# 구별 어린이 교통사고 발생건수와 어린이보호구역 내 어린이 교통사고 발생건수의 비율 계산
for idx, row in child_accidents_in_protection_zone.iterrows():
    for year in ["2018", "2019", "2020", "2021"]:
        total_accidents_col = f"{year}_발생건수 (건)"
        #해당 연도의 전체 어린이 교통사고 발생건수 열 이름 저장
        accidents_in_protection_zone = child_accidents_in_protection_zone.loc[idx, total_accidents_col]
        # 해당 행의 어린이보호구역 내 어린이 교통사고 값을 저장
        total_accidents = child_accidents.loc[child_accidents["자치구별(2)"] == row["자치구별(2)"], total_accidents_col].values[0]
        # "자치구별(2)"]에서 가져오고, 동일한 구에 해당하는 전체 어린이 교통사고 발생건수 값을 저장합니다.
        if pd.isna(accidents_in_protection_zone) or pd.isna(total_accidents):
            ratio = np.nan
            # 값이 결측치 (NaN)인 경우, 비율인 ratio를 NaN으로 설정합니다.
        else:
            ratio = float(accidents_in_protection_zone) / float(total_accidents)
# 결측치가 아닌 경우, ratio를 accidents_in_protection_zone를 total_accidents로 나눈 값으로 .

        child_accidents_in_protection_zone.loc[idx, "ratio_" + year] = ratio

# 결과 출력
print(child_accidents_in_protection_zone)

plt.figure(figsize=(12, 8))
plt.title("어린이보호구역과 어린이 교통사고 비율", fontsize=15)

for year_idx, year in enumerate(["2018", "2019", "2020", "2021"]):
    
    
    df_ratio = child_accidents_in_protection_zone[['자치구별(2)', f'ratio_{year}']].dropna()
    df_ratio = df_ratio.sort_values(by=f'ratio_{year}', ascending=False).reset_index(drop=True)
    df_ratio = df_ratio.head(10)
    
    # 원형그래프
    ax = plt.subplot(2, 2, year_idx+1)
    ax.pie(df_ratio[f"ratio_{year}"], labels=df_ratio["자치구별(2)"], autopct='%1.1f%%')
    ax.set_title(f"{year}", fontsize=12)

plt.tight_layout()
plt.show()

