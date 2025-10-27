function openMap(){window.open("https://www.google.com/maps?q=20.87607,106.5843","_blank");}
function openGift(){document.getElementById("qrPopup").style.display="block";}
function closeGift(){document.getElementById("qrPopup").style.display="none";}

function updateCountdown(){
 const t=new Date("2025-11-30T00:00:00"),n=new Date(),d=t-n;
 if(d<=0)return document.getElementById("countdown").innerText="💞 Hôm nay là ngày trọng đại của chúng ta 💞";
 const a=Math.floor(d/864e5),h=Math.floor(d/36e5%24),m=Math.floor(d/6e4%60),s=Math.floor(d/1e3%60);
 document.getElementById("countdown").innerText=`💍 Còn ${a} ngày ${h} giờ ${m} phút ${s} giây 💍`;
}
setInterval(updateCountdown,1000);updateCountdown();

function submitChoice(c){
 fetch("/submit",{method:"POST",headers:{"Content-Type":"application/json"},
 body:JSON.stringify({guest:document.getElementById("guestName").innerText,choice:c})
 }).then(()=>console.log("Đã ghi phản hồi"));
}

/* tim & hoa */
const heartsContainer=document.getElementById("hearts-container");
function createHeart(){
 const h=document.createElement("div");
 h.classList.add("heart");
 const s=["💗","🌸","🌿","🌼","💚"];
 h.innerText=s[Math.floor(Math.random()*s.length)];
 h.style.left=Math.random()*100+"vw";
 h.style.animationDuration=3+Math.random()*2+"s";
 heartsContainer.appendChild(h);
 setTimeout(()=>h.remove(),5e3);
}
setInterval(createHeart,300);

/* nhạc nền */
const music=document.getElementById("bgMusic");
function initMusic(){music.play().catch(()=>{});}
