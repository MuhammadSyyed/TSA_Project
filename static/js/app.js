
let sidebarOpen = false;
const sidebar = document.getElementById('sidebar');
function togglestudentform() {

    if (document.getElementById('uploadStudentsheet').hidden) {

        document.getElementById('studentForm').hidden = true;
        document.getElementById('uploadStudentsheet').hidden = false;
        document.getElementById('toggleFormbutton').innerText = "+ Add One Student";
    } else {
        document.getElementById('studentForm').hidden = false;
        document.getElementById('uploadStudentsheet').hidden = true;
        document.getElementById('toggleFormbutton').innerText = "+ Import Excel File";
    }

}

function showUploadedImage(event) {
    var input = event.target;
    var preview = document.getElementById('previewImage');
    var reader = new FileReader();

    reader.onload = function () {
        preview.style.backgroundImage = 'url(' + reader.result + ')';
    };

    if (input.files && input.files[0]) {
        reader.readAsDataURL(input.files[0]);
    }

    document.getElementById('previewImage').hidden = false;
    document.getElementById('cross').hidden = false;
    document.getElementById('avatar').hidden = true;
}

function resetImage() {
    document.getElementById('image').value = '';
    document.getElementById('previewImage').hidden = true;
    document.getElementById('avatar').hidden = false;
    document.getElementById('cross').hidden = true;

}

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

function gotoSubjects(session_id) {
    console.log(session_id)
    document.cookie = `session_id=${session_id};`;
    window.location.href = "/subjects";
}

function gotoResults(session_id) {
    console.log(session_id)
    document.cookie = `session_id=${session_id};`;
    window.location.href = "/results";
}

function gotoExaminationBoard(session_id) {
    console.log(session_id)
    document.cookie = `session_id=${session_id};`;
    window.location.href = "/examination_board";
}

function editUser(user_id, session_id) {
    console.log(user_id);

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

    document.cookie = `session_id=${session_id};`;
    window.location.href = "/add_user";
}

function gotoAddSubject(session_id) {
    document.cookie = `session_id=${session_id};`;
    window.location.href = "/form_subject";
}

function gotoAddCampus(session_id) {

    document.cookie = `session_id=${session_id};`;
    window.location.href = "/form_campus";
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

function addSubject(event, session_id) {
    event.preventDefault(); // Prevents the default form submission behavior

    var formData = {
        subject_name: document.getElementById('subject').value,
        total_lecture_units: document.getElementById('lecture_units').value
    };
    console.log(formData)

    fetch('/add_subject', {
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
                timedPopup("success", data.message, 'subjects', session_id);

            } else {
                timedPopup("warning", data.message, 'subjects', session_id);
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

function gotoAddMarks(session_id) {
    console.log(session_id)
    document.cookie = `session_id=${session_id};`;
    window.location.href = "/add_marks";
}

function gotoStudents(session_id) {
    console.log(session_id)
    document.cookie = `session_id=${session_id};`;
    window.location.href = "/students";

}

function gotoCampuses(session_id) {
    console.log(session_id)
    document.cookie = `session_id=${session_id};`;
    window.location.href = "/campuses";

}

function addCampus(event, session_id) {

    event.preventDefault(); // Prevents the default form submission behavior

    var formData = {
        campus_name: document.getElementById('campus_name').value,
        address: document.getElementById('address').value,
        incharge: document.getElementById('incharge').value,
        admin: document.getElementById('admin').value,
        coo: document.getElementById('coo').value,
        head_eb: document.getElementById('head_eb').value,
        contact_number: document.getElementById('contact').value,
    };
    console.log(formData)

    fetch('/add_campus', {
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
                timedPopup("success", data.message, 'campuses', session_id);

            } else {
                timedPopup("warning", data.message, 'campuses', session_id);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });

}

function deleteCampus(campus_id, session_id) {
    var formData = {
        campus_id: campus_id
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

            fetch('/delete_campus', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Cookie': 'session_id' + `${session_id}`,
                },
                body: JSON.stringify(formData),

            }).then(response => response.json())  // This returns a promise
                .then(data => {
                    timedPopup("success", data.message, 'campuses', session_id);
                })
                .catch(error => {
                    console.error('Error:', error);
                });

        }
    });

}

