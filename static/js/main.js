async function getMonsterInfo() {
    const response = await fetch("/api/monster");
    if (response.ok) {
        const monster = await response.json();
        console.log(monster);
        return monster;
    } else {
        console.error("Failed to fetch monster info");
        return null;
    }
}

function setMonsterSrc(monster) {
    const monsterImage = document.getElementById("currentMonster");
    if (monster.url) {
        currentSrc = monsterImage.src;
        if (currentSrc !== monster.url) {
            monsterImage.src = monster.url;
        }
    }
}

function setMonsterName(monster) {
    const monsterNameLabel = document.getElementById("monsterNameLabel");
    if (monster.name) {
        monsterNameLabel.textContent = monster.name;
        monsterNameLabel.classList.remove("hidden");
    }
}

function startIdleMonsterAnimation() {
    const monsterImage = document.getElementById("currentMonster");
    monsterImage.classList.add("animate-monsterIdle");
}

function stopIdleMonsterAnimation() {
    const monsterImage = document.getElementById("currentMonster");
    monsterImage.classList.remove("animate-monsterIdle");
}

function startPlayerAttackAnimation() {
    const playerImage = document.getElementById("Player");
    if (playerImage.classList.contains("animate-playerAttack")) {
        playerImage.classList.remove("animate-playerAttack");
        void playerImage.offsetWidth;
    }

    playerImage.classList.add("animate-playerAttack");
}

function showExplosions() {
    const explosions = ['explosion1', 'explosion2', 'explosion3'];
    const explosionGifUrl = "/static/images/Explosion.gif";

    explosions.forEach((explosionId, index) => {
        const explosion = document.getElementById(explosionId);
        if (explosion) {
            setTimeout(() => {
                explosion.style.opacity = '1';
                explosion.src = explosionGifUrl + "?t=" + Date.now();

                setTimeout(() => {
                    explosion.style.opacity = '0';
                }, 5000);
            }, index * 200);
        }
    });
}

function playerAttack() {
    startPlayerAttackAnimation();
    setTimeout(() => {
        showExplosions();
    }, 2250);
}

function arduinoMap(value, in_min, in_max, out_min, out_max) {
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

let lastSetMonsterHealth = null;
function setMonsterHealth(health, maxHealth) {
    if (lastSetMonsterHealth === health) return;
    lastSetMonsterHealth = health;

    const healthBar = document.getElementById("MonsterHealth")
    if (healthBar) {
        healthBar.innerHTML = '';

        const healthPercentage = arduinoMap(health, in_min = 0, in_max = maxHealth, out_min = 0, out_max = 21);
        console.log(`Setting monster health: ${health} / ${maxHealth} (${healthPercentage})`);
        for (let i = healthPercentage; i > 0; i--) {
            const healthDiv = document.createElement("div");
            healthDiv.className = "health";
            healthBar.appendChild(healthDiv);
        }
    }

    const healthNumber = document.getElementById("MonsterHealthNumber");
    if (healthNumber) {
        healthNumber.textContent = `${health} / ${maxHealth}`;
    }
}

document.addEventListener("DOMContentLoaded", async () => {
    const monster = await getMonsterInfo();
    if (monster) {
        setMonsterSrc(monster);
        setMonsterName(monster);
        startIdleMonsterAnimation();
        setMonsterHealth(monster.health, monster.max_health);
    }
});