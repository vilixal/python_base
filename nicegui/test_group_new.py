from nicegui import ui

master_data = [
    {'name': 'ГПБ', 'status': 'Саппорт', 'servers': [
        {'server': 'app1', 'status': 'Работает'},
        {'server': 'app2', 'status': 'Не работает'},
    ]},
    {'name': 'Совкомбанк', 'status': 'Отказался', 'servers': [
        {'server': 'app1', 'status': 'Не работает'},
    ]},
    {'name': 'ВТБ', 'status': 'Активен', 'servers': [
        {'server': 'app1', 'status': 'Работает'},
        {'server': 'app2', 'status': 'Работает'},
        {'server': 'app3', 'status': 'Работает'},
    ]},
]

html_code = f'''
<style>
    .bank-table {{
        width: 100%;
        border-collapse: collapse;
        background: white;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }}
    .bank-table th {{
        background-color: #f3f4f6;
        padding: 12px;
        text-align: left;
        font-weight: bold;
        border-bottom: 2px solid #e5e7eb;
    }}
    .bank-table td {{
        padding: 12px;
        border-bottom: 1px solid #e5e7eb;
    }}
    .bank-row {{
        cursor: pointer;
        transition: background-color 0.2s;
    }}
    .bank-row:hover {{
        background-color: #f9fafb;
    }}
    .status-badge {{
        display: inline-block;
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 12px;
        font-weight: bold;
        color: white;
    }}
    .status-sapport {{ background-color: #3b82f6; }}
    .status-rejected {{ background-color: #ef4444; }}
    .status-active {{ background-color: #10b981; }}
    .detail-row {{
        background-color: #f9fafb;
    }}
    .detail-content {{
        padding: 10px;
    }}
    .servers-table {{
        width: 90%;
        margin: 0 auto;
        border-collapse: collapse;
        background: white;
        border-radius: 4px;
    }}
    .servers-table th {{
        background-color: #e5e7eb;
        padding: 8px;
        text-align: left;
        font-size: 13px;
    }}
    .servers-table td {{
        padding: 8px;
        border-bottom: 1px solid #e5e7eb;
    }}
    .status-working {{ color: #10b981; font-weight: bold; }}
    .status-not-working {{ color: #ef4444; font-weight: bold; }}
    .toggle-icon {{
        display: inline-block;
        margin-right: 8px;
        transition: transform 0.2s;
        font-size: 12px;
    }}
    .toggle-icon.expanded {{
        transform: rotate(90deg);
    }}
</style>

<table class="bank-table" id="bankTable">
    <thead>
        <tr>
            <th>Название банка</th>
            <th>Статус</th>
        </tr>
    </thead>
    <tbody id="bankTableBody">
    </tbody>
</table>

<script>
    const bankData = {master_data};
    let expandedRows = {{}};

    function toggleRow(bankName) {{
        expandedRows[bankName] = !expandedRows[bankName];
        renderTable();
    }}

    function getStatusClass(status) {{
        if (status === 'Саппорт') return 'status-sapport';
        if (status === 'Отказался') return 'status-rejected';
        return 'status-active';
    }}

    function renderTable() {{
        const tbody = document.getElementById('bankTableBody');
        tbody.innerHTML = '';

        bankData.forEach(bank => {{
            const isExpanded = expandedRows[bank.name];

            // Основная строка
            const row = tbody.insertRow();
            row.className = 'bank-row';
            row.onclick = () => toggleRow(bank.name);

            // Ячейка с названием банка и иконкой
            const nameCell = row.insertCell(0);
            const icon = document.createElement('span');
            icon.className = `toggle-icon ${{isExpanded ? 'expanded' : ''}}`;
            icon.textContent = '▶';
            nameCell.appendChild(icon);
            nameCell.appendChild(document.createTextNode(bank.name));

            // Ячейка со статусом
            const statusCell = row.insertCell(1);
            const statusBadge = document.createElement('span');
            statusBadge.className = `status-badge ${{getStatusClass(bank.status)}}`;
            statusBadge.textContent = bank.status;
            statusCell.appendChild(statusBadge);

            // Детальная строка
            if (isExpanded && bank.servers && bank.servers.length > 0) {{
                const detailRow = tbody.insertRow();
                detailRow.className = 'detail-row';
                const detailCell = detailRow.insertCell(0);
                detailCell.colSpan = 2;
                detailCell.className = 'detail-content';

                // Таблица серверов
                let serversHtml = `
                    <table class="servers-table">
                        <thead>
                            <tr><th>Сервер</th><th>Статус</th</tr>
                        </thead>
                        <tbody>
                `;

                bank.servers.forEach(server => {{
                    const statusClass = server.status === 'Работает' ? 'status-working' : 'status-not-working';
                    serversHtml += `
                        <tr>
                            <td>${{server.server}}</td>
                            <td class="${{statusClass}}">${{server.status}}</td>
                        </tr>
                    `;
                }});

                serversHtml += '</tbody></table>';
                detailCell.innerHTML = serversHtml;
            }}
        }});
    }}

    renderTable();
</script>
'''

ui.add_body_html(html_code)
ui.run()