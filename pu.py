import json
import requests
import xlwt
import base64
import os

company_token = '4450c6eb7c034a8e9bb2f5ae60fce9e3'
account_token = '495c6a6b05194a4498f872a09e8238ee'

# 串API 需要的參數
URL = "https://ezpy.pu.edu.tw/dataTrans/index.php/FRS/"

PU_KEY = 'cHVfY2NjX2Zycw'
API_EMP = 'employee_base?='
API_EMP_PHOTO ='employee_photo'
API_STU = 'students_base?='
API_STU_PHOTO = 'students_photo'
API_UNI = 'unit_data?='

URL_API_UNI = URL + API_UNI + PU_KEY
URL_EMP_API = URL + API_EMP + PU_KEY 
URL_EMP_PHOTO = URL +API_EMP_PHOTO

URL_STU_API = URL + API_STU + PU_KEY
URL_STU_PHOTO = URL + API_STU_PHOTO

baseheaders = {
   'Content-Type': "application/x-www-form-urlencoded",
   'secretKey': "cHVfY2NjX2Zycw",
   'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
   'Accept': "*/*",
   'Cache-Control': "no-cache",
   'Host': "ezpy.pu.edu.tw",
   'Accept-Encoding': "gzip, deflate",
   'Content-Length': "0",
   'Connection': "keep-alive",
   }

avatarheaders = {
    'Content-Type': "application/x-www-form-urlencoded",
    'secretKey': "cHVfY2NjX2Zycw",
    'User-Agent': "PostmanRuntime/7.20.1",
    'Accept': "*/*",
    'Cache-Control': "no-cache",
    'Postman-Token': "83bdc6dc-e640-40f0-bd32-eb7ddc997062,ba2196bd-f9ca-46bf-91a5-9ff57c1d6b05",
    'Host': "ezpy.pu.edu.tw",
    'Accept-Encoding': "gzip, deflate",
    'Content-Length': "4",
    'Cookie': "citrix_ns_id=PcSefr3+nOP8Egz6jiHjKs4Vtho0002",
    'Connection': "keep-alive",
    'cache-control': "no-cache"
    }
# # 1. 匯入 team（下⼀階段）
# def get_team(URL_API_UNI, baseheaders):
#     response = requests.request("POST", URL_API_UNI, headers=baseheaders)
#     team =json.loads(response.text)
#     return team.text

# team = get_team(URL_API_UNI, baseheaders)

# # 2. 匯入員⼯資訊(可以增改員工資料)
def get_staffs_from_uni(URL_EMP_API):
    get_staffs_from_uni = requests.request("POST", URL_EMP_API, headers=baseheaders)
    get_staffs_uni = json.loads(get_staffs_from_uni.text)
    return get_staffs_uni

def get_staffs_uni_regular_import(staffs_uni_file_path,company_token,account_token):
    url = 'http://127.0.0.1:8000/api/staffs/regular_import'
    payload = {'company_token': company_token,
        'account_token': account_token}
    my_files = {'file_xls': open(staffs_uni_file_path,'rb')}
    r = requests.post(url,data=payload , files=my_files)
    err = r.text
    if err:
        return err

def get_staffs_uni_file_path(staffs):
    wb = xlwt.Workbook()
    sh = wb.add_sheet('avartor')
    if staffs['success'] is not 1:
        return "API Erro"
    else:     
        x=0
        for staff in staffs['data']:
            if x<180:
                y=0
                sh.write(x, y, '靜宜大學測試')
                y+=1
                sh.write(x, y, staff['id'])
                y+=1
                sh.write(x, y, staff['name'])
                y+=1
                sh.write(x, y, staff['name'])
                y+=1
                sh.write(x, y, staff['email'])
                y+=1
                sh.write(x, y, '體育館')  # 這邊先不處理
                y+=1
                sh.write(x, y, '2019-12-23')
                y+=1
                sh.write(x, y, ' ')
                y+=1
                sh.write(x, y, 'note')
                x+=1
        wb.save('avatar.xls')   
    file_path = os.path.abspath('avatar.xls')
    return file_path
        
