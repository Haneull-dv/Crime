from dataclasses import dataclass
import pandas as pd

@dataclass
class Dataset:
    cctv : pd.DataFrame
    crime : pd.DataFrame
    pop : pd.DataFrame

    @property
    def cctv(self) -> pd.DataFrame:
        return self._cctv
    @cctv.setter
    def cctv(self,cctv):
        self._cctv = cctv

    @property
    def crime(self) -> pd.DataFrame:
        return self._crime
    @crime.setter
    def crime(self,crime):
        self._crime = crime
        
    @property
    def pop(self) -> pd.DataFrame:
        return self._pop
    @pop.setter
    def pop(self,pop):
        self._pop = pop






