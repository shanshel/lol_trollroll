let championsList = [];
let championIdMap = {};
let ddragonVersion = '14.8.1'; // Fallback
let slots = [];
const container = document.getElementById('slots-container');
const addCard = document.getElementById('add-card');

async function init() {
  try {
    // 1. Get latest DDragon version
    const versionRes = await fetch('https://ddragon.leagueoflegends.com/api/versions.json');
    const versions = await versionRes.json();
    ddragonVersion = versions[0];
    
    // 2. Get champion data for mapping names to IDs
    const champDataRes = await fetch(`https://ddragon.leagueoflegends.com/cdn/${ddragonVersion}/data/en_US/champion.json`);
    const champData = await champDataRes.json();
    
    // Create mapping: "Aatrox" -> "Aatrox"
    Object.values(champData.data).forEach(champ => {
      championIdMap[champ.name] = champ.id;
    });

    // 3. Load our local list (which includes 2026 champs)
    const response = await fetch('./champions.json');
    const data = await response.json();
    championsList = data.champions;
    
    addSlot();
    setupEventListeners();
  } catch (error) {
    console.error('Error loading champions:', error);
    // Fallback if APIs fail
    const response = await fetch('./champions.json');
    const data = await response.json();
    championsList = data.champions;
    addSlot();
    setupEventListeners();
  }
}

function setupEventListeners() {
  document.getElementById('randomize-btn').addEventListener('click', randomize);
  document.getElementById('reset-btn').addEventListener('click', resetAll);
  addCard.addEventListener('click', addSlot);
}

function addSlot() {
  if (slots.length >= 5) return;
  
  const id = Date.now();
  const slotEl = document.createElement('div');
  slotEl.className = 'champion-slot';
  slotEl.setAttribute('data-empty', 'true');
  slotEl.innerHTML = `
    <button class="remove-slot" title="Remove Slot">×</button>
    <div class="card-inner">
        <span class="lock-status">UNLOCKED</span>
        <div class="icon-placeholder">
          <img src="" class="champ-img" style="display: none;">
          <span class="placeholder-char">?</span>
        </div>
        <div class="name">EMPTY</div>
    </div>
  `;
  
  const slot = {
    id: id,
    el: slotEl,
    name: 'EMPTY',
    locked: false
  };
  
  slotEl.querySelector('.card-inner').addEventListener('click', () => toggleLock(slot));
  slotEl.querySelector('.remove-slot').addEventListener('click', (e) => {
    e.stopPropagation();
    removeSlot(slot);
  });
  
  container.insertBefore(slotEl, addCard);
  slots.push(slot);
  updateAddButtonState();
}

function removeSlot(slot) {
  if (slots.length <= 1) return;
  slot.el.style.opacity = '0';
  slot.el.style.transform = 'scale(0.8)';
  setTimeout(() => {
    container.removeChild(slot.el);
    slots = slots.filter(s => s.id !== slot.id);
    updateAddButtonState();
  }, 300);
}

function updateAddButtonState() {
  addCard.style.display = slots.length >= 5 ? 'none' : 'block';
}

function toggleLock(slot) {
  slot.locked = !slot.locked;
  slot.el.classList.toggle('locked', slot.locked);
  slot.el.querySelector('.lock-status').textContent = slot.locked ? 'LOCKED' : 'UNLOCKED';
}

async function randomize() {
  const randomizeBtn = document.getElementById('randomize-btn');
  if (randomizeBtn.disabled) return;
  
  const unlockedSlots = slots.filter(s => !s.locked);
  if (unlockedSlots.length === 0) return;

  randomizeBtn.disabled = true;
  unlockedSlots.forEach(s => s.el.classList.add('rolling'));

  // Snappy name cycling (Faster: 100ms)
  for (let step = 0; step < 10; step++) {
    unlockedSlots.forEach(s => {
      const tempName = championsList[Math.floor(Math.random() * championsList.length)];
      // Fast UI update: Just text during roll
      const nameEl = s.el.querySelector('.name');
      const imgEl = s.el.querySelector('.champ-img');
      const placeholderEl = s.el.querySelector('.placeholder-char');
      
      nameEl.textContent = tempName;
      imgEl.style.display = 'none';
      placeholderEl.style.display = 'block';
      placeholderEl.textContent = tempName.charAt(0);
    });
    await new Promise(r => setTimeout(r, 100));
  }

  unlockedSlots.forEach(s => s.el.classList.remove('rolling'));
  
  const lockedNames = slots.filter(s => s.locked).map(s => s.name);
  let availableChampions = championsList.filter(name => !lockedNames.includes(name));
  availableChampions.sort(() => 0.5 - Math.random());
  
  unlockedSlots.forEach((s, i) => {
    const finalName = availableChampions[i];
    s.name = finalName;
    updateSlotUI(s, finalName);
    s.el.classList.add('final-pop');
    setTimeout(() => s.el.classList.remove('final-pop'), 600);
  });

  randomizeBtn.disabled = false;
}

function updateSlotUI(slot, name) {
  const nameEl = slot.el.querySelector('.name');
  const imgEl = slot.el.querySelector('.champ-img');
  const placeholderEl = slot.el.querySelector('.placeholder-char');
  
  nameEl.textContent = name;
  slot.el.setAttribute('data-empty', name === 'EMPTY' ? 'true' : 'false');

  if (name === 'EMPTY') {
    imgEl.style.display = 'none';
    placeholderEl.style.display = 'block';
    placeholderEl.textContent = '?';
  } else {
    const champId = championIdMap[name];
    if (champId) {
      imgEl.src = `https://ddragon.leagueoflegends.com/cdn/${ddragonVersion}/img/champion/${champId}.png`;
      imgEl.style.display = 'block';
      placeholderEl.style.display = 'none';
    } else {
      // Fallback for new/2026 champs not in DDragon
      imgEl.style.display = 'none';
      placeholderEl.style.display = 'block';
      placeholderEl.textContent = name.charAt(0);
    }
  }
}

function resetAll() {
  slots.forEach(s => {
    s.locked = false;
    s.name = 'EMPTY';
    s.el.classList.remove('locked');
    s.el.setAttribute('data-empty', 'true');
    s.el.querySelector('.lock-status').textContent = 'UNLOCKED';
    updateSlotUI(s, 'EMPTY');
  });
}

init();
