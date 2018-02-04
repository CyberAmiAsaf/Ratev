import json
import requests
import os
import isodate
from collections import Counter

#CONST
WEIGHT_FOR_VIDEOS_AFTER_WATCHING = 40
WEIGHT_FOR_VIDEO_TIME_WATCH = 50
WEIGHT_FOR_LIKE = 10


def enter_to_dictionary_the_tags_for_the_topic(topic_or_topics, dict_of_topics_and_rated_tags, video_tags_and_rate, total_rate):
    #   Input:
    #   Output:  a dictionary with rate and tags for it
    #   example: topic:{'rate_for_topic':Sport, tags:[['funny moments',86],[['goals','crazy'],86]]}
    if type(topic_or_topics) is list:
        for topic in topic_or_topics:
            if topic in dict_of_topics_and_rated_tags:
                #tags list with rate
                dict_of_topics_and_rated_tags[topic]["tags"].append(video_tags_and_rate)
                #rate sum
                if "rate_for_topic" in dict_of_topics_and_rated_tags[topic]:

                    rate_now = dict_of_topics_and_rated_tags[topic]["rate_for_topic"]
                    dict_of_topics_and_rated_tags[topic]["rate_for_topic"] = total_rate + rate_now
                else:
                    dict_of_topics_and_rated_tags[topic]["rate_for_topic"] = total_rate
            else:
                #tags list with rate
                dict_of_topics_and_rated_tags[topic] = {}
                dict_of_topics_and_rated_tags[topic]["tags"] = []
                dict_of_topics_and_rated_tags[topic]["tags"].append(video_tags_and_rate)

                #rate sum
                if "rate_for_topic" in dict_of_topics_and_rated_tags[topic]:
                    rate_now = dict_of_topics_and_rated_tags[topic]["rate_for_topic"]
                    dict_of_topics_and_rated_tags[topic]["rate_for_topic"] = total_rate + rate_now
                else:
                    dict_of_topics_and_rated_tags[topic]["rate_for_topic"] = total_rate
    else:
        if topic_or_topics in dict_of_topics_and_rated_tags:
            #tags list with rate
            dict_of_topics_and_rated_tags[topic_or_topics]["tags"].append(video_tags_and_rate)

            #rate sum
            if "rate_for_topic" in dict_of_topics_and_rated_tags[topic_or_topics]:
                rate_now = dict_of_topics_and_rated_tags[topic_or_topics]["rate_for_topic"]
                dict_of_topics_and_rated_tags[topic_or_topics]["rate_for_topic"] = rate_now + total_rate
            else:
                dict_of_topics_and_rated_tags[topic_or_topics]["rate_for_topic"] = total_rate

        else:
            dict_of_topics_and_rated_tags[topic_or_topics] = {}
            dict_of_topics_and_rated_tags[topic_or_topics]["tags"] = []
            dict_of_topics_and_rated_tags[topic_or_topics]["tags"].append(video_tags_and_rate)

            if "rate_for_topic" in dict_of_topics_and_rated_tags:
                rate_now = dict_of_topics_and_rated_tags[topic_or_topics]["rate_for_topic"]
                dict_of_topics_and_rated_tags[topic_or_topics]["rate_for_topic"] = rate_now + total_rate
            else:
                dict_of_topics_and_rated_tags[topic_or_topics]["rate_for_topic"] = total_rate
    #return dict_of_topics_and_rated_tags


def video_count_now(json_data):
    #Input: data from the json file
    #Output: the serial number of the next video
    list_of_dicts = json_data["Videos info"]
    count_list = []
    for dict in list_of_dicts:
        count_list.append(dict["video_count"])
    count_now = max(count_list)
    return count_now


def most_common_items_by_appearing_and_rate(list_of_items_list_and_rate):
    #Input: list of list items with rate
    #Output: items sorted by rate and appearing

    list_of_item_of_the_video = []
    for video_info in list_of_items_list_and_rate:
        list_of_item_of_the_video.append(video_info[0])
    d = Counter()
    for items_list_and_rate in list_of_items_list_and_rate:
        items_list=items_list_and_rate[0]
        rate_for_items_list=items_list_and_rate[1]
        if type(items_list) is list:
            for item in items_list:
                d[item] = d[item] + rate_for_items_list
        else:
            d[items_list] = d[items_list] + rate_for_items_list
    return d.most_common()


