/*通信*/
const axiosInstance = axios.create({
    baseURL: 'http://127.0.0.1:8000', // 设置后端 API 地址
    headers: {
        'Content-Type': 'application/json' // 设置请求头
    }
});
/*
function RequestTargetTemp(roomid){
    return new Promise(function (resolve,reject){
      axios.get('targetTemp/',{roomid: roomid})
      .then(function(response){
          if(response.data.code == 1){
              document.getElementsByClassName(roomid)[0].getElementsByClassName('targetTemp')[0].textContent = String(response.data.Targettemp);
          }
      })
      .catch(error =>{
          console.log("getTargetTemp error at room: " + String(roomid));
      });  
    });
}
function requestRoomtemp(roomid){
    return new Promise(function (resolve,reject){
        axios.get('roomTemp/',{roomid: roomid})
        .then(function(response){
            if(response.data.code == 1){
                document.getElementsByClassName(roomid).getElementsByClassName('roomTemp')[0].textContent = String(response.data.roomtemp);
            }
        })
        .catch(error =>{
            console.log("getRoomTemp error at room: " + String(roomid));
        }); 
    });
}*/

function RequestTargetTemp(Roomid){
    axios.get('targetTemp',{params:{roomid: Roomid}})
    .then(function(response){
            document.getElementsByClassName(Roomid)[0].getElementsByClassName('targetTemp')[0].textContent = String(response.data.targetTemp);
    })
    .catch(error =>{
        console.log("getTargetTemp error at room: " + String(Roomid));
    });
}
function requestRoomtemp(Roomid){
    axios.get('roomTemp',{params:{roomid: Roomid}})
    .then(function(response){
            document.getElementsByClassName(Roomid)[0].getElementsByClassName('roomTemp')[0].textContent = String(response.data.roomTemp);
    })
    .catch(error =>{
        console.log("getRoomTemp error at room: " + String(Roomid));
    }); 
}
/*动画效果*/
function mouseon(){
    this.classList.add("active");
    this.classList.remove("text-white");
}
function mouseleave(){
    this.classList.add("text-white");
    this.classList.remove("active");
}

/*初始化*/
var rownum = 1;
var colnum = 3;
var update;
var roomid = 1;
function init(){
    let template = document.getElementById("pannel");
    for (let r = 0; r < rownum; r++){
        table = document.getElementById('monitor-table').getElementsByClassName("ctable")[r];
        for(let c = 0;c < colnum;c++){
            //模板只能导入一次，因此每次都复制一份
            var tem = template.content.cloneNode(true);
            //修改模板房间号
            var room = tem.getElementById("room");
            room.textContent = String(c+1) + "号客房";
            var col = document.createElement("div");
            col.setAttribute("class","col " + String(c+1));
            col.appendChild(tem);
            table.appendChild(col);
        }       
    }
    updateData();
}
function updateData(){
    clearInterval(update);
    for (let r = 0; r < rownum; r++){
        for(let c = 0;c < colnum;c++){
            requestRoomtemp(c + 1);
            RequestTargetTemp(c + 1);
        }       
    }

    setInterval(update,2000);
}
/*
fetch('monitor.html').then(Response => Response.text())
.then(data =>{
    init();
})*/