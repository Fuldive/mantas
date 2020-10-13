import jenkins
import time

# 使用说明：
# 使用前在终端输入 pip3 install python-jenkins
# 安装成功后，在终端进入Python，输入import jenkins确认是否安装成功


class jenkinsPython(object):

    # Jenkins域名以及个人登录账户，可以根据需要修改
    jenkins_url = 'http://ci.petkit.cn'
    user_id = 'Shixufeng'
    password = 'Petkit123'
    server = jenkins.Jenkins(jenkins_url, username=user_id, password=password)

    # 按顺序输入发布相关项目，项目名称必须正确且完整
    job_chain = [
         #'com-petkit-pom',
        # 'com-petkit-data-analysis',
        # 'com-petkit-aliyun-dysms',
        # 'com-petkit-food-common',
        # 'com-petkit-weixin-common',
        # 'com-petkit-user',
        # 'com-petkit-product',
        # 'com-petkit-coupon',
        # 'com-petkit-warehouse',
        # 'com-petkit-campaign',
        # 'com-petkit-mall',
        # 'com-petkit-store',
        # 'com-petkit-trade',
        # 'sandbox-com-petkit-admin',
        # 'sandbox-com-petkit-chain',
        # 'sandbox-com-petkit-sm',
         'sandbox-com-petkit-food',
        # 'sandbox-com-petkit-task',
        # 'sandbox-com-petkit-schedule',
        # 'sandbox-com-petkit-weixin',
        # 'sandbox-com-petkit-schedule-coupon',
        # 'sandbox-com-petkit-schedule-booking',
        # 'sandbox-com-petkit-notification-task',
        # 'sandbox-com-petkit-open-in-one',
        # 'sandbox-com-petkit-search'
        # 'sandbox-com-petkit-updater',
    ]
    #
    branch_name = "production"

    param = {
        "namespace": "sandbox-2",
        "branch_name": branch_name,
        "version": "latest"
    }
    for index in range(len(job_chain)):
        # 构建项目
        server.build_job(job_chain[index], param)
        #
        global console_status
        while True:
            # 设置监听事件，以秒为单位
            time.sleep(10)
            print(job_chain[index] + '版本号' + branch_name + ':')

            # 获得当前构建号
            last_build_number = server.get_job_info(
                job_chain[index])['lastBuild']['number']
            # 获得构建状态
            building_status = server.get_build_info(
                job_chain[index], last_build_number)['building']
            # print(building_status)
            if not building_status:
                # 执行结束
                print('构建结束')
                # 获取构建结果
                console_output = server.get_build_console_output(
                    job_chain[index], last_build_number)
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
