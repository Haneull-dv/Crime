import googlemaps
from com.haneull.models.datareader import DataReader
from com.haneull.models.dataset import Dataset
import pandas as pd


class CrimeService:
    dataset = Dataset()
    datareader = DataReader()

    def new_model(self, fname) -> object:
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

    
    def preprocess(self, *args) -> object:
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
    def cctv_ratio(this) -> object:
        cctv = this.cctv
        this.cctv = this.cctv.drop(['2013년도 이전', '2014년', '2015년', '2016년'], axis = 1)
        print(f"📁CCTV 데이터프레임 헤드: {this.cctv.head()}")
        CrimeService.get_null_of_check(this.cctv)
        return this
    
    @staticmethod
    def crime_ratio(this) -> object:
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
        # gmaps = DataReader.create_gmaps()
        return this

    @staticmethod
    def pop_ratio(this) -> object:
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

