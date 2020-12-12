from flask import Flask, render_template, request, json
from club import Club
from datamanager import *
from message import *
from user import *
from activity import Activity

app = Flask(__name__)

# for test
@app.route("/gp10",methods=['GET'])
def test_form():
    return "response from SE group 10"

'''
API:
create a user (用户注册)
'''
@app.route('/gp10/createUser', methods=['POST'])
def createUser():
    wxid = request.form.get("wx_id")
    name = request.form.get("user_name")
    datamanager = DataManager(DataType.user)
    user = User(wxid=wxid, name=name)
    datamanager.addInfo(user)

    res = {'status':'200 OK'}
    return json.dumps(res)

'''
API:
create a club
'''
@app.route('/gp10/createClub', methods=['POST'])
def createClub():
    club_name = request.form.get("club_name")
    club_description = request.form.get("club_description")
    club_president_wxid = request.form.get("club_president_user_id")

    club=Club(club_name=club_name,club_description=club_description,club_president_wxid=club_president_wxid)
    manager=DataManager(DataType.club)
    manager.addInfo(club)

    res={'status':'200 OK'}
    return json.dumps(res)

'''
API:
delete a club
'''
@app.route('/gp10/deleteClub', methods=['POST'])
def deleteClub():
    club_id = int(request.form.get("club_id"))
    manager = DataManager(DataType.club)
    manager.deleteInfo(club_id)

    res = {'status':'200 OK'}
    return json.dumps(res)

'''
API:
Function: getClubInfo(club_id) 
Return: {'status':status,'club_name': club_name, 'club_description':club_description,'club_president_user_id',club_president_user_id}

Return in Json format
'''
@app.route('/gp10/getClubInfo', methods=['POST'])
def getClubInfo():
    club_id = int(request.form.get("club_id"))
    manager=DataManager(DataType.club)
    club_info=manager.getInfo(club_id)
    if len(club_info)==0:
        return json.dumps({'status:':'Not Found'})
    club=Club(club_id=club_id,club_name=club_info[0][1],club_description=club_info[0][2],club_president_wxid=club_info[0][3])
    res=club.Jsonfy()
    return res

'''
API: getClubManagers
获取社团骨干列表
'''
@app.route('/gp10/getClubManagers', methods = ['POST'])
def getClubManagers():
    club_id = int(request.form.get("club_id"))
    datamanager = DataManager(DataType.club_managers)
    res = datamanager.getSlaveList(club_id)
    return json.dumps({'status':'200 OK', 'club_manager_list': res})

'''
API: getClubMembers
获取社团成员列表
'''
@app.route('/gp10/getClubMembers', methods = ['POST'])
def getClubMembers():
    club_id = int(request.form.get("club_id"))
    datamanager = DataManager(DataType.club_members)
    res = datamanager.getSlaveList(club_id)
    return json.dumps({'status':'200 OK', 'club_member_list': res})

'''
API: getClubActivities
获取社团活动列表
'''
@app.route('/gp10/getClubActivities', methods = ['POST'])
def getClubActivities():
    club_id = int(request.form.get("club_id"))
    datamanager = DataManager(DataType.club_activities)
    res = datamanager.getSlaveList(club_id)
    return json.dumps({'status':'200 OK', 'club_activity_list': res})

'''
API: addManagerToClub
向社团增加骨干
'''
@app.route('/gp10/addManagerToClub', methods = ['POST'])
def addManagerToClub():
    club_id = int(request.form.get("club_id"))
    wxid = request.form.get("wx_id")
    datamanager = DataManager(DataType.club_managers)
    datamanager.addSlaveInfo(club_id, wxid)

    res = {'status':'200 OK'}
    return json.dumps(res)

'''
API: addMemberToClub
向社团增加成员
'''
@app.route('/gp10/addMemberToClub', methods = ['POST'])
def addMemberToClub():
    club_id = int(request.form.get("club_id"))
    wxid = request.form.get("wx_id")
    datamanager = DataManager(DataType.club_members)
    datamanager.addSlaveInfo(club_id, wxid)

    res = {'status': '200 OK'}
    return json.dumps(res)

'''
API: addActivityToClub
向社团增加活动
'''
@app.route('/gp10/addActivityToClub', methods = ['POST'])
def addActivityToClub():
    club_id = int(request.form.get("club_id"))
    activity_id = int(request.form.get("activity_id"))
    datamanager = DataManager(DataType.club_activities)
    datamanager.addSlaveInfo(club_id, activity_id)

    res = {'status':'200 OK'}
    return json.dumps(res)

