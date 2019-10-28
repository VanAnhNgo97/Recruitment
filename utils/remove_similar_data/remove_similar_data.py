from pyvi import ViTokenizer
import re
from py_stringmatching.similarity_measure.soft_tfidf import SoftTfIdf
import math
from datetime import datetime
from dateutil.relativedelta import relativedelta


class DataReduction:
    def __init__(self, no_fields, Y, jaccard_measure=0.8, similarity_threshold=0.9):
        self.no_fields = no_fields
        self.jaccard_measure = jaccard_measure
        self.similarity_threshold = similarity_threshold
        self.size = len(Y)

        # Split Y into tokens and normalize
        self.Y_normalize = []
        for y in Y:
            y_split = []
            for i in range(no_fields):
                y_split.append(self.word_nomalize(self.word_split(y[i])))
            y_split.append(y[-2])
            y_split.append(y[-1])
            self.Y_normalize.append(y_split)
        # Build index
        self.Y_index = []
        self.Y_fields = [[] for i in range(no_fields)]
        for y in self.Y_normalize:
            for i in range(no_fields):
                self.Y_fields[i].append(y[i])
        for i in range(no_fields):
            self.Y_index.append(self.invert_index(self.Y_fields[i]))
        # Soft TF/IDF models
        self.soft_tf_idf = []
        for i in range(no_fields):
            self.soft_tf_idf.append(SoftTfIdf(self.Y_fields[i]))

    def is_match(self, x):
        # normalize x
        #x_normalize = [self.word_nomalize(self.word_split(x_)) for x_ in x]
        #vananh
        x_normalize = []
        for i in range(self.no_fields):
            x_normalize.append(self.word_nomalize(self.word_split(x[i])))
        x_normalize.append(x[-2])
        x_normalize.append(x[-1])
        '''
        print("x_normalize")
        print(x_normalize)
        print("length y normalize")
        print(len(self.Y_normalize))
        print("y normalize 0")
        print(self.Y_normalize[0])
        '''
        #

        # size filtering
        Y_size_filtering = self.size_filtering(x_normalize, self.Y_normalize)
        '''
        print("filtering")
        print(len(Y_size_filtering))
        '''
        # position filtering
        Y_candidates = self.position_filtering(x_normalize, Y_size_filtering)
        '''
        print("y candidates")
        print(len(Y_candidates))
        print("y_candidate 0")
        '''
        #print(Y_candidates[0])
        # check match
        flag = False  # flag check x match in Y
        for y in Y_candidates:
            inner_flag = True
            for i in range(self.no_fields):
                if self.soft_tf_idf[i].get_raw_score(x_normalize[i], y[i]) < self.similarity_threshold:
                    inner_flag = False
                    break
            #print(x_normalize[-1])
            #print(y[-1])
            #print("------------------------")
            #kiem tra truong ngay thang neu data bi trung
            if inner_flag:
                
                check_date_posted = self.is_over_range(x_normalize[-2],y[-2],1)
                check_valid_through = self.is_over_range(x_normalize[-1],y[-1],1)
                #vananh kiem tra truong ngay thang neu trung thi return luon
                
                if check_date_posted and check_valid_through:
                    flag = False
                else:
                    flag = True
                    break
        return flag
    #tach tu tieng viet
    @staticmethod
    def word_split(text):
        return re.compile("[\\w_]+").findall(ViTokenizer.tokenize(text))

    @staticmethod
    def word_nomalize(text):
        return [word.lower() for word in text]

    @staticmethod
    def invert_index(str_list):
        inverted = {}
        for i, s in enumerate(str_list):
            for word in s:
                locations = inverted.setdefault(word, [])
                locations.append(i)
        return inverted

    def size_filtering(self, x, Y):
        up_bound = [len(x_) / self.jaccard_measure for x_ in x[:-2]]
        '''
        print("up_bound")
        print(up_bound)
        '''
        down_bound = [len(x_) * self.jaccard_measure for x_ in x[:-2]]
        Y_size_filtering = []

        for y in Y:
            flag = True
            for i in range(self.no_fields):
                flag &= down_bound[i] <= len(y[i]) <= up_bound[i]
            if flag:
                Y_size_filtering.append(y)

        return Y_size_filtering

    def calc_prefix(self, x, y):
        k = math.ceil((self.jaccard_measure / (self.jaccard_measure + 1)) * (len(x) + len(y)))
        if len(x) >= k and len(y) >= k:
            return y, k
        return None

    def position_filtering(self, x, Y):
        # Calc an array of tuple (y, prefix) of Y
        Y_prefix = []
        ids = []
        for i, y in enumerate(Y):
            flag_choose = True
            prefix = []
            for j in range(self.no_fields):
                p = self.calc_prefix(x[j], y[j])
                prefix.append(p)
                if p is None:
                    flag_choose = False
            if flag_choose:
                Y_prefix.append(prefix)
                ids.append(i)

        # Calculate array of y' = y[len(y) - prefix_filtering + 1] sorted by frequency and min_prefix
        Y_ = []
        min_prefix = [10000 for i in range(self.no_fields)]
        for y in Y_prefix:
            y_ = []
            for i in range(self.no_fields):
                y_.append(self.sort_by_frequency(self.Y_index[i], y[i][0])[:len(y[i][0]) - y[i][1] + 1])
                if y[i][1] < min_prefix[i]:
                    min_prefix[i] = y[i][1]

            Y_.append(y_)

        # Build inverted index of y' (Y_)
        Y_index = []
        for i in range(self.no_fields):
            Y_index.append(self.invert_index([y[i] for y in Y_]))

        # Sort x by frequency
        x_ = []
        for i in range(self.no_fields):
            x_.append(self.sort_by_frequency(self.Y_index[i], x[i]))

        # Ids of y_ satisfied
        Y_filtered_id = []

        for i in range(self.no_fields):
            y_filter_id = []
            for x_i in x_[i][:len(x_[i]) - min_prefix[i] + 1]:
                id_match = Y_index[i].get(x_i)
                if id_match is not None:
                    y_filter_id += id_match
            Y_filtered_id.append(y_filter_id)

        # set of ids y_ satisfied
        Y_set_id = set(Y_filtered_id[0])
        for y_filter_id in Y_filtered_id[1:]:
            Y_set_id.intersection_update(y_filter_id)

        return [Y[ids[i]] for i in Y_set_id]

    def is_over_range(self,from_date,to_date,range_month):
        exact_from_date = from_date
        exact_to_date = to_date
        if from_date > to_date:
            exact_from_date = to_date
            exact_to_date = from_date 
        expire_date = exact_from_date + relativedelta(months=1)
        if exact_to_date >= expire_date:
            return True
        else:
            return False

    #vananh
    def add_job(self,filterd_job):
        self.size = self.size + 1
        y_split = []
        for i in range(self.no_fields):
            y_split.append(self.word_nomalize(self.word_split(filterd_job[i])))
            self.Y_fields[i].append(y_split[i])
            self.Y_index[i]=self.rebuild_invert_index(y_split[i],self.size-1,self.Y_index[i])
            self.soft_tf_idf[i] = SoftTfIdf(self.Y_fields[i])
        y_split.append(filterd_job[-2])
        y_split.append(filterd_job[-1])
        self.Y_normalize.append(y_split)
        
        

    def rebuild_invert_index(self,word_list,data_index,ini_invert_index):
        inverted = ini_invert_index
        for word in word_list:
            locations = inverted.setdefault(word, [])
            locations.append(data_index)
        return inverted


    @staticmethod
    def sort_by_frequency(inverted_index, arr):
        return sorted(arr,
                      key=lambda arr_i: len(inverted_index.get(arr_i) if inverted_index.get(arr_i) is not None else []))
