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
    today_wday = localtime().tm_wday
    
    go_main_button = '처음으로'
    go_back_button = '뒤로 가기'
    select_day = '요일지정'

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
        if meal_list[i] == '-':
            meal_list[i] = '\n학식이 없는 날이거나 홈페이지에 등록되지 않았습니다.'

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

    # 분기문
    if return_str == '오늘':
        if wday_arr[today_wday] == 'sat' or wday_arr[today_wday] == 'sun':
            return JsonResponse(
            {
                'version': '2.0',
                'template': {
                    'outputs': [
                        {
                            'simpleText': {
                                'text': '오늘은 주말입니다. :)'
                            }
                        }
                    ],
                    'quickReplies': [
                        {
                            'label': go_main_button,
                            'action': 'message',
                            'messageText': go_main_button
                        }
                    ]
                }
            }
        )
        else:
            return JsonResponse(
            {
                'version': '2.0',
                'template': {
                    'outputs': [
                        {
                            'simpleText': {
                                'text': info[wday_arr[today_wday]]+
                                        '\n오늘 학식입니다.\n\n'+
                                        s_day[wday_arr[today_wday]]+''+
                                        e_day[wday_arr[today_wday]]
                            }
                        }
                    ],
                    'quickReplies': [
                        {
                            'label': go_main_button,
                            'action': 'message',
                            'messageText': go_main_button
                        }
                    ]
                }
            }
        )

    elif return_str == '내일':
        if wday_arr[today_wday] == 'fri' or wday_arr[today_wday] == 'sat':
            return JsonResponse(
            {
                'version': '2.0',
                'template': {
                    'outputs': [
                        {
                            'simpleText': {
                                'text': '내일은 주말입니다. :)'
                            }
                        }
                    ],
                    'quickReplies': [
                        {
                            'label': go_main_button,
                            'action': 'message',
                            'messageText': go_main_button
                        }
                    ]
                }
            }
        )
        else:
            return JsonResponse(
            {
                'version': '2.0',
                'template': {
                    'outputs': [
                        {
                            'simpleText': {
                                'text': info[wday_arr[(today_wday+1)%7]]+
                                        '\n내일 학식입니다.\n\n'+
                                        s_day[wday_arr[(today_wday+1)%7]]+''+
                                        e_day[wday_arr[(today_wday+1)%7]]
                            }
                        }
                    ],
                    'quickReplies': [
                        {
                            'label': go_main_button,
                            'action': 'message',
                            'messageText': go_main_button
                        }
                    ]
                }
            }
        )

    elif return_str == '요일지정':
        return JsonResponse(
        {
            'version': '2.0',
            'template': {
                'outputs': [
                    {
                        'simpleText': {
                            'text': '요일을 선택하세요.'
                        }
                    }
                ],
                'quickReplies': [
                    {
                        'label': '월',
                        'action': 'message',
                        'messageText': '월'
                    },
                    {
                        'label': '화',
                        'action': 'message',
                        'messageText': '화'
                    },
                    {
                        'label': '수',
                        'action': 'message',
                        'messageText': '수'
                    },
                    {
                        'label': '목',
                        'action': 'message',
                        'messageText': '목'
                    },
                    {
                        'label': '금',
                        'action': 'message',
                        'messageText': '금'
                    }
                ]
            }
        }
    )

    elif return_str == '상시메뉴':
        return JsonResponse(
        {
            'version': '2.0',
            'template': {
                'outputs': [
                    {
                        'simpleText': {
                            'text': '학식 제공시간: 10:00~18:30\n'\
                                    ':: 4000원 ::\n'+s_day['every']
                        }
                    }
                ],
                'quickReplies': [
                    {
                        'label': go_main_button,
                        'action': 'message',
                        'messageText': go_main_button
                    }
                ]
            }
        }
    )

    elif return_str == '월':
        return JsonResponse(
        {
            'version': '2.0',
            'template': {
                'outputs': [
                    {
                        'simpleText': {
                            'text': info['mon']+'\n학식입니다.\n\n'+
                                    s_day['mon']+''+e_day['mon']
                        }
                    }
                ],
                'quickReplies': [
                    {
                        'label': go_main_button,
                        'action': 'message',
                        'messageText': go_main_button
                    },
                    {
                        'label': go_back_button,
                        'action': 'message',
                        'messageText': select_day
                    }
                ]
            }
        }
    )

    elif return_str == '화': 
        return JsonResponse(
        {
            'version': '2.0',
            'template': {
                'outputs': [
                    {
                        'simpleText': {
                            'text': info['tue']+'\n학식입니다.\n\n'+
                                    s_day['tue']+''+e_day['tue']
                        }
                    }
                ],
                'quickReplies': [
                    {
                        'label': go_main_button,
                        'action': 'message',
                        'messageText': go_main_button
                    },
                    {
                        'label': go_back_button,
                        'action': 'message',
                        'messageText': select_day
                    }
                ]
            }
        }
    )

    elif return_str == '수': 
        return JsonResponse(
        {
            'version': '2.0',
            'template': {
                'outputs': [
                    {
                        'simpleText': {
                            'text': info['wed']+'\n학식입니다.\n\n'+
                                    s_day['wed']+''+e_day['wed']
                        }
                    }
                ],
                'quickReplies': [
                    {
                        'label': go_main_button,
                        'action': 'message',
                        'messageText': go_main_button
                    },
                    {
                        'label': go_back_button,
                        'action': 'message',
                        'messageText': select_day
                    }
                ]
            }
        }
    )

    elif return_str == '목': 
        return JsonResponse(
        {
            'version': '2.0',
            'template': {
                'outputs': [
                    {
                        'simpleText': {
                            'text': info['thu']+'\n학식입니다.\n\n'+
                                    s_day['thu']+''+e_day['thu']
                        }
                    }
                ],
                'quickReplies': [
                    {
                        'label': go_main_button,
                        'action': 'message',
                        'messageText': go_main_button
                    },
                    {
                        'label': go_back_button,
                        'action': 'message',
                        'messageText': select_day
                    }
                ]
            }
        }
    )

    elif return_str == '금': 
        return JsonResponse(
        {
            'version': '2.0',
            'template': {
                'outputs': [
                    {
                        'simpleText': {
                            'text': info['fri']+'\n학식입니다.\n\n'+
                                    s_day['fri']+''+e_day['fri']
                        }
                    }
                ],
                'quickReplies': [
                    {
                        'label': go_main_button,
                        'action': 'message',
                        'messageText': go_main_button
                    },
                    {
                        'label': go_back_button,
                        'action': 'message',
                        'messageText': select_day
                    }
                ]
            }
        }
    )

    else: 
        return JsonResponse(
        {
            'version': '2.0',
            'template': {
                'outputs': [
                    {
                        'simpleText': {
                            'text': '개발 중이거나 오류입니다. '\
                                    '개발자에게 문의해주세요. \n'\
                                    'dev.dain.k.@gmail.com'
                        }
                    }
                ],
                'quickReplies': [
                    {
                        'label': go_main_button,
                        'action': 'message',
                        'messageText': go_main_button
                    }
                ]
            }
        }
    )