'''
API: deleteManagerFromClub
从社团删除骨干
'''
@app.route('/gp10/deleteManagerFromClub', methods = ['POST'])
def deleteManagerFromClub():
    club_id = int(request.form.get("club_id"))
    wxid = request.form.get("wx_id")
    datamanager = DataManager(DataType.club_managers)
    datamanager.deleteSlaveInfo(club_id, wxid)

    res = {'status': '200 OK'}
    return json.dumps(res)

'''
API: deleteMemberFromClub
从社团删除成员
'''
@app.route('/gp10/deleteMemberFromClub', methods = ['POST'])
def deleteMemberFromClub():
    club_id = int(request.form.get("club_id"))
    wxid = request.form.get("wx_id")
    datamanager = DataManager(DataType.club_members)
    datamanager.deleteSlaveInfo(club_id, wxid)

    res = {'status': '200 OK'}
    return json.dumps(res)

'''
API: deleteActivityFromClub
从社团删除活动
'''
@app.route('/gp10/deleteActivityFromClub', methods = ['POST'])
def deleteActivityFromClub():
    club_id = int(request.form.get("club_id"))
    activity_id = int(request.form.get("activity_id"))
    datamanager = DataManager(DataType.club_activities)
    datamanager.deleteSlaveInfo(club_id, activity_id)

    res = {'status': '200 OK'}
    return json.dumps(res)

'''
API:setClubInfo
设定社团信息
'''
@app.route('/gp10/setClubInfo', methods=['POST'])
def setClubInfo():
    club_id = int(request.form.get("club_id"))
    club_name = request.form.get("club_name")
    club_description = request.form.get("club_description")
    club_president_wxid = request.form.get("club_president_user_id")
    club=Club(club_id=club_id,club_name=club_name,club_description=club_description,club_president_wxid=club_president_wxid)
    manager=DataManager(DataType.club)
    manager.updateInfo(club)
    res = {'status':'200 OK'}
    return json.dumps(res)

'''
API:getClubList
获取社团列表
'''
@app.route('/gp10/getClubList', methods=['POST','GET'])
def getClubList():
    manager=DataManager(DataType.club)
    res=manager.getList()
    club_list=[]
    for club in res:
        club_list.append((club[0],club[1]))
    return json.dumps({'status':'200 OK','club_list':club_list})

'''
API:getRelatedClubList
输入关键字keyword，返回相关的社团
'''
@app.route('/gp10/getRelatedClubList', methods=['POST'])
def getRelatedClubList():
    keyword = request.form.get("keyword")
    manager=DataManager(DataType.club)
    res=manager.getList()
    related_club_list=[]
    for club in res:
        if keyword in club[1] or keyword in club[2]:
            related_club_list.append((club[0],club[1]))
    return json.dumps({'status':'200 OK','related_club_list':related_club_list})

'''
API:
Function: sendMessage(wx_id_sender, wx_id_receiver, type, title, content)
Return: {'status': status}
'''
@app.route('/gp10/sendMessage', methods = ['POST'])
def sendMessage():
    message_type = request.form.get("type")
    message_title = request.form.get("title")
    message_content = request.form.get("content")
    message_sender_wxid = request.form.get("wx_id_sender")
    message_receiver_wxid = request.form.get("wx_id_receiver")
    message = Message(message_type=message_type, message_title=message_title, message_content=message_content,
                      message_sender_wxid=message_sender_wxid, message_receiver_wxid=message_receiver_wxid)
    manager = DataManager(DataType.message)
    manager.addInfo(message)

    res = {'status':'200 OK'}
    return json.dumps(res)

'''
API:
Function: getMessages(wx_id)
Return: {status: ‘’, send_message_list: [ {id: '', type: ‘’, title: ‘’, content: ‘’, sender: ‘’, receiver: ‘’} , …], 
    receive_message_list: [ {id: '', type: ‘’, title: ‘’, content: ‘’, sender: ‘’, receiver: ‘’} , …]}
其中send_message_list包含该wx_id发出的信息，receive_message_list包含该wx_id收到的信息

Return in JSON format
'''
@app.route('/gp10/getMessages', methods = ['POST'])
def getMessages():
    wxid = request.form.get("wx_id")
    message_list_of_user = MessageListOfUser(wxid=wxid)
    return json.dumps(message_list_of_user.__dict__)


