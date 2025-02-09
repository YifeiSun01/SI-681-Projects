import mrjob
import json
import csv
from mrjob.job import MRJob


class AverageRevenue(MRJob):
    OUTPUT_PROTOCOL = mrjob.protocol.TextProtocol
    def mapper(self, _, line):
        try:
            # line = line.encode(encoding = 'UTF-8', errors = 'ignore')
            line_list = list(csv.reader([line], delimiter=',', quotechar='"'))[0]
            genres = line_list[3]
            id =  line_list[5]
            original_language = line_list[7]
            title = line_list[20]
            release_date = line_list[14]
            spoken_languages = line_list[17]
            release_year = release_date[-4:]
            revenue = int(line_list[15])
            if genres != ""  and revenue != 0 and revenue != None and (release_year.startswith("19") or release_year.startswith("20")):
                genres_json_list = json.loads(genres.replace("'", '"'))
                for dictionary in genres_json_list:
                    genre = dictionary["name"]
                    yield (release_year,genre),(1,revenue)
        except:
            pass
    def combiner(self, key, values):
        counts = 0
        revenues = 0
        for value in values:
            counts += value[0]
            revenues += value[1]
        yield key, (counts,revenues)
    def reducer(self, key, values):
        counts = 0
        revenues = 0
        for value in values:
            counts += value[0]
            revenues += value[1]
        yield key[0]+"\t"+key[1], str(round((revenues/counts),2))
if __name__ == '__main__':
    AverageRevenue.run()