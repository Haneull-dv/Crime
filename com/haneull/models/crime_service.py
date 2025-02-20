from com.haneull.models.datareader import DataReader
from com.haneull.models.dataset import Dataset
import pandas as pd


class CrimeService:
    dataset = Dataset()
    datareader = DataReader()

    def new_model(self, fname) -> object:
        reader = self.datareader
        this = self.dataset
        print(f"Dataset 객체 확인: {this}") 
        return pd.read_csv(reader._context + fname)
    
    def preprocess(self, *args) -> object:
        print(f"------------모델 전처리 시작-----------")
        temp = []
        for i in list(args):
            print(f"📁 C파일 로드: {i}")
            temp.append(i)
        this = self.dataset
        this.cctv = self.new_model(temp[0])
        this.crime = self.new_model(temp[1])
        this.pop = self.new_model(temp[2])
        return this