function editCampus(campus_id, session_id) {

    fetch(`/edit_campus?campus_id=${campus_id}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Cookie': 'session_id' + `${session_id}`
        }
    })
    document.cookie = `session_id=${session_id};`;
    window.location.href = `/edit_campus?campus_id=${campus_id}`;

}

function updateCampus(event, session_id, campus_id) {

    event.preventDefault();

    var formData = {
        campus_id: campus_id,
        campus_name: document.getElementById('campus_name').value,
        address: document.getElementById('address').value,
        incharge: document.getElementById('incharge').value,
        admin: document.getElementById('admin').value,
        coo: document.getElementById('coo').value,
        head_eb: document.getElementById('head_eb').value,
        contact_number: document.getElementById('contact').value,
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

            fetch('/update_campus', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Cookie': 'session_id' + `${session_id}`,
                },
                body: JSON.stringify(formData),

            }).then(response => response.json())  // This returns a promise
                .then(data => {
                    timedPopup("success", data.message, 'campuses', session_id);
                })
                .catch(error => {
                    console.error('Error:', error);
                });

        }
    });

}

function gotoEditSubject(subject_id, session_id) {
    console.log(session_id, subject_id);
    fetch(`/edit_subject?subject_id=${subject_id}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Cookie': 'session_id' + `${session_id}`
        }
    })
    document.cookie = `session_id=${session_id};`;
    window.location.href = `/edit_subject?subject_id=${subject_id}`;

}

function updateSubject(event, session_id, subject_id) {

    event.preventDefault();

    var formData = {
        subject_id: subject_id,
        subject_name: document.getElementById('subject').value,
        total_lecture_units: document.getElementById('lecture_units').value
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

            fetch('/update_subject', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Cookie': 'session_id' + `${session_id}`,
                },
                body: JSON.stringify(formData),

            }).then(response => response.json())  // This returns a promise
                .then(data => {
                    timedPopup("success", data.message, 'subjects', session_id);
                })
                .catch(error => {
                    console.error('Error:', error);
                });

        }
    });

}

function gotoAdmissions(session_id) {
    console.log(session_id)
    document.cookie = `session_id=${session_id};`;
    window.location.href = "/admissions";
}

function gotoAddStudent(session_id) {
    console.log(session_id)
    document.cookie = `session_id=${session_id};`;
    window.location.href = "/form_student";
}

function addStudent(event, session_id) {
    event.preventDefault();

    var formData = {
        student_name: document.getElementById('student_name').value,
        campus_id: document.getElementById('campus_id').value,
        roll_no: document.getElementById('roll_no').value,
        batch: document.getElementById('batch').value,
        date_joined: document.getElementById('date_joined').value,
        parent_name: document.getElementById('parent_name').value,
        parent_contact: document.getElementById('parent_contact').value,
        group: document.getElementById('group').value,
        last_class_percentage: document.getElementById('percentage').value,
        reference: document.getElementById('reference').value
    };

    console.log(formData);


    fetch('/add_student', {
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
                timedPopup("success", data.message, 'students', session_id);

            } else {
                timedPopup("warning", data.message, 'students', session_id);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function uploadStudentsFile(session_id) {

    var fileInput = document.getElementById('fileInput');
    if (fileInput.files.length > 0) {
        var formData = new FormData();
        formData.append('xlsxfile', fileInput.files[0]);
        fetch('/add_students_via_sheet', {
            method: 'POST',
            body: formData,
            headers: {
                'Cookie': 'session_id' + `${session_id}`,
            },
        })
            .then(response => response.json())
            .then(data => {
                alert(data.message);

            })
            .catch(error => {
                console.error('Error:', error);

            });


    }
    else {
        alert('Please select a file.');
    }
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
            show: true,
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
