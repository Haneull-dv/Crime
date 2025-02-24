import os
from com.haneull.models.google_map_singleton import GoogleMapsClient
import googlemaps
from com.haneull.models.datareader import DataReader
from com.haneull.models.dataset import Dataset
import pandas as pd


class CrimeService:
    dataset = Dataset()
    datareader = DataReader()

    def new_model(self, fname) -> str:
        reader =  CrimeService.datareader
        reader = self.datareader
        this = self.dataset
        print(f"📁Dataset 객체 확인: {this}")
        reader.fname = fname
        if fname.endswith(".csv"):
            print(f"📁CSV 파일 로드: {reader.fname}")
            return reader.csv_to_dframe()
        elif fname.endswith(".xls") or reader.fname.endswith(".xlsx"):
            print(f"📁Excel 파일 로드: {reader.fname}")
            return reader.xls_to_dframe(header = 2, usecols = 'B,D,G,J,N')

    
    def preprocess(self, *args) -> pd.DataFrame:
        print(f"------------모델 전처리 시작-----------")
        temp = []
        for i in list(args):
            print(f"📁C파일 로드: {i}")
            temp.append(i)
        this = self.dataset
        this.cctv = self.new_model(temp[0])
        this = self.cctv_ratio(this)    

        this.crime = self.new_model(temp[1])
        this = self.crime_ratio(this)
        this.pop = self.new_model(temp[2])
        this = self.pop_ratio(this)
        return this
    
    @staticmethod
    def cctv_ratio(this) -> pd.DataFrame:
        cctv = this.cctv
        cctv = cctv.drop(['2013년도 이전', '2014년', '2015년', '2016년'], axis = 1)
        print(f"📁CCTV 데이터프레임 헤드: {cctv.head()}")
        CrimeService.get_null_of_check(cctv)
        return this
    
    @staticmethod
    def crime_ratio(this) -> pd.DataFrame:
        crime = this.crime
        print(f"📁Crime 데이터프레임 헤드: {crime.head()}")
        CrimeService.get_null_of_check(this.crime)
        station_names = [] #경찰서 관서명 리스트
        for name in crime['관서명']:
            station_names.append('서울' + str(name[:-1]) + '경찰서')
        print(f"👮경찰서 관서명 리스트: {station_names}")
        station_addrs = [] #경찰서 주소 리스트
        station_lats = [] #경찰서 위도 리스트
        station_lngs = [] #경찰서 경도 리스트
        gmaps_client = GoogleMapsClient().get_client()
        for name in station_names:
            tmp = gmaps_client.geocode(name, language='ko')
            print(f"""👮{name}의 검색 결과: {tmp[0].get("formatted_address")}""")
            station_addrs.append(tmp[0]['formatted_address'])
            tmp_loc = tmp[0].get("geometry")
            station_lats.append(tmp_loc['location']['lat'])
            station_lngs.append(tmp_loc['location']['lng'])
        print(f"🐣자치구 리스트: {station_addrs}")
        gu_names = []
        for addr in station_addrs:
            tmp = addr.split()
            tmp_gu = [gu for gu in tmp if gu[-1] == '구'][0]
            gu_names.append(tmp_gu)
        crime['자치구'] = gu_names
        [print("😎자치구 리스트 2: {gu_names}")]
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 현재 .py 파일 기준 디렉터리
        SAVE_DIR = os.path.join(BASE_DIR, '..', 'saved_data')  # 한 단계 상위로 올라가서 saved_data
        os.makedirs(SAVE_DIR, exist_ok=True)  # 폴더가 없으면 생성
        csv_file_path = os.path.join(SAVE_DIR, 'police_position.csv')
        crime.to_csv(csv_file_path)                          
        return this

    @staticmethod
    def mkdirs(folder_name: str) -> str:
        """📂 지정한 폴더가 없으면 생성하고 경로를 반환하는 함수"""
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 현재 .py 파일 기준 디렉터리
        SAVE_DIR = os.path.join(BASE_DIR, "..", folder_name)  # 한 단계 상위 경로에 폴더 생성
        os.makedirs(SAVE_DIR, exist_ok=True)  # 폴더가 없으면 생성
        print(f"📂 저장 폴더 생성됨: {SAVE_DIR}")
        return SAVE_DIR

    @staticmethod
    def pop_ratio(this) -> pd.DataFrame:
        pop = this.pop
        pop.rename(columns = {
            # pop.columns[0]: '자치구' #변경하지 않음
            pop.columns[1]: '인구수',
            pop.columns[2]: '한국인',
            pop.columns[3]: '외국인',
            pop.columns[4]: '고령자'}, inplace = True)
        print(f"📁Pop 데이터 헤드: {this.pop.head()}")
        CrimeService.get_null_of_check(this.pop)
        return this
    
    @staticmethod
    def get_null_of_check(df):
        null_count = df.isnull().sum().sum() 
        print(f"📁총 결측치 개수: {null_count}")