staffs_file_from_uni = get_staffs_from_uni(URL_EMP_API)
staffs_uni_file_path = get_staffs_uni_file_path(staffs_file_from_uni)
staffs_uni_regular_import = get_staffs_uni_regular_import(staffs_uni_file_path,company_token,account_token) 
# 2. 比對ceo && uni_avatar
def get_staffs_avatas_from_uni(URL_EMP_PHOTO):
    payload = "id=a"
    response = requests.request("POST", URL_EMP_PHOTO, data=payload, headers=avatarheaders)
    uni_avatars =json.loads(response.text)
    return uni_avatars

def get_ceo_staffs(company_token):
    url = 'http://127.0.0.1:8000/api/staffs/list'
    payload = {'company_token':company_token}
    r = requests.post(url,data=payload)
    staffs =json.loads(r.text)
    if r.text is '':
        return 'NO STAFFS LIST'
    return staffs

# 把ceo跟uni_avatar撈出
ceo_staffs = get_ceo_staffs(company_token)
staffs_avatas_from_uni = get_staffs_avatas_from_uni(URL_EMP_PHOTO)

# TODO : 排除VIP token 先假定體育館為VIP 1ed89101990d41c09762c7b6e93283f9
def get_vip_ids():
    team_id = '0'
    return team_id
vip_team_ids = get_vip_ids()

# 做ceo vip的排除
def splt_staffs_by_team_ids(ceo_staffs,staffs_avatas_from_uni,vip_team_ids):
    staffs_not_vip = []
    staffs_w_vip = []
    for ceo_staff in ceo_staffs['staffs']:
        if vip_team_ids == ceo_staff['team_id']:
            staffs_w_vip.append(ceo_staff['emp_id'])
        else:
            staffs_not_vip.append(ceo_staff['emp_id'])
    # print('staffs_not_vip : ' + str(staffs_not_vip))
    # print('staffs_w_vip : ' + str(staffs_w_vip))
    return staffs_not_vip,staffs_w_vip

staffs_not_vip,staffs_w_vip = splt_staffs_by_team_ids(ceo_staffs,staffs_avatas_from_uni, vip_team_ids) 

#######################################################################################################

def base64_to_avatar(URL_EMP_PHOTO, staffs_not_vip,avatarheaders):
    # print('staffs_not_vip1 : ' + str(staffs_not_vip))
    staff_not_vip_wo_avatar = []
    staff_not_vip_w_avatar = []
    for staff_not_vip in staffs_not_vip:
        # print("staff_not_vip : " + staff_not_vip)
        payload =  'id=' + staff_not_vip
        response = requests.request("POST", URL_EMP_PHOTO, data=payload, headers=avatarheaders)
        staff_not_vip_avatars =json.loads(response.text)
        # print(staff_not_vip_avatars['data'])
        for staff_not_vip_avatar in staff_not_vip_avatars['data']:
            if staff_not_vip_avatar['img'] is '':
                staff_not_vip_wo_avatar.append(staff_not_vip_avatar['id'])

            else:
                staff_not_vip_w_avatar.append(staff_not_vip_avatar['id'])
                img = base64.urlsafe_b64decode(staff_not_vip_avatar['img'])
                fh = open(staff_not_vip_avatar['id'] + '.jpeg', "wb")
                fh.write(img)
                fh.close()
    # print('staff_not_vip_wo_avatar : ' + str(staff_not_vip_wo_avatar))
    # print('staff_not_vip_w_avatar : ' + str(staff_not_vip_w_avatar))
    return staff_not_vip_wo_avatar,staff_not_vip_w_avatar
      

def ceo_avatar_update_wo_vips(staff_not_vip_w_avatars, company_token):
    url = 'http://127.0.0.1:8000/api/staffs/list'
    payload = {'company_token':company_token}
    ceo_staffs_list_tmp = requests.request("POST", url, data = payload)
    ceo_staffs_list = json.loads(ceo_staffs_list_tmp.text)

    url_update = 'http://127.0.0.1:8000/api/staffs/avatar_update'
    directory = os.getcwd()
    for ceo_staff in ceo_staffs_list['staffs']:
        for staff_not_vip_w_avatar in staff_not_vip_w_avatars:
            if ceo_staff['emp_id'] == staff_not_vip_w_avatar:
                staff_avatar_file = os.path.join(directory, staff_not_vip_w_avatar + '.jpeg')
                print(staff_avatar_file)
                my_files = {'image_file': open(staff_avatar_file, 'rb')}
                # my_files = {'image_file': '/home/webber/project/elf/074008.jpeg'}
                # print(my_files)
                # print('ceo_staff_token : ' + ceo_staff['token'])
                payload = {'company_token':company_token, 'staff_token':ceo_staff['token'] }
                # print(payload)
                ceo_staff_avatar_update = requests.request("POST", url_update, data = payload, files = my_files)
                # print('圖片上傳錯誤')
                # print(ceo_staff_avatar_update.request.body.decode('utf-8'))
                print(ceo_staff_avatar_update.text)

    return None
