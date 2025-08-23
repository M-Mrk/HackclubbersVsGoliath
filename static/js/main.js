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

function startFireballAnimation() {
    const fireball = document.getElementById("fireball");
    if (fireball) {
        // Reset any previous animation
        if (fireball.classList.contains("animate-fireballAttack")) {
            fireball.classList.remove("animate-fireballAttack");
            void fireball.offsetWidth;
        }

        // Make fireball visible and start animation
        fireball.style.opacity = '1';
        fireball.classList.add("animate-fireballAttack");

        // Hide fireball after animation completes
        setTimeout(() => {
            fireball.style.opacity = '0';
            fireball.classList.remove("animate-fireballAttack");
        }, 1000);
    }
}

function startPlayerWeakAttackAnimation() {
    startFireballAnimation();
    setTimeout(() => {
        showExplosion();
    }, 900);
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

function showExplosion() {
    const explosions = ['explosion1'];
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
    fetch("/api/attack", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ type: "strong" })
    }).then(response => {
        if (!response.ok) {
            console.error("Failed to send attack");
        } else {
            console.log("Attack sent successfully.");
            startPlayerAttackAnimation();
            attackCycle(true);
            setTimeout(() => {
                showExplosions();
                monsterCycle(true);
            }, 2250);
        }
    }).catch(error => {
        console.error("Error sending attack:", error);
    });
}

function arduinoMap(value, in_min, in_max, out_min, out_max) {
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

let lastSetMonsterHealth = null;
let firstRun = true;
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
    if (firstRun) {
        firstRun = false;
        return;
    }
    healthNumber.classList.add("animate-healthChange");
    setTimeout(() => {
        healthNumber.classList.remove("animate-healthChange");
    }, 1000);
}

async function getPlayerAttackStatus() {
    const response = await fetch("/api/attack", {
        method: "GET"
    });
    if (response.ok) {
        const monster = await response.json();
        console.log(monster);
        return monster;
    } else {
        console.error("Failed to fetch attack info");
        return null;
    }
}

function setStrongAttackStatus(attack) {
    const strongAttackStatus = document.getElementById("strongAttackStatus");
    if (strongAttackStatus) {
        strongAttackStatus.classList.remove("bg-green-200", "bg-red-200");
        if (attack.status === "ready") {
            strongAttackStatus.classList.add("bg-green-200");
            strongAttackStatus.textContent = "Ready";
        } else {
            strongAttackStatus.classList.add("bg-red-200");
            if (attack.time_left > 22) {
                time_left = attack.time_left + 1;
            } else {
                time_left = attack.time_left;
            }
            strongAttackStatus.textContent = "Ready in " + time_left + "h";
        }
    }
}

function setWeakAttackStatus(percentage) {
    const weakAttackStatus = document.getElementById("weakAttackStatus");
    if (weakAttackStatus) {
        const progressBar = weakAttackStatus.querySelector("div");
        if (progressBar) {
            const clampedPercentage = Math.max(0, Math.min(100, percentage));

            weakAttackStatus.style.justifyContent = "flex-start";

            if (clampedPercentage === 0) {
                progressBar.style.width = "0%";
                progressBar.style.opacity = "0";
            } else {
                progressBar.style.width = clampedPercentage + "%";
                progressBar.style.opacity = "1";
            }
        }
    }
}

let weakAttackActive = true;
function disableWeakAttack() {
    weakAttackActive = false;
    const weakAttackButton = document.getElementById("weakAttackButton");
    if (weakAttackButton) {
        weakAttackButton.classList.remove("bg-green-600");
        weakAttackButton.classList.remove("hover:bg-green-700");
        weakAttackButton.classList.add("bg-gray-300");
    }
    setWeakAttackStatus(0);
    const weakAttackStatus = document.getElementById("weakAttackStatus");
    if (weakAttackStatus) {
        weakAttackStatus.innerText = "On Cooldown...";
    }
}

function enableWeakAttack() {
    console.log("Enabling weak attack");
    weakAttackActive = true;
    const weakAttackButton = document.getElementById("weakAttackButton");
    if (weakAttackButton) {
        weakAttackButton.classList.add("bg-green-600");
        weakAttackButton.classList.add("hover:bg-green-700");
        weakAttackButton.classList.remove("bg-gray-300");
    }

    const weakAttackStatus = document.getElementById("weakAttackStatus");
    if (weakAttackStatus) {
        weakAttackStatus.innerText = "";
        const gradientBar = document.createElement("div");
        gradientBar.className = "w-full h-4 bg-gradient-to-r from-blue-500 to-purple-500 rounded";
        weakAttackStatus.appendChild(gradientBar);
        setWeakAttackStatus(0);
    }
}

let weakCharge = 0;
function weakAttack() {
    if (!weakAttackActive) return;
    if (weakCharge < 100) {
        weakCharge += 2;
        setWeakAttackStatus(weakCharge);
    } else {
        weakCharge = 0;
        fetch("/api/attack", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ type: "weak" })
        }).then(response => {
            if (!response.ok) {
                console.error("Failed to send weak attack");
            } else {
                console.log("weak Attack sent successfully.");
                disableWeakAttack();
                startPlayerWeakAttackAnimation();
                attackCycle(true);
                setTimeout(() => {
                    showExplosion();
                    monsterCycle(true);
                }, 2250);
                setTimeout(() => {
                    enableWeakAttack();
                }, 25000);
            }
        }).catch(error => {
            console.error("Error sending weak attack:", error);
        });
    }
}

async function attackCycle(runOnce = false) {
    const attack = await getPlayerAttackStatus();
    if (attack) {
        console.log(attack);
        setStrongAttackStatus(attack);
    }

    if (!runOnce) {
        setTimeout(() => {
            attackCycle();
        }, 15000);
    }
}

async function monsterCycle(runOnce = false) {
    const monster = await getMonsterInfo();
    const noPeaceContainer = document.getElementById("NonPeaceContainer");
    const peaceContainer = document.getElementById("PeaceContainer");
    if (monster) {
        if (!monster.peace) {
            if (noPeaceContainer.classList.contains("hidden")) {
                noPeaceContainer.classList.remove("hidden");
            }
            if (!peaceContainer.classList.contains("hidden")) {
                peaceContainer.classList.add("hidden");
            }
            setMonsterSrc(monster);
            setMonsterName(monster);
            startIdleMonsterAnimation();
            setMonsterHealth(monster.health, monster.max_health);
        } else {
            if (!noPeaceContainer.classList.contains("hidden")) {
                noPeaceContainer.classList.add("hidden");
            }
            if (peaceContainer.classList.contains("hidden")) {
                peaceContainer.classList.remove("hidden");
            }
        }
    }

    if (!runOnce) {
        setTimeout(() => {
            monsterCycle();
        }, 15000);
    }
}

async function getLastAttacks() {
    const response = await fetch("/api/last_attacks");
    if (!response.ok) {
        console.error("Failed to fetch last attacks");
        return [];
    }
    return await response.json();
}

async function setLastAttacks() {
    const lastAttackTableBody = document.getElementById("lastAttackTableBody");
    if (!lastAttackTableBody) return;

    const lastAttacks = await getLastAttacks();
    lastAttackTableBody.innerHTML = "";
    for (const attack of lastAttacks) {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td class="border border-gray-300 px-16 py-1" >${attack.type}</td>
            <td class="border border-gray-300 px-16 py-1" >${attack.time_ago}</td>
        `;
        lastAttackTableBody.appendChild(row);
    }
}

document.addEventListener("DOMContentLoaded", async () => {
    setWeakAttackStatus(0);
    attackCycle();
    monsterCycle();
    setLastAttacks();
});