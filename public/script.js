// Имитация загрузки
setTimeout(() => {
    document.getElementById('loader').style.display = 'none';
    document.getElementById('mainContent').style.display = 'block';
}, 2000);

// Переключение вкладок
const tabs = document.querySelectorAll('.tab-button');
const panes = document.querySelectorAll('.tab-pane');

tabs.forEach((tab, index) => {
    tab.addEventListener('click', () => {
        tabs.forEach(t => t.classList.remove('active'));
        panes.forEach(p => p.classList.remove('active'));

        tab.classList.add('active');
        panes[index].classList.add('active');
    });
});

// Загрузка данных
async function loadData() {
    const response = await fetch('/api/user'); // Замените на ваш API
    const data = await response.json();

    document.getElementById('pointsValue').textContent = data.points;
    document.getElementById('referralLink').textContent = data.referral_link;

    const referralList = document.getElementById('referralList');
    referralList.innerHTML = data.referrals.map(ref => `
        <li>${ref.username} (Уровень ${ref.level})</li>
    `).join('');
}

loadData();