# 

    # url = "http://127.0.0.1:8000/api/staffs/avatar_update"
    # payload = {'company_token': '4450c6eb7c034a8e9bb2f5ae60fce9e3',
    # 'staff_token': 'c339b251db6f4351b28de328cc5c779b'
    # }
    # # files = {'image_file': ('123456.jpg', open('123456.jpg','rb'), 'img/image')}
    # my_files = {'image_file': '/home/webber/project/elf/069002.jpeg'}
    
    # response = requests.request("POST", url, data = payload, files = my_files)

#     # print(response.text.encode('utf8'))
#     # print(response.request.body)
    # print(response.text)
  
# print('staffs_not_vip : ' + str(staffs_not_vip))

# print('staffs_not_vip : ' + staffs_not_vip)
# if staffs_not_vip is not '':
# print('staffs_not_vip : ' + str(staffs_not_vip))
staff_not_vip_wo_avatar,staff_not_vip_w_avatar = base64_to_avatar(URL_EMP_PHOTO, staffs_not_vip, avatarheaders)
ceo_avatar_update_wo_vips(staff_not_vip_w_avatar,company_token)

    # staffs_not_vip_wo_avatars_files = base64_to_avatar(URL_EMP_PHOTO, staffs_not_vip, avatarheaders)
    # print(staffs_not_vip_wo_avatars_files)
    # ceo_avatar_update_o_vip(staffs_not_vip_wo_avatars_files,company_token)


# if staffs_w_vip is '':
#     print('vipisnull')
# staffs_not_vip 做 avatar_remove && avatar_update
# staffs_avatars_w_avatar 
# ceo_staffs_wo_avatar,ceo_staffs_w_avatar = splt_staffs_by_avatar(uni_staffs_from_ceo,staffs_file_from_uni)



# uni_staffs_avator = get_uni_staffs_avator()
# # 3. 刪除員⼯頭像
# # 取得門禁員工
# ceo_staffs = get_staffs_from_ceo()
# # 排除 VIP 員工資料
# staffs_not_vip = splt_staffs_by_team_ids(ceo_staffs, vip_team_ids) # vip team token
# # 取得校務員工
# uni_staffs
# # 要刪除頭像員工 = VIP以外員工 - 校務員工 
# staffs_to_remove = get_staffs_to_remove_avator(staffs_not_vip, uni_staffs)
# # 刪除頭像
# err = remove_avatar(staffs_to_remove)

# if err:
#     print(err)

# # 4. 新增員⼯頭像
# #已經有頭像的 ceo 員工
# ceo_staffs_wo_avatar, ceo_staffs_w_avatar = splt_staffs_by_avatar(ceo_staffs)
# # 校務員工
# uni_staffs
# # 要新增頭像的員工 = 校務員工 - 已經有頭像的 ceo 員工
# staffs_to_update = get_staffs_to_update_avator(ceo_staffs_wo_avatar, ceo_staffs_w_avatar, uni_staffs) 
# # 更新頭像
# err = update_avatar(staffs_to_update)
# # 

# if err:
#     print(err)

# def get_staffs_to_update_avator(ceo_w_avatar, ceo_wo_avatar, uni_staffs):

#     staffs_need_update = []

#     for uni_staff in uni_staffs:
#         staff = objHelper.ezFind(ceo_w_avatar, uni_staff['emp_id'])

#         if not staff:
#             staff = objHelper.ezFind(ceo_wo_avatar, uni_staff['emp_id'])

#             if not staff:
#                 return err

#             staffs_need_update.append(staff)

#     return staffs_need_update

#     def ceo_api(api, data, file):
