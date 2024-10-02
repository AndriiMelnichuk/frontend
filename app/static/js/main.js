function toggleSidebar() {
    var sidebar = document.getElementById("sidebar");
    var content = document.getElementById("content");

    sidebar.classList.toggle("expanded");

    // Сдвигаем контент вправо, если сайдбар открыт
    if (sidebar.classList.contains("expanded")) {
        content.style.marginLeft = "250px";
    } else {
        content.style.marginLeft = "60px"; // Возвращаем в исходное положение
    }
}