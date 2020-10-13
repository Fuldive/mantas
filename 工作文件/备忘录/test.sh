#!/usr/bin/env bash

# 本地代码目录 放在用户下面 ~
LOCAL_PROJECT_PATCH="gitleb-code";
# 项目git地址
MP_GIT_ADDRESS="git@code.petkit.com:web/com-petkit-mp.git";
# 需要拉取的分支名 默认master
BRANCH_NUMBER="master";
# 项目名字
MP_PROJECT_NAME="com-petkit-mp";

# 微信相关东西 -----------------
# 微信cli工具目录
WX_CLI="/Applications/wechatwebdevtools.app/Contents/Resources/app.nw/bin";
# End 微信相关东西 -----------------

# 进入工作目录
cd ~;
if [[ ! -s ${LOCAL_PROJECT_PATCH} ]]; then
  mkdir ${LOCAL_PROJECT_PATCH};
fi;

# ~/gitleb-code
cd ${LOCAL_PROJECT_PATCH};

# 打包后的路径 测试
MP_DIST_PATCH=`pwd`/${MP_PROJECT_NAME}"/dist/chain-user-sandbox";

echo ${MP_DIST_PATCH}
# 默认测试环境
command="maid build -m";

# 获取到需要切的分支名
while getopts "b:msla" arg
  do
    case ${arg} in
      b)
      BRANCH_NUMBER=${OPTARG};
      ;;
      ?)
      echo "未知参数: $arg"
      exit 1
      ;;
  esac
done;

# 方法 ----------------
# log
shellLog(){
    action=$1;
    echo "----------------$action------------------";
}
# 打包
packingProjectTask(){
    shellLog "----------------安装依赖------------------";
    yarn install;
    shellLog "----------------开始打包------------------";
    ${command};
    shellLog "----------------打包完成----------------";
}

# 下载项目
downLoadProjectTask(){
    if [[ ! -s "./$MP_PROJECT_NAME" ]]; then
        shellLog "------------项目不存在, 拉取代码------------";
        git clone ${MP_GIT_ADDRESS};
    fi;

    shellLog "------------项目存在，更新代码------------";
#   进入项目
    cd ${MP_PROJECT_NAME};

    shellLog "------------git fetch start------------";
    git fetch;
    shellLog "------------git fetch end------------";
    shellLog "------------git checkout start------------";
    git checkout ${BRANCH_NUMBER};
    shellLog "------------git checkout end------------";
    shellLog "------------git pull start------------";
    git pull;
    shellLog "------------git pull end------------";
}
# 调用微信开发者工具上传代码
wxUploadProjectTask(){
    shopt -s expand_aliases;
    shellLog "----------------开始上传----------------";
    curr_commit_content=`git log -1 --pretty=format:"%s"`; # 获取最近提交的git内容

    echo "最新提交内容 ${curr_commit_content}";
    curr_version=${BRANCH_NUMBER};
    cd ${WX_CLI};

#   执行上传命令
    ./cli -u ${curr_version}@${MP_DIST_PATCH} --upload-desc ${curr_commit_content};
    shellLog "----------------上传完成----------------";
}
# End 方法 ----------------

# 上传总任务
upload(){
    downLoadProjectTask;
    packingProjectTask;
    wxUploadProjectTask;
}
upload;
