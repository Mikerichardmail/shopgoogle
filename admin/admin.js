document.addEventListener('DOMContentLoaded', () => {
    
    // UI Navigation Mock Logic
    const navItems = document.querySelectorAll('.sidebar li');
    const headerTitle = document.querySelector('header h1');
    
    navItems.forEach(item => {
        item.addEventListener('click', () => {
            navItems.forEach(n => n.classList.remove('active'));
            item.classList.add('active');
            headerTitle.innerText = item.childNodes[0].nodeValue.trim();
        });
    });

    // Mock Export CSV Call
    const btnExport = document.getElementById('btn-export');
    btnExport.addEventListener('click', () => {
        // Mocking CSV generating mechanism
        const csvContent = "data:text/csv;charset=utf-8,Domain,Code,Title,Score\najio.com,SAVE500,500 Off,82\namazon.in,HDFC10,10% Off,90\n";
        const encodedUri = encodeURI(csvContent);
        const link = document.createElement("a");
        link.setAttribute("href", encodedUri);
        link.setAttribute("download", "india_coupon_export.csv");
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    });

    // Mock Approval Action
    const approveBtns = document.querySelectorAll('.btn-success');
    approveBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const row = e.target.closest('tr');
            row.style.opacity = '0.5';
            setTimeout(() => {
                row.remove();
                alert("Coupon approved and moved to active database.");
            }, 300);
        });
    });

});