def enter_channels_by_rate_and_appearing_to_json_file(header_of_the_json_info, data, items_by_rate_and_appearing):
    #Input:the header of the json file, data of the json, the list of items sorted by rate.
    #      The name of the key in the dictionary to put the the items.
    #Outpt:-
    #Enter the items sorted by rate and appearing in the json file
    with open(header_of_the_json_info, 'w') as outfile:
        data["items_by_rate_and_appearing"]["list_of_all_channels_ids_and_rate"] = items_by_rate_and_appearing

        json.dump(data, outfile)
        outfile.close()

def enter_tags_by_topic_rate_and_appearing_to_json_file(header_of_the_json_info, data, items_by_rate_and_appearing, tag_id, rate_for_topic):
    #Input:the header of the json file, data of the json, the list of items sorted by rate.
    #      The name of the key in the dictionary to put the the items.
    #Outpt:-
    #Enter the items sorted by rate and appearing in the json file
    with open(header_of_the_json_info, 'w') as outfile:

        data["items_by_rate_and_appearing"]["tags_by_topic"][str(tag_id)] = {}
        data["items_by_rate_and_appearing"]["tags_by_topic"][str(tag_id)]["rate_for_topic"] = rate_for_topic
        data["items_by_rate_and_appearing"]["tags_by_topic"][str(tag_id)]["tags_for_the_topic"] = items_by_rate_and_appearing
        json.dump(data, outfile)
        outfile.close()


class UserInfo:

    def __init__(self, header_of_the_json_info):
        #Input: header of the json info
        #Output: -
        #The function create the User info object with the attributes: data in the json user info file,
        #the average time watched, sorted list of tags by rate and appearing,
        #sorted list of channels by rate and appearing and
        #sorted list of topics ids by rate and appearing.

        self.header_of_the_json_info = header_of_the_json_info
        with open(self.header_of_the_json_info) as data_file:
            data = json.load(data_file)
            data_file.close()
        self.data = data

        #Refreshtags_by_topic
        dict = self.data
        list_of_dicts = dict["Videos info"]
        dict_of_topics_and_rated_tags={}
        list_of_tags_list_total_rate = []
        list_of_all_chanels_ids_and_rate = []
        list_of_all_topics_ids_list_and_rate=[]
        count_for_time_watched = 0
        sum_of_times_watched = 0
        for dict in list_of_dicts:
            if dict["video_id"] != "":  # Checking if it is not the Null video

                time_watched = dict["time_watched"]
                sum_of_times_watched = sum_of_times_watched+time_watched
                count_for_time_watched = count_for_time_watched+1

                #this part of code give a count rate to videos.
                #count rate is bigger when the video is closer to the last video.
                count_now=video_count_now(self.data)
                video_count = dict['video_count']
                delta_count = count_now-video_count
                if delta_count <= WEIGHT_FOR_VIDEOS_AFTER_WATCHING:
                    count_rate = WEIGHT_FOR_VIDEOS_AFTER_WATCHING-delta_count
                else:
                    count_rate = 0
                total_rate = float(dict["video_rate"])+float(count_rate)

                # Tags list
                video_tags_and_rate = []
                video_tags_and_rate.append(dict["tags_list"])
                video_tags_and_rate.append(total_rate)
                list_of_tags_list_total_rate.append(video_tags_and_rate)


                # ChannelId list
                chanel_id_and_rate = []
                chanel_id_and_rate.append(dict["channelId"])
                chanel_id_and_rate.append(total_rate)
                list_of_all_chanels_ids_and_rate.append(chanel_id_and_rate)


                # Topics ids list list
                video_topics_ids_list_and_rate=[]
                video_topics_ids_list_and_rate.append(dict["topics_ids_list"])
                video_topics_ids_list_and_rate.append(total_rate)
                list_of_all_topics_ids_list_and_rate.append(video_topics_ids_list_and_rate)
                if dict["topics_ids_list"] != "no_topic":
                    enter_to_dictionary_the_tags_for_the_topic(dict["topics_ids_list"],dict_of_topics_and_rated_tags,video_tags_and_rate,total_rate)
                else:
                    enter_to_dictionary_the_tags_for_the_topic("no_topic",dict_of_topics_and_rated_tags,video_tags_and_rate,total_rate)


        for topic in dict_of_topics_and_rated_tags:

            rate_for_topic = dict_of_topics_and_rated_tags[topic]["rate_for_topic"]
            sorted_tags_by_rate_and_appearing_for_the_topic = most_common_items_by_appearing_and_rate(dict_of_topics_and_rated_tags[topic]["tags"])

            enter_tags_by_topic_rate_and_appearing_to_json_file(self.header_of_the_json_info, self.data, sorted_tags_by_rate_and_appearing_for_the_topic,str(topic),str(rate_for_topic))

        self.sorted_list_of_channels_by_rate_and_appearing = most_common_items_by_appearing_and_rate(list_of_all_chanels_ids_and_rate)
        self.sorted_list_of_topics_ids_by_rate_and_appearing = most_common_items_by_appearing_and_rate(list_of_all_topics_ids_list_and_rate)
        enter_channels_by_rate_and_appearing_to_json_file(self.header_of_the_json_info, self.data, self.sorted_list_of_channels_by_rate_and_appearing)

        self.average_time_watched = sum_of_times_watched/float(count_for_time_watched)

        sorted_dicts_of_tags_by_sorted_topics = []

        for topic_with_rate in self.sorted_list_of_topics_ids_by_rate_and_appearing:
            topic = topic_with_rate[0]

            rate_for_topic = self.data["items_by_rate_and_appearing"]["tags_by_topic"][str(topic)]["rate_for_topic"]
            tags_for_the_topic = self.data["items_by_rate_and_appearing"]["tags_by_topic"][str(topic)]["tags_for_the_topic"]
            dict_topic_rate_tags = {}
            dict_topic_rate_tags["topic"] = topic
            dict_topic_rate_tags["rate_for_topic"] = rate_for_topic
            dict_topic_rate_tags["tags_for_the_topic"]= tags_for_the_topic

            sorted_dicts_of_tags_by_sorted_topics.append(dict_topic_rate_tags)

        self.sorted_dicts_of_tags_by_sorted_topics = sorted_dicts_of_tags_by_sorted_topics



    #Get functions
    def get_sorted_list_of_channels_ids_by_rate_and_appearing(self):
        return self.sorted_list_of_channels_by_rate_and_appearing

    def get_sorted_list_of_topics_ids_by_rate_and_appearing(self):
        return self.sorted_list_of_topics_ids_by_rate_and_appearing

    def get_sorted_tags_by_topic(self, topic_id):
        return self.data["items_by_rate_and_appearing"]["tags_by_topic"][str(topic_id)]["tags_for_the_topic"]

    def get_sorted_dicts_of_tags_by_sorted_topics(self):
        return self.sorted_dicts_of_tags_by_sorted_topics

    def get_average_time_watched(self):
        return self.average_time_watched

    def get_header_of_the_json_info(self):
        return self.header_of_the_json_info

    def get_data(self):
        return self.data

    #Set functions
    def set_header_of_the_json_info(self,header_of_the_json_info):
        self.header_of_the_json_info = header_of_the_json_info

    def set_data(self, data):
        with open(self.header_of_the_json_info, 'w') as outfile:
            json.dump(data, outfile)
            outfile.close()


