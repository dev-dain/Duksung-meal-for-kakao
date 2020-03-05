from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from time import localtime
from datetime import datetime
import json


def keyboard(request):
    return JsonResponse({
        'type': 'text'
    })

@csrf_exempt
def message(request):
    answer = ((request.body).decode('utf-8'))
    return_json_str = json.loads(answer)
    return_str = return_json_str['userRequest']['utterance']

    wday_arr = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
    go_main_button = '초기화면'
    today_wday = localtime().tm_wday
    
    meal_path = '/home/ubuntu/haksik_project/haksik/week_meal.txt'
    # open에는 full 경로 설정 필수
    meal_fp = open(meal_path, 'r', encoding='utf-8')

    temp_str = ''
    for line in meal_fp.readlines():
        temp_str += line
    temp_str = temp_str.strip('\n')
    meal_list = []
    meal_list = temp_str.split('\n\n')
    meal_fp.close()

    info_path = '/home/ubuntu/haksik_project/haksik/week_info.txt'
    info_fp = open(info_path, 'r', encoding='utf-8')

    temp_str = ''
    for line in info_fp.readlines():
        temp_str += line
    temp_str = temp_str.strip('\n')
    info_list = []
    info_list = temp_str.split('\n\n')
    info_list = [tmp for tmp in info_list if tmp]
    info_fp.close()

    for i in range(11):
        if meal_list[i] == '\xa0' or meal_list[i] == '\n\n':
            meal_list[i] += '\n학식이 없는 날이거나 홈페이지에 등록되지 않았습니다.'

    add_text = ''
    for j in range(10):
        if j < 5:
            add_text += '*'
            add_text += info_list[6]
            add_text += '\n'
        else:
            add_text += '\n<택1>\n\n*'
            add_text += info_list[7]
            add_text += '\n'
        add_text += meal_list[j]
        meal_list[j] = add_text
        add_text = ''

    s_day = {'mon': meal_list[0], 'tue': meal_list[1], 'wed': meal_list[2],
            'thu': meal_list[3], 'fri': meal_list[4], 'every': meal_list[10]}
    e_day = {'mon': meal_list[5], 'tue': meal_list[6], 'wed': meal_list[7],
            'thu': meal_list[8], 'fri': meal_list[9]}
    info = {'mon': info_list[1], 'tue': info_list[2], 'wed': info_list[3],
            'thu': info_list[4], 'fri': info_list[5]}

    if return_str == '테스트':
        return JsonResponse({
            'version': "2.0",
            'template': {
                'outputs': [{
                    'simpleText': {
                        'text': info_list[1]+"\n테스트 성공입니다."
                    }
                }],
                'quickReplies': [{
                    'label': '처음으로',
                    'action': 'message',
                    'messageText': '처음으로'
                }]
            }
        })
