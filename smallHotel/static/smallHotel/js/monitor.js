/*通信*/
/*
const axiosInstance = axios.create({
    baseURL: 'http://127.0.0.1:8000', // 设置后端 API 地址
    headers: {
        'Content-Type': 'application/json' // 设置请求头
    }
});
*/
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
function init(){
    let template = document.getElementById("pannel");
    for (let r = 0; r < 2; r++){
        table = document.getElementById('monitor-table').getElementsByClassName("ctable")[r];
        //console.log(table) 
        for(let c = 0;c < 3;c++){
            //模板只能导入一次，因此每次都复制一份
            var tem = template.content.cloneNode(true);
            //修改模板房间号
            var room = tem.getElementById("room");
            room.textContent = String(c+1) + "号客房";
            var col = document.createElement("div");
            col.setAttribute("class","col");
            col.appendChild(tem);
            table.appendChild(col);
        }       
    }
}
/*
fetch('monitor.html').then(Response => Response.text())
.then(data =>{
    init();
})*/