'''
API:
Function: getActivityInfo(Activity_id)
return:{'status':status, 'activity_name':activity_name, 'activity_description':description, 'activity_club_id':club_id,
'activity_place':place, 'activity_start_time':start_time, 'activity_end_time':end_time, 'activity_lottery_time':lottery_time,
'activity_lottery_method':lottery_method, 'activity_max_number':max_number, 'activity_registered_people':registered_people,
'activity_selected_people':selected_people }
Return in Json format

返回的是Activity的json化，如果需要返回其他属性，需要修改Activity类的属性及方法
'''
@app.route('/gp10/getActivityInfo', methods=['POST'])
def getActivityInfo():
    activity_id = int(request.form.get("activity_id"))
    manager = DataManager(DataType.activity)
    activity_info = manager.getInfo(activity_id)
    if len(activity_info) == 0 :
        return json.dumps({'status':'Not Found'})

    activity = Activity(at_id=activity_id, at_name=activity_info[0][1], at_description=activity_info[0][2], 
    at_club_id=activity_info[0][3], at_place=activity_info[0][4], at_start_time=activity_info[0][5], 
    at_end_time=activity_info[0][6], at_lottery_time=activity_info[0][7], at_lottery_method=activity_info[0][8], 
    at_max_number=activity_info[0][9] )
    
    res = activity.Jsonfy()

    return res

'''
API:
Function: getActivityList()
Return: ActivityList

list中每一项包含id和name
'''
@app.route('/gp10/getActivityList', methods=['POST','GET'])
def getActivityList():
    manager = DataManager(DataType.activity)
    li = manager.getList()
    activity_list = []
    for activity in li:
        activity_list.append((activity[0], activity[1]))
    
    return json.dumps({'status':'200 OK', 'activity_list':activity_list})


'''
API:createActivity
Function: createActivity(name,description,club_id,place,start_time,end_time,lottery_time,lottery_method,max_number)
create an activity
return: {status,id} in JSON format
'''
@app.route('/gp10/createActivity',methods=['POST'])
def createActivity():
    activity_name = request.form.get("name")
    activity_description = request.form.get("description")
    activity_club_id = int(request.form.get("club_id"))
    activity_place = request.form.get("place")
    activity_start_time = request.form.get("start_time")
    activity_end_time = request.form.get("end_time")
    activity_lottery_time = request.form.get("lottery_time")
    activity_lottery_method = request.form.get("lottery_method")
    activity_max_number = int(request.form.get("max_number"))

    newActivity = Activity(at_name=activity_name, at_description=activity_description, at_club_id=activity_club_id,
    at_place=activity_place, at_start_time=activity_start_time, at_end_time=activity_end_time,
    at_lottery_time=activity_lottery_time, at_lottery_method=activity_lottery_method,at_max_number=activity_max_number)

    manager = DataManager(DataType.activity)
    manager.addInfo(newActivity)

    res = {'status':'200 OK', 'id':newActivity.id}
    return json.dumps(res)


'''
API: setActivityInfo
Function: setActivityInfo(id,name,description,club_id,place,start_time,end_time,lottery_time,lottery_method,max_number)
return:{status} in JSON format
'''
@app.route('/gp10/setActivityInfo', methods=['POST'])
def setActivityInfo():
    activity_id = int(request.form.get("id"))
    activity_name = request.form.get("name")
    activity_description = request.form.get("description")
    activity_club_id = int(request.form.get("club_id"))
    activity_place = request.form.get("place")
    activity_start_time = request.form.get("start_time")
    activity_end_time = request.form.get("end_time")
    activity_lottery_time = request.form.get("lottery_time")
    activity_lottery_method = request.form.get("lottery_method")
    activity_max_number = int(request.form.get("max_number"))
    
    myActivity = Activity(at_id=id, at_name=activity_name, at_description=activity_description, at_club_id=activity_club_id,
    at_place=activity_place, at_start_time=activity_start_time, at_end_time=activity_end_time,
    at_lottery_time=activity_lottery_time, at_lottery_method=activity_lottery_method,at_max_number=activity_max_number)

    manager = DataManager(DataType.activity)
    manager.updateInfo(myActivity)

    res = {'status':'200 OK'}
    return json.dumps(res)




if __name__ == '__main__':
    app.run(debug=True, threaded=True,host='0.0.0.0',port=5000)
