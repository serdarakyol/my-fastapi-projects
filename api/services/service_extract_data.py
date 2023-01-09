from shutil import copyfileobj 
from pandas import read_excel, DataFrame
from os import listdir, remove, mkdir
from os.path import isdir
from loguru import logger

class FileProcess:

    def __init__(self, files, root_dir) -> None:
        self.files = files
        self.data_store_path = f"{root_dir}/sabiduria_tool_api/data/"
        self.root_dir = root_dir
        self.final_data = {
            "Ad": [],
            "Soyad": [],
            "TC": [],
            "Matrah": [],
            "Brut": [],
            "Toplam": [],
            "OdenecekTutar": [],
            "DamgaVergisiKesintiToplami": [],
            "GelirVergisiKesintiToplami": [],
            "IstisnaEdilenGelirVergisiToplami": [],
            "GorevSayisi": [],
            "EnAzMatrahDosyasi": [],
            "GorevYerleri": []
        }

    async def save_files(self) -> None:
        if isdir(self.data_store_path):
            old_files = self.get_files()
            for o_file in old_files:
                remove(f"{self.data_store_path}{o_file}")
        else:
            mkdir(self.data_store_path)
        for file in self.files:
            with open(f"{self.data_store_path}{file.filename}", "wb") as destination:
                copyfileobj(file.file, destination)
    

    def get_files(self) -> list:
        all_files = listdir(f"{self.data_store_path}")
        return all_files

    def preprocess_files(self):
        all_files = self.get_files()
        for file in all_files:
            values = []
            selected_data = read_excel(f"{self.data_store_path}{file}", skiprows=9)
            del selected_data[selected_data.columns[0]]
            selected_data.rename(columns={'Unnamed: 17':'Kesintiler Toplamı'}, inplace=True)
            selected_data.rename(columns={'Unnamed: 18':'Ödenecek Tutar'}, inplace=True)
            for i, sira_no in enumerate(selected_data["Sıra No"]):
                if type(sira_no) != int:
                    break
                values.append(selected_data.iloc[[i]].values[0])
            temp_df = DataFrame(values, columns=selected_data.columns.values)
            logger.info(f"FILE SAVED TO: {self.data_store_path}{file}")
            temp_df.to_excel(f"{self.data_store_path}{file}", sheet_name="page1")

    def init_data(self):
        all_file = self.get_files()
        for file in all_file:
            file_data = read_excel(f"{self.data_store_path}{file}")
            file = file.split(".")[0]
            for i, tc in enumerate(file_data['Tc. No']):
                if tc not in self.final_data["TC"]:
                    self.final_data["TC"].append(tc)
                    self.final_data["Ad"].append(file_data["Adı"][i])
                    self.final_data["Soyad"].append(file_data["Soyadı"][i])
                    self.final_data["Matrah"].append(file_data["Aylık Vergi Matrahı  (Kümülatif)**"][i])
                    self.final_data["Brut"].append(file_data["Brüt Ücret ****"][i])
                    self.final_data["Toplam"].append(file_data["Aylık Vergi Matrahı  (Kümülatif)**"][i] + file_data["Brüt Ücret ****"][i])
                    self.final_data["OdenecekTutar"].append(file_data["Ödenecek Tutar"][i])
                    self.final_data["DamgaVergisiKesintiToplami"].append(file_data["Damga Vergisi Kesintisi"][i])
                    self.final_data["GelirVergisiKesintiToplami"].append(file_data["Gelir Vergisi Kesintisi"][i])
                    self.final_data["IstisnaEdilenGelirVergisiToplami"].append(file_data["İstisna Edilen Gelir Vergisi"][i])
                    self.final_data["GorevSayisi"].append(1)
                    self.final_data["GorevYerleri"].append(file + ", ")
                    self.final_data["EnAzMatrahDosyasi"].append(file)
                else:
                    id = self.final_data["TC"].index(tc)
                    if self.final_data["Matrah"][id] > file_data["Aylık Vergi Matrahı  (Kümülatif)**"][i]:
                        self.final_data["Matrah"][id] = file_data["Aylık Vergi Matrahı  (Kümülatif)**"][i]
                        self.final_data["EnAzMatrahDosyasi"][id] = file
                        self.final_data["Brut"][id] += file_data["Brüt Ücret ****"][i]
                        self.final_data["Toplam"][id] = file_data["Aylık Vergi Matrahı  (Kümülatif)**"][i] + file_data["Brüt Ücret ****"][i]
                        self.final_data["OdenecekTutar"][id] += file_data["Ödenecek Tutar"][i]
                        self.final_data["DamgaVergisiKesintiToplami"][id] += file_data["Damga Vergisi Kesintisi"][i]
                        self.final_data["GelirVergisiKesintiToplami"][id] += file_data["Gelir Vergisi Kesintisi"][i]
                        self.final_data["IstisnaEdilenGelirVergisiToplami"][id] += file_data["İstisna Edilen Gelir Vergisi"][i]
                        self.final_data["GorevSayisi"][id] += 1
                        self.final_data["GorevYerleri"][id] += file + ", "

    async def calculate(self):
        await self.save_files()
        self.preprocess_files()
        self.init_data()
        all_files = self.get_files()
        for file in all_files:
            file_data = read_excel(f"{self.data_store_path}{file}")
            file = file.split(".")[0]
            for i, tc in enumerate(file_data['Tc. No']):
                id = self.final_data["TC"].index(tc)
                if file != self.final_data["EnAzMatrahDosyasi"][id]:
                    self.final_data["Matrah"][id] += file_data["Brüt Ücret ****"][i]
                    self.final_data["Brut"][id] += file_data["Brüt Ücret ****"][i]
                    self.final_data["Toplam"][id] = self.final_data["Matrah"][id] + self.final_data["Brut"][id]
                    self.final_data["OdenecekTutar"][id] += file_data["Ödenecek Tutar"][i]
                    self.final_data["DamgaVergisiKesintiToplami"][id] += file_data["Damga Vergisi Kesintisi"][i]
                    self.final_data["GelirVergisiKesintiToplami"][id] += file_data["Gelir Vergisi Kesintisi"][i]
                    self.final_data["IstisnaEdilenGelirVergisiToplami"][id] += file_data["İstisna Edilen Gelir Vergisi"][i]
                    self.final_data["GorevSayisi"][id] += 1
                    self.final_data["GorevYerleri"][id] += file + ", "

        del all_files
        clean_data = DataFrame(self.final_data)
        del self.final_data
        clean_data.to_excel(f"{self.root_dir}/output.xlsx", sheet_name="page1")
