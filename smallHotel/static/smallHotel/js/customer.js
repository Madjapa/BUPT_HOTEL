const axiosInstance = axios.create({
    baseURL: 'http://127.0.0.1:8000/smallHotel/cus/', // 设置后端 API 地址
    headers: {
        'Content-Type': 'application/json' // 设置请求头
    }
});
function btnFuncAdd(){//给button添加点击事件
    document.getElementById('target_temp_sub_button').setAttribute("onclick","tempSub()");
    document.getElementById('target_temp_add_button').setAttribute("onclick","tempAdd()");
    document.getElementById('low_speed_button').setAttribute("onclick","windspeedAdjust.call(this)");
    document.getElementById('middle_speed_button').setAttribute("onclick","windspeedAdjust.call(this)");
    document.getElementById('high_speed_button').setAttribute("onclick","windspeedAdjust.call(this)");
    document.getElementById('cool_button').setAttribute("onclick","coolButton()");
    document.getElementById('heat_button').setAttribute("onclick","heatButton()");
}
function btnFuncCease(){//删除button的点击事件
    document.getElementById('target_temp_sub_button').removeAttribute("onclick");
    document.getElementById('target_temp_add_button').removeAttribute("onclick");
    document.getElementById('low_speed_button').removeAttribute("onclick");
    document.getElementById('middle_speed_button').removeAttribute("onclick");
    document.getElementById('high_speed_button').removeAttribute("onclick");
    document.getElementById('cool_button').removeAttribute("onclick");
    document.getElementById('heat_button').removeAttribute("onclick");
}
function bootfront(){
//界面
//修改上方状态栏（关机->运行中）
//修改温度界面（开空调改为关空调）
//（隐藏->显示）调温界面或修改调温界面中间元素为（--- -> 26℃）
    //风速栏风速条默认中风速，低中风速涂颜色，风速文字显示
//目前累计费用（--元 -> 0元）
//制冷默认打开（调用coolButton）
    document.getElementById('statusText').textContent = '运行中';
    document.getElementById('switch').textContent = '关空调';
    document.getElementById('targetTemp').textContent = String(targetTemp);
    document.getElementById('roomtemp').textContent = '---';
    document.getElementById('expenses').textContent = '---';
    //document.getElementById('expenses').textContent = '0';
}
function shutdownfront(){
    document.getElementById('statusText').textContent = '关机';
    document.getElementById('switch').textContent = '开空调';
    document.getElementById('targetTemp').textContent = '---';
    document.getElementById('roomtemp').textContent = '---';
    document.getElementById('expenses').textContent = '---';
}
function tempAdd(){//空调升温
    clearTimeout(tempTimer);
    //点击后先停止上一个时钟
    targetTemp = targetTemp + 1;
    //目标温度+1
    document.getElementById('targetTemp').textContent = String(targetTemp);
    //显示在温度调节器上
    tempTimer = setTimeout(tempSubmit,500);
    //计时，计时结束前若时钟没有被停止则执行tempSubmit()
}
function tempSub(){//空调降温
    clearTimeout(tempTimer);
    //点击后先停止上一个时钟
    targetTemp = targetTemp - 1;
    //目标温度-1
    document.getElementById('targetTemp').textContent = String(targetTemp);
    //显示在温度调节器上
    tempTimer = setTimeout(tempSubmit,500);
    //计时，计时结束前若时钟没有被停止则执行tempSubmit()
}
function tempSubmit(){
    //提交温度给后端（提交当前显示在温度调节器的目标温度即可）
    axiosInstance.post('temperature/',{roomid: roomid,temp: targetTemp})
    .then(response =>{
        submit = 1;
        console.log(response.data);
    })
    .catch(error =>{
        console.log("error");
    });
}
function coolButton(){//制冷
    //制冷按钮颜色由灰色到蓝色
    //（也许可以在css里制作两套button属性，一个代表关闭按钮时的，一个代表打开时的）
    //然后这个函数修改button class就行
}
function heatButton(){//制热
    //制热按钮颜色由灰色到红色
}
function clearWindCssEcp(windspeed){

}

function windspeedAdjust(){//风速调节
    //被选中风速条从低到该风速条显示颜色，其余为灰色
    //显示当前风速
    document.getElementById('low_speed_button').classList.add("clicked");
    document.getElementById('middle_speed_button').classList.add("clicked")
    document.getElementById('high_speed_button').classList.add("clicked")
    if(this.id == 'low_speed_button'){
        var windspeed = 0;
        document.getElementById('middle_speed_button').classList.remove("clicked")
        document.getElementById('high_speed_button').classList.remove("clicked")
    }else if(this.id == 'middle_speed_button'){
        var windspeed = 1;
        document.getElementById('high_speed_button').classList.remove("clicked")
    }else{
        var windspeed = 2;
    }
    axiosInstance.post('windSpeed/',{roomid: roomid,windspeed: windspeed})
    .then(function(response){
        if(response.data.code == 1){
            //待补充
        }
    })
    .catch(error =>{
        console.log("getExp error");
    });
}
function requestExp(){
    axiosInstance.get('getExpenses/',{params: {roomid: roomid}})
    .then(function(response){
        document.getElementById('expenses').textContent = String(response.data.expenses);
    })
    .catch(error =>{
        console.log("getExp error");
    });
}
function requestRoomtemp(){
    axiosInstance.get('roomTemp/',{params: {roomid: roomid}})
    .then(function(response){
        document.getElementById('roomtemp').textContent = String(response.data.roomTemp);
    })
    .catch(error =>{
        console.log("getRoomTemp error");
    });
}
function requestStatus(Roomid){
    axiosInstance.get('getStatus/', {params:{roomid: roomid}})
    .then(function (response) {
        var state = response.data.status;
        if (state == 0 && document.getElementById('status').getAttribute('value') == '1' && submit == 1){
            submit = 0;
            ACSwitch();
        }
    })
    .catch(function (error) {
        console.log("getStatus error at room: " + String(roomid));
    });
}
function ACSwitch(){//空调开关机（以关机->开机为例）
    var status = document.getElementById('status');
    if(status.getAttribute('value')=='0'){
        status.setAttribute('value','1');
        //开机并发送当前房间温度给后端
        axiosInstance.post('boot/',{roomid: roomid,temp: temp})
        .then(function(response){
            console.log(response)
            getStatus = setInterval(requestStatus,1000);
        })
        .catch(error =>{
            console.log("error");
        });
        btnFuncAdd();
        bootfront();
    }else{
        clearInterval(getStatus);
        status.setAttribute('value','0');
        btnFuncCease();
        shutdownfront();
        axiosInstance.post('shutdown/',{roomid: roomid})
        .then(response =>{
            console.log(response.data);
        })
        .catch(error =>{
            console.log("error");
        });
    }
}
function init(){
//通信
    getExp = setInterval(requestExp,1000);//请求累计费用及房间温度
    getRoomtemp = setInterval(requestRoomtemp,1000);
    //getStatus = setInterval(requestStatus,1000);

}
function test(){
}
var temp = 21;//初始房间温度
var targetTemp = 26;//缺省目标温度
var tempTimer,getExp,getRoomtemp,getStatus;
var roomid = 1;
var submit = 0;
init();