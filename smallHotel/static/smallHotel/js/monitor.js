/*通信*/
const axiosInstance = axios.create({
    baseURL: 'http://127.0.0.1:8000/smallHotel/mon/', // 设置后端 API 地址
    headers: {
        'Content-Type': 'application/json' // 设置请求头
    }
});
/*
function RequestTargetTemp(Roomid){
    axiosInstance.post('targetTemp/',{roomid: Roomid})
    .then(function(response){
            document.getElementsByClassName(Roomid)[0].getElementsByClassName('targetTemp')[0].textContent = String(response.data.targetTemp);
    })
    .catch(error =>{
        console.log("getTargetTemp error at room: " + String(Roomid));
    });
}
*/
function RequestTargetTemp(Roomid){
    axiosInstance.get('targetTemp/',{params:{roomid: Roomid}})
    .then(function(response){
            document.getElementsByClassName(Roomid)[0].getElementsByClassName('targetTemp')[0].textContent = String(response.data.targetTemp);
    })
    .catch(error =>{
        console.log("getTargetTemp error at room: " + String(Roomid));
    });
}
function RequestRoomtemp(Roomid){
    //{params:{roomid: Roomid}}
    axiosInstance.get('roomTemp/',{params:{roomid: Roomid}})
    .then(function(response){
            document.getElementsByClassName(Roomid)[0].getElementsByClassName('roomTemp')[0].textContent = String(response.data.roomTemp);
            //console.log(document.getElementsByClassName(Roomid)[0].getElementsByClassName('roomTemp')[0])
    })
    .catch(error =>{
        console.log("getRoomTemp error at room: " + String(Roomid));
    }); 
}
function RequestSpeed(Roomid){
    axiosInstance.get('getSpeed/',{params:{roomid: Roomid}})
    .then(function(response){
            var speed = response.data.windSpeed
            //document.getElementsByClassName(Roomid)[0].getElementsByClassName('Speed')[0].textContent = String(response.data.roomTemp);
            document.getElementsByClassName(Roomid)[0].getElementsByClassName('Speed')[speed].classList.add("mark");
    })
    .catch(error =>{
        console.log("getWindSpeed error at room: " + String(Roomid));
    }); 
}
function RequestStatus(Roomid){
    return new Promise(function (resolve, reject) {
        axiosInstance.get('getStatus/', {params:{roomid: Roomid}})
            .then(function (response) {
                var status = response.data.status;
                if (status == 1){
                    document.getElementsByClassName(Roomid)[0].getElementsByClassName('boot')[0].classList.add("text-danger");
                }
                resolve(status);
            })
            .catch(function (error) {
                reject(error)
                console.log("getStatus error at room: " + String(Roomid));
            });
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
var rownum = 2;
var colnum = 3;
var update;
function init(){
    let template = document.getElementById("pannel");
    for (let r = 0; r < rownum; r++){
        table = document.getElementById('monitor-table').getElementsByClassName("ctable")[r];
        for(let c = 0;c < colnum;c++){
            //模板只能导入一次，因此每次都复制一份
            var tem = template.content.cloneNode(true);
            //修改模板房间号
            var room = tem.getElementById("room");
            room.textContent = String(r * 3 + c + 1) + "号客房";
            var col = document.createElement("div");
            col.setAttribute("class","col " + String(r * 3 + c + 1));
            col.appendChild(tem);
            table.appendChild(col);
        }       
    }
    updateData();
}

function clear(){
    for (let r = 0; r < rownum; r++){
        for(let c = 0;c < colnum;c++){
            document.getElementsByClassName(r * 3 + c + 1)[0].getElementsByClassName('targetTemp')[0].textContent = '-';
            document.getElementsByClassName(r * 3 + c + 1)[0].getElementsByClassName('roomTemp')[0].textContent = '-';
            document.getElementsByClassName(r * 3 + c + 1)[0].getElementsByClassName('boot')[0].classList.remove("text-danger");
            for(let d = 0;d < 3;d++){
                document.getElementsByClassName(r * 3 + c + 1)[0].getElementsByClassName('Speed')[d].classList.remove("mark");
            }     
        }       
    }
}
async function updateData(){
    clearInterval(update);
    clear();
    for (let r = 0; r < rownum; r++){
        for(let c = 0;c < colnum;c++){
            var status = await RequestStatus(r * 3 + c + 1);  
            if(status){//若已开机，则更新内容
                RequestRoomtemp(r * 3 + c + 1);
                RequestTargetTemp(r * 3 + c + 1);
                RequestSpeed(r * 3 + c + 1);
            }
        }       
    }
    update = setInterval(updateData,2000);
    /*
    RequestRoomtemp(r * 3 + c + 1);
    RequestTargetTemp(r * 3 + c + 1);
    RequestSpeed(r * 3 + c + 1);
    RequestStatus(r * 3 + c + 1)
    */
    //update = setInterval(clear,2000);
}