class VideoInfo:

    def __init__(self,api_key,video_id,time_watched,like_or_unlike,header_of_the_json_info):
        self.video_id = video_id
        self.time_watched = time_watched
        self.like_or_unlike = like_or_unlike
        self.header_of_the_json_info = header_of_the_json_info

        part="snippet%2CcontentDetails%2Cstatistics%2CtopicDetails"
        request="https://www.googleapis.com/youtube/v3/videos?part="
        final_request=request+part+"&id="+self.video_id+"&key="+api_key
        r = requests.get(final_request)
        #info from request r.status_code
        #                  r.headers
        #                  r.content
        json_content = json.loads(r.content)
        channelId = json_content["items"][0]['snippet']['channelId']
        tags_list=[]
        topics_ids_list=[]
        try:
            tags_list=json_content["items"][0]['snippet']['tags']
        except:
            print "No tags"
        try:
            topics_ids_list=json_content["items"][0]['topicDetails']['relevantTopicIds']
            topics_ids_list_with_no_duplicates = list(set(topics_ids_list))  # removing duplicates in lists
        except:
            topics_ids_list_with_no_duplicates = "no_topic"
            print "No topic details"
        self.channelId = channelId
        self.tags_list = tags_list
        self.topics_ids_list = topics_ids_list_with_no_duplicates

        #video time from the request info
        time=json_content["items"][0]['contentDetails']['duration']
        dur=isodate.parse_duration(time)
        video_time = dur.total_seconds()
        self.video_time = video_time

        #video rate with no time rate = 60%
        video_rate = 0
        watch_time_per_one = time_watched/float(self.video_time)

        video_rate = video_rate + watch_time_per_one*WEIGHT_FOR_VIDEO_TIME_WATCH
        #if like_or_unlike == -1 nothing will happen no rate
        if like_or_unlike == 0:
            video_rate = video_rate+WEIGHT_FOR_LIKE*(0.5)
        if like_or_unlike == 1:
            video_rate = video_rate+WEIGHT_FOR_LIKE

        self.video_rate = video_rate

        #
        #
        #
        if os.stat(self.header_of_the_json_info).st_size == 0:
            with open(self.header_of_the_json_info, 'w') as outfile:
                dict={}
                dict["Videos info"] = []
                dict["Videos info"].append({
                    'video_count': 0,
                    'time_watched': 0,
                    'video_id': "",
                    'tags_list': [],
                    'topics_ids_list': [],
                    'channelId': "",
                    'video_rate': 0,
                })

                dict["items_by_rate_and_appearing"] = {}
                dict["items_by_rate_and_appearing"]["tags_by_topic"] = {}
                dict["items_by_rate_and_appearing"]["list_of_all_channels_ids_and_rate"] = {}
                json.dump(dict, outfile)
                outfile.close()
        with open(self.header_of_the_json_info) as data_file:
            data = json.load(data_file)
            data_file.close()

        self.video_count = video_count_now(data)+1


    def save_info_after_watched(self):
        #Input:  api_key,video_id,watch_rate,watch_date,header_of_the_json_info
        #Output:-
        #The function get the information about the video and save it in a jason file.
        #The function set the values of the videos info object.
        with open(self.header_of_the_json_info) as data_file:
            data = json.load(data_file)
            data_file.close()
        with open(self.header_of_the_json_info, 'w') as outfile:
            data["Videos info"].append({
            'video_id': self.video_id,
            'time_watched': self.time_watched,
            'tags_list': self.tags_list,
            'topics_ids_list': self.topics_ids_list,
            'channelId': self.channelId,
            'video_rate': self.video_rate,
            'video_count': self.video_count})
            json.dump(data, outfile)
            outfile.close()

    #Set functions
    def set_video_id(self, video_id):
        self.video_id = video_id

    def set_tags_list(self, tags_list):
        self.tags_list = tags_list

    def set_topics_ids_list(self, topics_ids_list):
        self.topics_ids_list = topics_ids_list

    def set_channel_id(self, channelId):
        self.channelId = channelId

    def set_video_time(self, video_time):
        self.video_time = video_time

    def set_time_watched(self, time_watched):
        self.time_watched = time_watched

    def set_like_or_unlike(self, like_or_unlike):
        self.like_or_unlike = like_or_unlike

    def set_video_rate(self, video_rate):
        self.video_rate = video_rate

    def set_header_of_the_json_info(self, header_of_the_json_info):
        self.header_of_the_json_info = header_of_the_json_info

    def set_video_count(self, video_count):
        self.video_count = video_count

    #Get functions


    def get_video_id(self):
        return self.video_id

    def get_tags_list(self):
        return self.tags_list

    def get_topics_ids_list(self):
        return self.topics_ids_list

    def get_channel_id(self):
        return self.channelId

    def get_video_time(self):
        return self.video_time

    def get_time_watched(self):
        return self.time_watched

    def get_like_or_unlike(self):
        return self.like_or_unlike

    def get_video_rate(self):
        return self.video_rate

    def get_header_of_the_json_info(self):
        return self.header_of_the_json_info

    def get_video_count(self):
        return self.video_count


#video id with no topic: L6mrnTze_Tw
if __name__ == '__main__':
    time_watched = 345.93
    like_or_unlike = 1

    api_key = "AIzaSyD1gPOy2GQv7HzWjDy5ihhk2MZhYTsxENE"
    video_id = "57MH1mumt5w"

    header_of_the_json_info = 'data.json'
    VideoInfo1 = VideoInfo(api_key, video_id, time_watched, like_or_unlike, header_of_the_json_info)

    VideoInfo1.save_info_after_watched()
    print VideoInfo1.get_tags_list()
    print VideoInfo1.get_topics_ids_list()

    UserInfo1 = UserInfo(header_of_the_json_info)

    print UserInfo1.get_data()
    print UserInfo1.get_sorted_list_of_topics_ids_by_rate_and_appearing()
    print UserInfo1.get_sorted_list_of_channels_ids_by_rate_and_appearing()
    print UserInfo1.get_sorted_dicts_of_tags_by_sorted_topics()
    #print UserInfo1.get_sorted_list_of_channels_ids_by_rate_and_appearing()
    #print UserInfo1.get_sorted_list_of_tags_by_rate_and_appearing()
    #print UserInfo1.get_average_time_watched()