
let sidebarOpen = false;
const sidebar = document.getElementById('sidebar');

function timedPopup(type, message, goto, session_id) {
    let timerInterval;
    Swal.fire({
        title: message,
        icon: type,
        timer: 1500,
        timerProgressBar: true,
        didOpen: () => {
            Swal.showLoading();
        },
        willClose: () => {
            clearInterval(timerInterval);
            document.cookie = `session_id=${session_id};`;
            window.location.href = `/${goto}`;
        }
    }).then((result) => {
        if (result.dismiss === Swal.DismissReason.timer) {
        }
    });
}

function gotoLogin(session_id) {
    document.cookie = `session_id=${session_id};`;
    window.location.href = "/logout"
}

function openSidebar() {
    if (!sidebarOpen) {
        sidebar.classList.add('sidebar-responsive');
        sidebarOpen = true;
    }
}

function closeSidebar() {
    if (sidebarOpen) {
        sidebar.classList.remove('sidebar-responsive');
        sidebarOpen = false;
    }
}

function gotoUsers(session_id) {
    console.log(session_id)
    document.cookie = `session_id=${session_id};`;
    window.location.href = "/users";
}

function editUser(user_id, session_id) {
    console.log(user_id);
    var dtl = { id: user_id }
    fetch(`/edit_user?id=${user_id}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Cookie': 'session_id' + `${session_id}`
        }
    })
    document.cookie = `session_id=${session_id};`;
    window.location.href = `/edit_user?id=${user_id}`;

}

function updateUser(event, session_id, user_id) {
    event.preventDefault(); // Prevents the default form submission behavior

    var formData = {
        id: user_id,
        username: document.getElementById('username').value,
        password: document.getElementById('password').value,
        role: document.getElementById('role').value
    };
    console.log(formData);
    Swal.fire({
        title: "Are you sure?",
        text: "You won't be able to revert this!",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Yes, update it!"
    }).then((result) => {
        if (result.isConfirmed) {

            fetch('/update_user', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Cookie': 'session_id' + `${session_id}`,
                },
                body: JSON.stringify(formData),

            }).then(response => response.json())  // This returns a promise
                .then(data => {
                    timedPopup("success", data.message, 'users', session_id);
                })
                .catch(error => {
                    console.error('Error:', error);
                });

        }
    });
}

function gotoDashboard(session_id) {
    console.log(session_id)
    document.cookie = `session_id=${session_id};`;
    window.location.href = "/dashboard";
}

function sendMessage(message) {
    if (message !== "login") {
        alert(message);
    }
}

function gotoAddUser(session_id) {
    console.log("adding user")
    document.cookie = `session_id=${session_id};`;
    window.location.href = "/add_user";
}

function signUp(event, session_id) {
    event.preventDefault(); // Prevents the default form submission behavior

    var formData = {
        username: document.getElementById('username').value,
        password: document.getElementById('password').value,
        role: document.getElementById('role').value
    };
    console.log(formData)

    fetch('/signup', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Cookie': 'session_id' + `${session_id}`,
        },
        body: JSON.stringify(formData),

    }).then(response => response.json())  // This returns a promise
        .then(data => {
            console.log(data);
            if (data.success) {
                timedPopup("success", data.message, 'users', session_id);

            } else {
                timedPopup("warning", data.message, 'users', session_id);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });

}

function getMe(session_id) {
    alert(session_id);
}

function deleteUser(user_id, session_id) {
    var formData = {
        id: user_id
    };
    console.log(formData)

    Swal.fire({
        title: "Are you sure?",
        text: "You won't be able to revert this!",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Yes, delete it!"
    }).then((result) => {
        if (result.isConfirmed) {

            fetch('/delete_user', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Cookie': 'session_id' + `${session_id}`,
                },
                body: JSON.stringify(formData),

            }).then(response => response.json())  // This returns a promise
                .then(data => {
                    timedPopup("success", data.message, 'users', session_id);
                })
                .catch(error => {
                    console.error('Error:', error);
                });

        }
    });

}
// ---------- CHARTS ----------

// BAR CHART
const barChartOptions = {
    series: [
        {
            data: [10, 8, 6, 4, 2],
        },
    ],
    chart: {
        type: 'bar',
        height: 350,
        toolbar: {
            show: false,
        },
    },
    colors: ['#246dec', '#cc3c43', '#367952', '#f5b74f', '#4f35a1'],
    plotOptions: {
        bar: {
            distributed: true,
            borderRadius: 4,
            horizontal: false,
            columnWidth: '40%',
        },
    },
    dataLabels: {
        enabled: false,
    },
    legend: {
        show: false,
    },
    xaxis: {
        categories: ['Laptop', 'Phone', 'Monitor', 'Headphones', 'Camera'],
    },
    yaxis: {
        title: {
            text: 'Count',
        },
    },
};

const barChart = new ApexCharts(
    document.querySelector('#bar-chart'),
    barChartOptions
);
barChart.render();

// AREA CHART
const areaChartOptions = {
    series: [
        {
            name: 'Purchase Orders',
            data: [31, 40, 28, 51, 42, 109, 100],
        },
        {
            name: 'Sales Orders',
            data: [11, 32, 45, 32, 34, 52, 41],
        },
    ],
    chart: {
        height: 350,
        type: 'area',
        toolbar: {
            show: false,
        },
    },
    colors: ['#4f35a1', '#246dec'],
    dataLabels: {
        enabled: false,
    },
    stroke: {
        curve: 'smooth',
    },
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
    markers: {
        size: 0,
    },
    yaxis: [
        {
            title: {
                text: 'Purchase Orders',
            },
        },
        {
            opposite: true,
            title: {
                text: 'Sales Orders',
            },
        },
    ],
    tooltip: {
        shared: true,
        intersect: false,
    },
};

const areaChart = new ApexCharts(
    document.querySelector('#area-chart'),
    areaChartOptions
);
areaChart.render();
