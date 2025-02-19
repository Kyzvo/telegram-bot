// Имитация загрузки
setTimeout(() => {
    document.getElementById('loader').style.display = 'none';
    document.getElementById('mainContent').style.display = 'block';
}, 2000); // Задержка 2 секунды

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

// Пример данных
document.getElementById('pointsValue').textContent = 100;
document.getElementById('referralLink').textContent = "https://t.me/your_bot?start=ref123";

const tasks = ["Подписаться на канал", "Репостнуть запись"];
const taskList = document.getElementById('taskList');
tasks.forEach(task => {
    const li = document.createElement('li');
    li.textContent = task;
    taskList.appendChild(li);
});