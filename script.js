function updateCountdown() {
  const target = new Date("2025-11-30T00:00:00");
  const now = new Date();
  const diff = target - now;
  if (diff <= 0) {
    document.getElementById("countdown").innerText = "💞 Hôm nay là ngày trọng đại của chúng ta 💞";
    return;
  }
  const d = Math.floor(diff / (1000*60*60*24));
  const h = Math.floor((diff / (1000*60*60)) % 24);
  const m = Math.floor((diff / (1000*60)) % 60);
  const s = Math.floor((diff / 1000) % 60);
  document.getElementById("countdown").innerText = `💍 Còn ${d} ngày ${h} giờ ${m} phút ${s} giây 💍`;
}
setInterval(updateCountdown, 1000);
updateCountdown();

function submitChoice(choice) {
  const guest = document.getElementById("guestName").innerText;

  fetch("/submit", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ guest, choice })
  }).then(() => {
    if (choice.includes("Tham gia")) {
      window.open("https://www.google.com/maps/place/Th%C3%B4n+6,+B%E1%BA%AFc+S%C6%A1n,+An+D%C6%B0%C6%A1ng,+H%E1%BA%A3i+Ph%C3%B2ng/", "_blank");
    } else {
      document.getElementById("popup").style.display = "block";
    }
  });
}

function closePopup() {
  document.getElementById("popup").style.display = "none";
}

const heartsContainer = document.getElementById("hearts-container");
function createHeart() {
  const heart = document.createElement("div");
  heart.classList.add("heart");
  const symbols = ["💗", "🌸", "🌿", "🌼", "💚"];
  heart.innerText = symbols[Math.floor(Math.random() * symbols.length)];
  heart.style.left = Math.random() * 100 + "vw";
  heart.style.animationDuration = (3 + Math.random() * 2) + "s";
  heartsContainer.appendChild(heart);
  setTimeout(() => heart.remove(), 5000);
}
setInterval(createHeart, 300);

const music = document.getElementById("bgMusic");
function initMusic() {
  music.play().catch(()=>{});
}
