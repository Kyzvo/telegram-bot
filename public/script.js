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
    const user_id = 123; // Замените на реальный ID пользователя
    const response = await fetch(`https://telegram-bot-api-ckw4.onrender.com/api/user?user_id=${user_id}`);
    const data = await response.json();

    if (data.error) {
        console.error(data.error);
        return;
    }

    // Отображаем данные
    document.getElementById('pointsValue').textContent = data.points;
    document.getElementById('referralLink').textContent = data.referral_link;

    const referralList = document.getElementById('referralList');
    referralList.innerHTML = data.referrals.map(ref => `
        <li>Пользователь ${ref.user_id} (Уровень ${ref.level})</li>
    `).join('');
}

loadData();
