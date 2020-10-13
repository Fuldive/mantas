import jenkins
import time
from _collections import defaultdict

class jenkinsPython(object):
    # Jenkins域名以及个人登录账户，可以根据需要修改
    jenkins_url = 'https://ci.petkit.cn'
    user_id = 'yanziqiang'
    password = 'Petkit123'
    server = jenkins.Jenkins(jenkins_url, username=user_id, password=password)

    # 前端项目
    job_web_name = [
        {
            "name": 'sandbox-com-petkit-admin-web',
            "branch_name":"t3.2032.6",
            "projects":'com-petkit-nx-web',
            "project":'project-4-admin-web',
        },
        {
            "name": 'sandbox-com-petkit-chain-web',
            "branch_name": "t3.2032.21",
            "projects": 'com-petkit-chain-nx-web',
            "project": 'project-4-chain-web',
        }
    ]

    job_list = []

    for index in range(len(job_web_name)):
        job_list.append(job_web_name[index].get("name"))

        #构建项目
        server.build_job(job_list[index],job_web_name[index])
        #
        global console_status
        while True:
            # 设置监听事件，以秒为单位
            time.sleep(8)
            print(job_list[index]+ '版本号' + job_web_name[index].get("branch_name") + ':')

            # 获得当前构建号
            last_build_number = server.get_job_info(
                job_list[index])['lastBuild']['number']
            # 获得构建状态
            building_status = server.get_build_info(
                job_list[index], last_build_number)['building']
            # print(building_status)
            if not building_status:
                # 执行结束
                print('构建结束')
                # 获取构建结果
                console_output = server.get_build_console_output(
                    job_list[index], last_build_number)
                for i in console_output.split('\n'):
                    if 'Finished' in i and 'SUCCESS' in i:
                        console_status = 'SUCCESS'
                    if 'Finished' in i and 'FAILURE' in i:
                        console_status = 'FAILURE'
                print('构建结果:' + console_status)
                break
            else:
                print("构建中……")
                continue
            # continue
        if console_status == "FAILURE":
            print('构建失败，后续项目终止构建')
            break
