const axiosInstance = axios.create({
    baseURL: 'http://127.0.0.1:8000', // 设置后端 API 地址
    headers: {
        'Content-Type': 'application/json' // 设置请求头
    }
});

function tempAdd(){//空调升温
    clearTimeout(mytimer);
    //点击后先停止上一个时钟
    targetTemp = targetTemp + 1;
    //目标温度+1
    console.log(targetTemp);        //需要修改
    //显示在温度调节器上
    mytimer = setTimeout(tempSubmit,2000);
    //计时，计时结束前若时钟没有被停止则执行tempSubmit()
}
function tempSub(){//空调降温
    clearTimeout(mytimer);
    //点击后先停止上一个时钟
    targetTemp = targetTemp - 1;
    //目标温度-1
    console.log(targetTemp);        //需要修改
    //显示在温度调节器上
    mytimer = setTimeout(tempSubmit,2000);
    //计时，计时结束前若时钟没有被停止则执行tempSubmit()
}
function tempSubmit(){
    //用表单的方式提交温度给后端（提交当前显示在温度调节器的目标温度即可）
    axios.post('/cus/temperature/',{roomid: roomid,temp: targetTemp})
    .then(response =>{
        console.log(response.data);
    })
    .catch(error =>{
        console.error("error");
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
function windspeedAdjust(){//风速调节
    //被选中风速条从低到该风速条显示颜色，其余为灰色
    //显示当前风速
}
function ACSwitch(){//空调开关机（以关机->开机为例）
    //界面
        //修改上方状态栏（关机->运行中）
        //修改温度界面（开空调改为关空调）
        //（隐藏->显示）调温界面或修改调温界面中间元素为（--- -> 26℃）
        //风速栏风速条默认中风速，低中风速涂颜色，风速文字显示
        //目前累计费用（--元 -> 0元）
        //制冷默认打开（调用coolButton）

    //通信
        //发送当前房间温度给后端
}
function test(){
    alert("now temp is" + targetTemp);
}
var temp = 21;//初始房间温度
var targetTemp = 26;//缺省目标温度
var mytimer;
var roomid = 1;

