# -*- coding: utf-8 -*-


def main():
    from collections import Counter
    from itertools import combinations
    list_of_items_list_and_rate  = [
[["surfing","Israel","summer","Tel Aviv"],0.8],
[["surfing","Israel"],0.6],
[["surfing","Israel"],0.85],
[["Tel Aviv"],0.95],
[["Ed Sheeran","acoustic","lyrics"],0.85],
[["Ed Sheeran","Video Clip","Passenger","Live Music"],0.1],
[["Bon","Music","Rock"],0.9],
[["MERCURY","Music","Rock"],0.87],
[["Bon","Music","Rock"],0.34],
[["Bon","Music","Jovi"],0.89]
]

    print list_of_items_list_and_rate
    list_of_item_of_the_video=[]
    for video_info in list_of_items_list_and_rate:
        list_of_item_of_the_video.append(video_info[0])

    print list_of_item_of_the_video
    print max(list_of_item_of_the_video,key=len)
    print len(max(list_of_item_of_the_video,key=len))
    d  = Counter()
    for items_list_and_rate in list_of_items_list_and_rate:
        items_list=items_list_and_rate[0]
        rate_for_items_list=items_list_and_rate[1]
        items_list.sort()
        for i in range(1,len(max(list_of_item_of_the_video,key=len))):
            for comb in combinations(items_list,i):
                d[comb] = d[comb] + rate_for_items_list

    print(d.most_common())

if __name__ == '__main__':
    main()