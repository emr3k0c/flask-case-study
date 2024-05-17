/* eslint-disable no-unused-vars */
document.addEventListener('DOMContentLoaded', () => {
    const companyUsers = JSON.parse(document.getElementById('company-users-div').getAttribute('data-company-users'));
    const dailyUsers = JSON.parse(document.getElementById('daily-users-graph').getAttribute('data-daily-users'));
    
    const tbody = document.querySelector('#company-users-table tbody');
    JSON.parse(companyUsers).forEach(company => {
        const row = document.createElement('tr');
        
        const nameCell = document.createElement('td');
        nameCell.textContent = company.company_name;
        row.appendChild(nameCell);
        
        const userCountCell = document.createElement('td');
        userCountCell.textContent = company.user_count; 
        row.appendChild(userCountCell);
        
        tbody.appendChild(row);
    });

    const ctx2 = document.getElementById('daily-users-graph').getContext('2d');
    const user_graph = new Chart(ctx2, {
        type: 'line',
        data: {
            labels: Object.keys(JSON.parse(dailyUsers)).map(serial => {
                const date = new Date(new Date(1899, 11, 30).getTime() + serial * 24 * 60 * 60 * 1000);
                return date.toLocaleDateString('en-US', { year: '2-digit', month: '2-digit', day: '2-digit' });
            }),            
            datasets: [{
                label: 'Daily Users',
                data: Object.values(JSON.parse(dailyUsers)),
                backgroundColor: 'rgba(153, 102, 255, 0.2)',
                borderColor: 'rgba(153, 102, 255, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
               
                y: {
                    beginAtZero: true
                }
            }
        }
    });
});
