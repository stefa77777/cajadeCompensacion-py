        const stackData = []; // Pila
        const queueData = []; // Cola
        const listData = [];  // Lista

        document.getElementById('affiliationDate').valueAsDate = new Date();

        function calculateFee() {
            const income = parseFloat(document.getElementById('currentIncome').value) || 0;
            const mode = document.querySelector('input[name="empMode"]:checked').value;
            const service = document.getElementById('service').value;

            let fee = 0;

            if (mode === "Employee") {
                if (income >= 1000000 && income <= 2000000) fee = 45000;
                else if (income > 2000000 && income <= 3000000) fee = 60000;
                else if (income > 3000000 && income <= 4000000) fee = 75000;
                else if (income > 4000000 && income <= 5000000) fee = 90000;
                else if (income > 5000000) fee = 150000;
            } else { // Independent
                if (income >= 1000000 && income <= 2000000) fee = 10000;
                else if (income > 2000000 && income <= 3000000) fee = 20000;
                else if (income > 3000000 && income <= 4000000) fee = 30000;
                else if (income > 4000000 && income <= 5000000) fee = 40000;
                else if (income > 5000000) fee = 80000;
            }

            if (service === "Ingreso a parque") fee += 2500;
            else if (service === "Curso de formación") fee += 7500;
            else if (service === "Paquete de viaje") fee += 10000;
            else if (service === "Medicina preventiva") fee += (income * 0.10);

            document.getElementById('affiliationFee').value = `$${fee.toLocaleString('es-CO')}`;
            return fee;
        }

        document.getElementById('affiliationForm').addEventListener('submit', function(e) {
            e.preventDefault();
            const idNumber = document.getElementById('idNumber').value;
            const fullName = document.getElementById('fullName').value;

            if (!/^\d+$/.test(idNumber)) {
                alert("Error: ID Number must contain digits only.");
                return;
            }
            if (!/^[a-zA-Z\s]+$/.test(fullName)) {
                alert("Error: Full Name must contain letters only.");
                return;
            }

            const record = {
                idType: document.getElementById('idType').value,
                idNumber: idNumber,
                fullName: fullName,
                income: parseFloat(document.getElementById('currentIncome').value),
                mode: document.querySelector('input[name="empMode"]:checked').value,
                service: document.getElementById('service').value,
                fee: calculateFee(),
                date: document.getElementById('affiliationDate').value
            };

            const struct = document.getElementById('structChoice').value;
            if (struct === "Stack") stackData.push(record);
            else if (struct === "Queue") queueData.push(record);
            else listData.push(record);

            renderTable();
            clearForm();
            alert("Affiliate successfully registered!");
        });

        function renderTable() {
            const struct = document.getElementById('structChoice').value;
            document.getElementById('activeStructBadge').textContent = `Structure: ${struct}`;
            const tbody = document.getElementById('treeviewBody');
            tbody.innerHTML = '';

            let data = [];
            if (struct === "Stack") data = stackData;
            else if (struct === "Queue") data = queueData;
            else data = listData;

            if (data.length === 0) {
                tbody.innerHTML = `<tr><td colspan="8" class="text-center py-8 text-slate-500 italic">No records registered in this structure.</td></tr>`;
                return;
            }

            data.forEach(item => {
                const tr = document.createElement('tr');
                tr.className = "hover:bg-zinc-800/60";
                tr.innerHTML = `
                    <td class="py-2.5 px-3">${item.idType}</td>
                    <td class="py-2.5 px-3 font-semibold text-purple-400">${item.idNumber}</td>
                    <td class="py-2.5 px-3">${item.fullName}</td>
                    <td class="py-2.5 px-3">$${item.income.toLocaleString('es-CO')}</td>
                    <td class="py-2.5 px-3">${item.mode}</td>
                    <td class="py-2.5 px-3">${item.service}</td>
                    <td class="py-2.5 px-3 text-emerald-400 font-semibold">$${item.fee.toLocaleString('es-CO')}</td>
                    <td class="py-2.5 px-3 text-slate-400">${item.date}</td>
                `;
                tbody.appendChild(tr);
            });
        }

        function generateReport() {
            const struct = document.getElementById('structChoice').value;
            const display = document.getElementById('reportDisplay');

            if (struct === "Stack") {
                const totalFees = stackData.reduce((acc, curr) => acc + curr.fee, 0);
                display.value = `Stack Report: Sum of Fees = $${totalFees.toLocaleString('es-CO')}`;
            } else if (struct === "Queue") {
                display.value = `Queue Report: Total Records = ${queueData.length}`;
            } else {
                if (listData.length === 0) {
                    display.value = `List Report: Average Income = $0`;
                } else {
                    const avgIncome = listData.reduce((acc, curr) => acc + curr.income, 0) / listData.length;
                    display.value = `List Report: Average Income = $${avgIncome.toLocaleString('es-CO', {maximumFractionDigits: 2})}`;
                }
            }
        }

        function deleteRecord() {
            const struct = document.getElementById('structChoice').value;

            if (struct === "Stack") {
                if (stackData.length === 0) return alert("Stack is empty.");
                if (confirm("Are you sure you want to pop (unstack) the last registered affiliate?")) {
                    stackData.pop();
                    renderTable();
                }
            } else if (struct === "Queue") {
                if (queueData.length === 0) return alert("Queue is empty.");
                if (confirm("Are you sure you want to dequeue the first registered affiliate?")) {
                    queueData.shift();
                    renderTable();
                }
            } else {
                if (listData.length === 0) return alert("List is empty.");
                const searchId = prompt("Enter the ID Number of the affiliate to delete from List:");
                if (!searchId) return;

                const index = listData.findIndex(item => item.idNumber === searchId);
                if (index !== -1) {
                    if (confirm(`Affiliate ${listData[index].fullName} found. Confirm deletion?`)) {
                        listData.splice(index, 1);
                        renderTable();
                    }
                } else {
                    alert("Affiliate ID not found in List.");
                }
            }
        }
        function clearForm() {
            document.getElementById('idNumber').value = '';
            document.getElementById('fullName').value = '';
            document.getElementById('currentIncome').value = '';
            document.getElementById('affiliationFee').value = '$0';
            document.getElementById('reportDisplay').value = 'Select structure and click Report';
        }
