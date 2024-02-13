
let sidebarOpen = false;
const sidebar = document.getElementById('sidebar');


function toggleForm(element_id, form_element_id, sheet_element_id) {

    if (document.getElementById(sheet_element_id).hidden) {

        document.getElementById(form_element_id).hidden = true;
        document.getElementById(sheet_element_id).hidden = false;
        document.getElementById(element_id).innerText = "+ Add One";
    } else {
        document.getElementById(form_element_id).hidden = false;
        document.getElementById(sheet_element_id).hidden = true;
        document.getElementById(element_id).innerText = "+ Import Excel File";
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
    document.cookie = `session_id=${session_id};`;
    window.location.href = "/users";
}

function gotoSubjects(session_id) {

    document.cookie = `session_id=${session_id};`;
    window.location.href = "/subjects";
}

function gotoResults(session_id) {

    document.cookie = `session_id=${session_id};`;
    window.location.href = "/results";
}

function gotoExaminationBoard(session_id) {

    document.cookie = `session_id=${session_id};`;
    window.location.href = "/examination_board";
}

function editUser(user_id, session_id) {


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


    fetch('/signup', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Cookie': 'session_id' + `${session_id}`,
        },
        body: JSON.stringify(formData),

    }).then(response => response.json())  // This returns a promise
        .then(data => {
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

function gotoSubjectDetails(session_id, subject_id) {
    document.cookie = `session_id=${session_id};`;
    window.location.href = `/subject_details?subject_id=${subject_id}`;
}

function gotoMonthlySubjectResult(session_id, subject_id) {
    document.cookie = `session_id=${session_id};`;
    window.location.href = `/monthly_subject_result?subject_id=${subject_id}`;
    console.log("Aalelola")
}

function addSubject(event, session_id) {
    event.preventDefault(); // Prevents the default form submission behavior

    var formData = {
        subject_name: document.getElementById('subject').value,
        total_lecture_units: document.getElementById('lecture_units').value
    };


    fetch('/add_subject', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Cookie': 'session_id' + `${session_id}`,
        },
        body: JSON.stringify(formData),

    }).then(response => response.json())  // This returns a promise
        .then(data => {

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
    Swal.fire(session_id);
}

function deleteUser(user_id, session_id) {
    var formData = {
        id: user_id
    };


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

    document.cookie = `session_id=${session_id};`;
    window.location.href = "/form_marks";
}

function gotoStudents(session_id) {

    document.cookie = `session_id=${session_id};`;
    window.location.href = "/students";

}

function gotoCampuses(session_id) {

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


    fetch('/add_campus', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Cookie': 'session_id' + `${session_id}`,
        },
        body: JSON.stringify(formData),

    }).then(response => response.json())  // This returns a promise
        .then(data => {
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

    document.cookie = `session_id=${session_id};`;
    window.location.href = "/admissions";
}

function gotoAddStudent(session_id) {

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




    fetch('/add_student', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Cookie': 'session_id' + `${session_id}`,
        },
        body: JSON.stringify(formData),

    }).then(response => response.json())  // This returns a promise

        .then(data => {

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

function uploadStudentsFile(event, session_id) {
    event.preventDefault();
    Swal.fire({
        title: "Are you sure?",
        text: "You won't be able to revert this!",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Yes, Upload it!"
    }).then((result) => {
        if (result.isConfirmed) {
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
                        timedPopup('success', data.message, 'students', session_id)

                    })
                    .catch(error => {
                        timedPopup('warning', error, 'form_student', session_id)

                    });
            }
            else {
                timedPopup('warning', 'Please Choose Xlsx File', 'form_student', session_id)
            }

        }
    });



}

function uploadMarksFile(event, session_id) {
    event.preventDefault();
    Swal.fire({
        title: "Are you sure?",
        text: "You won't be able to revert this!",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Yes, Upload it!"
    }).then((result) => {
        if (result.isConfirmed) {

            var fileInput = document.getElementById('fileInput');
            if (fileInput.files.length > 0) {
                var formData = new FormData();
                formData.append('xlsxfile', fileInput.files[0]);
                fetch('/add_marks_via_sheet', {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'Cookie': 'session_id' + `${session_id}`,
                    },
                })
                    .then(response => response.json())
                    .then(data => {
                        timedPopup('success', data.message, 'examination_board', session_id)
                    })
                    .catch(error => {
                        timedPopup('warning', data.message, 'form_marks', session_id)

                    });
            }
            else {
                timedPopup('warning', 'Please Select An Excel File', 'form_marks', session_id)
            }

        }
    });


}

function addMarks(event, session_id) {
    event.preventDefault();

    var formData = {
        student_id: document.getElementById('student_id').value,
        subject_id: document.getElementById('subject_id').value,
        month: document.getElementById('year').value + document.getElementById('month').value,
        marks_total: document.getElementById('marks_total').value,
        marks_obtained: document.getElementById('marks_obtained').value
    };




    fetch('/add_marks', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Cookie': 'session_id' + `${session_id}`,
        },
        body: JSON.stringify(formData),

    }).then(response => response.json())  // This returns a promise

        .then(data => {

            if (data.success) {
                timedPopup("success", data.message, 'examination_board', session_id);

            } else {
                timedPopup("warning", data.message, 'examination_board', session_id);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

// ---------- CHARTS ----------


const studentMarks = [
    { name: 'Alice', marks: 85 },
    { name: 'Bob', marks: 78 },
    { name: 'Charlie', marks: 92 },
    { name: 'David', marks: 65 },
    { name: 'Emma', marks: 89 },
    { name: 'Frank', marks: 72 },
    { name: 'Grace', marks: 94 },
    { name: 'Henry', marks: 60 },
    { name: 'Ivy', marks: 87 },
    { name: 'Jack', marks: 76 },
    { name: 'Karen', marks: 91 },
    { name: 'Liam', marks: 82 },
    { name: 'Mia', marks: 79 },
    { name: 'Noah', marks: 88 },
    { name: 'Olivia', marks: 70 },
    { name: 'Parker', marks: 93 },
    { name: 'Quinn', marks: 68 },
    { name: 'Ryan', marks: 83 },
    { name: 'Sophia', marks: 75 },
    { name: 'Thomas', marks: 97 },
    { name: 'Uma', marks: 69 },
    { name: 'Vincent', marks: 80 },
    { name: 'Willow', marks: 84 },
    { name: 'Xavier', marks: 73 },
    { name: 'Yara', marks: 96 },
    { name: 'Zane', marks: 71 },
    { name: 'Eva', marks: 74 },
    { name: 'Logan', marks: 98 },
    { name: 'Ava', marks: 81 },
    { name: 'Owen', marks: 77 },
];

var students = studentMarks.map(student => student.name);

const marks = studentMarks.map(student => student.marks);

const grade_colors = studentMarks.map(student => {
    const marks = student.marks;
    if (marks >= 91) {
        return '#4CAF50'; // Green for 91-100
    } else if (marks >= 81) {
        return '#2196F3'; // Blue for 81-90
    } else if (marks >= 71) {
        return '#FFC107'; // Amber for 71-80
    } else if (marks >= 61) {
        return '#FF5722'; // Deep Orange for 61-70
    } else {
        return '#F44336'; // Red for 51-60 and below
    }
});

const barChartOptions = {
    series: [
        {
            name: 'Percentage',
            data: marks,
        },
    ],
    chart: {
        type: 'bar',
        height: 420,
        toolbar: {
            show: true,
        },
    },
    colors: grade_colors,
    plotOptions: {
        bar: {
            distributed: true,
            borderRadius: 5,
            horizontal: false,
            columnWidth: '60%',
            dataLabels: {
                position: 'top', // top, center, bottom
            },
        },
    },
    dataLabels: {
        enabled: true,
        formatter: function (value) {
            return value + "%";
        },
        offsetY: -20,
        style: {
            fontSize: '12px',
            colors: ["#304758"]
        }
    },
    legend: {
        show: false,
    },
    xaxis: {
        categories: students,
    },
    yaxis: {
        title: {
            text: 'Marks(%)',
        },
    }
};

const barChart = new ApexCharts(
    document.querySelector('#bar-chart'),
    barChartOptions
);
barChart.render();

function categorizeMarks(marks) {
    if (marks >= 90) return '90+';
    if (marks >= 80) return '80-89';
    if (marks >= 70) return '70-79';
    if (marks >= 60) return '60-69';
    return '50-59';
}

const marksCount = {
    '90+': 0,
    '80-89': 0,
    '70-79': 0,
    '60-69': 0,
    '50-59': 0,
};

studentMarks.forEach((student) => {
    const category = categorizeMarks(student.marks);
    marksCount[category]++;
});

// Pie Chart

const seriesData = Object.values(marksCount);
var pie_options = {
    series: seriesData,
    chart: {
        type: 'donut',
    },
    labels: Object.keys(marksCount),
    responsive: [
        {
            breakpoint: 480,
            options: {
                chart: {
                    width: 200,
                },
                legend: {
                    position: 'bottom',
                },
            },
        },
    ],
};
var chart = new ApexCharts(document.querySelector("#pie-chart"), pie_options);
chart.render();

const words = [
    { key: "word", value: 45 },
    { key: "words", value: 81 },
    { key: "sprite", value: 70 },
    { key: "placed", value: 51 },
    { key: "layout", value: 49 }
];

const radar = new Chart(document.getElementById("canvas").getContext("2d"), {
    type: "radar",
    data: {
        labels: words.map((d) => d.key),
        datasets: [
            {
                label: "",
                data: words.map((d) => d.value)
            }
        ]
    },
    options: {
        title: {
            display: false,
            text: "Chart.js Word Cloud"
        },
        plugins: {
            legend: {
                display: false
            }
        }
    }
});

// -----------------------------------------------------------------------------
am4core.useTheme(am4themes_moonrisekingdom);
am4core.useTheme(am4themes_animated);

var chart = am4core.create("chartdiv", am4plugins_wordCloud.WordCloud);
chart.fontFamily = "Courier New";
var series = chart.series.push(new am4plugins_wordCloud.WordCloudSeries());
series.randomness = 0.2;
series.rotationThreshold = 0;

series.data = [{
    "tag": "Physics I",
    "count": "7"
}, {
    "tag": "Chemistry I",
    "count": "5"
}, {
    "tag": "Urdu I",
    "count": "6"
}, {
    "tag": "English I",
    "count": "6"
}, {
    "tag": "Islamiat",
    "count": "4"
}, {
    "tag": "Maths/Bio I",
    "count": "7"
}];

series.dataFields.word = "tag";
series.dataFields.value = "count";

series.heatRules.push({
    "target": series.labels.template,
    "property": "fill",
    "min": am4core.color("#0000CC"),
    "max": am4core.color("#CC00CC"),
    "dataField": "value"
});

series.labels.template.url = "http://localhost:8000/subjects";
series.labels.template.urlTarget = "_blank";
series.labels.template.tooltipText = "{word}: {value}";

var hoverState = series.labels.template.states.create("hover");
hoverState.properties.fill = am4core.color("orange");

var subtitle = chart.titles.create();

var title = chart.titles.create();
// title.text = "Most Popular Tags @ StackOverflow";
title.fontSize = 1700;
title.fontWeight = "1000000";



// ----------------------------------------------- Heatmap ------------------------
// Example data for 5 subjects
const subjectsData = [{
    subject: 'Physics I',
    marks:
        [
            { name: 'Alice', marks: 79 },
            { name: 'Bob', marks: 92 },
            { name: 'Charlie', marks: 68 },
            { name: 'David', marks: 87 },
            { name: 'Emma', marks: 74 },
            { name: 'Frank', marks: 95 },
            { name: 'Grace', marks: 81 },
            { name: 'Henry', marks: 70 },
            { name: 'Ivy', marks: 83 },
            { name: 'Jack', marks: 89 },
            { name: 'Karen', marks: 72 },
            { name: 'Liam', marks: 66 },
            { name: 'Mia', marks: 78 },
            { name: 'Noah', marks: 91 },
            { name: 'Olivia', marks: 84 },
            { name: 'Parker', marks: 76 },
            { name: 'Quinn', marks: 93 },
            { name: 'Ryan', marks: 85 },
            { name: 'Sophia', marks: 97 },
            { name: 'Thomas', marks: 88 },
            { name: 'Uma', marks: 73 },
            { name: 'Vincent', marks: 67 },
            { name: 'Willow', marks: 80 },
            { name: 'Xavier', marks: 94 },
            { name: 'Yara', marks: 82 },
            { name: 'Zane', marks: 71 },
            { name: 'Eva', marks: 76 },
            { name: 'Logan', marks: 98 },
            { name: 'Ava', marks: 75 },
            { name: 'Owen', marks: 79 },
        ]
}, {
    subject: 'Urdu I',
    marks: [
        { name: 'Alice', marks: 88 },
        { name: 'Bob', marks: 72 },
        { name: 'Charlie', marks: 95 },
        { name: 'David', marks: 69 },
        { name: 'Emma', marks: 84 },
        { name: 'Frank', marks: 78 },
        { name: 'Grace', marks: 90 },
        { name: 'Henry', marks: 77 },
        { name: 'Ivy', marks: 89 },
        { name: 'Jack', marks: 83 },
        { name: 'Karen', marks: 71 },
        { name: 'Liam', marks: 92 },
        { name: 'Mia', marks: 68 },
        { name: 'Noah', marks: 86 },
        { name: 'Olivia', marks: 79 },
        { name: 'Parker', marks: 94 },
        { name: 'Quinn', marks: 75 },
        { name: 'Ryan', marks: 81 },
        { name: 'Sophia', marks: 73 },
        { name: 'Thomas', marks: 97 },
        { name: 'Uma', marks: 82 },
        { name: 'Vincent', marks: 74 },
        { name: 'Willow', marks: 87 },
        { name: 'Xavier', marks: 76 },
        { name: 'Yara', marks: 70 },
        { name: 'Zane', marks: 91 },
        { name: 'Eva', marks: 85 },
        { name: 'Logan', marks: 98 },
        { name: 'Ava', marks: 80 },
        { name: 'Owen', marks: 93 },
    ]
},
{
    subject: 'Chemistry I',
    marks:
        [
            { name: 'Alice', marks: 79 },
            { name: 'Bob', marks: 92 },
            { name: 'Charlie', marks: 68 },
            { name: 'David', marks: 87 },
            { name: 'Emma', marks: 74 },
            { name: 'Frank', marks: 95 },
            { name: 'Grace', marks: 81 },
            { name: 'Henry', marks: 70 },
            { name: 'Ivy', marks: 83 },
            { name: 'Jack', marks: 89 },
            { name: 'Karen', marks: 72 },
            { name: 'Liam', marks: 66 },
            { name: 'Mia', marks: 78 },
            { name: 'Noah', marks: 91 },
            { name: 'Olivia', marks: 84 },
            { name: 'Parker', marks: 76 },
            { name: 'Quinn', marks: 93 },
            { name: 'Ryan', marks: 85 },
            { name: 'Sophia', marks: 97 },
            { name: 'Thomas', marks: 88 },
            { name: 'Uma', marks: 73 },
            { name: 'Vincent', marks: 67 },
            { name: 'Willow', marks: 80 },
            { name: 'Xavier', marks: 94 },
            { name: 'Yara', marks: 82 },
            { name: 'Zane', marks: 71 },
            { name: 'Eva', marks: 76 },
            { name: 'Logan', marks: 98 },
            { name: 'Ava', marks: 75 },
            { name: 'Owen', marks: 79 },
        ]
}
    , {
    subject: 'Maths/Bio I',
    marks:
        [
            { name: 'Alice', marks: 72 },
            { name: 'Bob', marks: 96 },
            { name: 'Charlie', marks: 79 },
            { name: 'David', marks: 68 },
            { name: 'Emma', marks: 85 },
            { name: 'Frank', marks: 90 },
            { name: 'Grace', marks: 73 },
            { name: 'Henry', marks: 88 },
            { name: 'Ivy', marks: 76 },
            { name: 'Jack', marks: 82 },
            { name: 'Karen', marks: 94 },
            { name: 'Liam', marks: 71 },
            { name: 'Mia', marks: 89 },
            { name: 'Noah', marks: 83 },
            { name: 'Olivia', marks: 65 },
            { name: 'Parker', marks: 78 },
            { name: 'Quinn', marks: 91 },
            { name: 'Ryan', marks: 74 },
            { name: 'Sophia', marks: 97 },
            { name: 'Thomas', marks: 80 },
            { name: 'Uma', marks: 69 },
            { name: 'Vincent', marks: 84 },
            { name: 'Willow', marks: 77 },
            { name: 'Xavier', marks: 93 },
            { name: 'Yara', marks: 70 },
            { name: 'Zane', marks: 75 },
            { name: 'Eva', marks: 86 },
            { name: 'Logan', marks: 98 },
            { name: 'Ava', marks: 81 },
            { name: 'Owen', marks: 92 },
        ]
}
    , {
    subject: 'English I',
    marks:
        [
            { name: 'Alice', marks: 84 },
            { name: 'Bob', marks: 77 },
            { name: 'Charlie', marks: 92 },
            { name: 'David', marks: 65 },
            { name: 'Emma', marks: 89 },
            { name: 'Frank', marks: 72 },
            { name: 'Grace', marks: 94 },
            { name: 'Henry', marks: 60 },
            { name: 'Ivy', marks: 87 },
            { name: 'Jack', marks: 76 },
            { name: 'Karen', marks: 91 },
            { name: 'Liam', marks: 82 },
            { name: 'Mia', marks: 79 },
            { name: 'Noah', marks: 88 },
            { name: 'Olivia', marks: 70 },
            { name: 'Parker', marks: 93 },
            { name: 'Quinn', marks: 68 },
            { name: 'Ryan', marks: 83 },
            { name: 'Sophia', marks: 75 },
            { name: 'Thomas', marks: 97 },
            { name: 'Uma', marks: 69 },
            { name: 'Vincent', marks: 80 },
            { name: 'Willow', marks: 84 },
            { name: 'Xavier', marks: 73 },
            { name: 'Yara', marks: 96 },
            { name: 'Zane', marks: 71 },
            { name: 'Eva', marks: 74 },
            { name: 'Logan', marks: 98 },
            { name: 'Ava', marks: 81 },
            { name: 'Owen', marks: 77 },
        ]
}, {
    subject: 'Islamiat',
    marks:
        [
            { name: 'Alice', marks: 84 },
            { name: 'Bob', marks: 77 },
            { name: 'Charlie', marks: 92 },
            { name: 'David', marks: 65 },
            { name: 'Emma', marks: 89 },
            { name: 'Frank', marks: 72 },
            { name: 'Grace', marks: 94 },
            { name: 'Henry', marks: 60 },
            { name: 'Ivy', marks: 87 },
            { name: 'Jack', marks: 76 },
            { name: 'Karen', marks: 91 },
            { name: 'Liam', marks: 82 },
            { name: 'Mia', marks: 79 },
            { name: 'Noah', marks: 88 },
            { name: 'Olivia', marks: 70 },
            { name: 'Parker', marks: 93 },
            { name: 'Quinn', marks: 68 },
            { name: 'Ryan', marks: 83 },
            { name: 'Sophia', marks: 75 },
            { name: 'Thomas', marks: 97 },
            { name: 'Uma', marks: 69 },
            { name: 'Vincent', marks: 80 },
            { name: 'Willow', marks: 84 },
            { name: 'Xavier', marks: 73 },
            { name: 'Yara', marks: 96 },
            { name: 'Zane', marks: 71 },
            { name: 'Eva', marks: 74 },
            { name: 'Logan', marks: 98 },
            { name: 'Ava', marks: 81 },
            { name: 'Owen', marks: 77 },
        ]
}
];

function generateData(numPoints, options, decimalPlaces = 0) {
    const { min, max } = options;
    const data = [];

    for (let i = 0; i < numPoints; i++) {
        const randomValue = Math.random() * (max - min) + min;
        const roundedValue = Number(randomValue.toFixed(decimalPlaces));
        data.push(roundedValue);
    }

    return data;
}

var heatmapOptions = {
    series: subjectsData.map(subject => ({
        name: subject.subject,
        data: subject.marks.map(student => ({
            x: student.name,
            y: student.marks,
        }))
    }))
    ,
    chart: {
        height: 400,
        type: 'heatmap',
    },
    stroke: {
        width: 1
    },
    plotOptions: {
        heatmap: {
            radius: 25,
            enableShades: false,
            colorScale: {
                ranges: [{
                    from: 0,
                    to: 50,
                    color: 'red'
                },
                {
                    from: 51,
                    to: 60,
                    color: 'blue'
                },
                {
                    from: 61,
                    to: 70,
                    color: 'orange'
                },
                {
                    from: 71,
                    to: 80,
                    color: 'purple'

                }, {
                    from: 81,
                    to: 90,
                    color: 'green'

                }, {
                    from: 91,
                    to: 100,
                    color: 'brown'

                }
                ],
            },

        }
    },
    dataLabels: {
        enabled: true,
        style: {
            colors: ['#fff']
        }
    },
    xaxis: {
        type: 'integer',
    },
    title: {
        text: 'Rounded (Range without Shades)'
    },
};

var heatmap = new ApexCharts(document.querySelector("#heatmap"), heatmapOptions);
heatmap.render();

// ------------------------------------------ Stacked Bar Chart ------------

var options = {
    series: subjectsData.map(subject => ({
        name: subject.subject,
        data: subject.marks.map(student => ({
            x: student.name,
            y: student.marks,
        }))
    })),
    chart: {
        type: 'bar',
        height: 350,
        stacked: true,
        toolbar: {
            show: true
        },
        zoom: {
            enabled: true
        }
    },
    responsive: [{
        breakpoint: 480,
        options: {
            legend: {
                position: 'bottom',
                offsetX: -10,
                offsetY: 0
            }
        }
    }],
    plotOptions: {
        bar: {
            horizontal: false,
            borderRadius: 10,
            dataLabels: {
                total: {
                    enabled: true,
                    style: {
                        fontSize: '13px',
                        fontWeight: 900
                    }
                }
            }
        },
    },
    xaxis: {
        type: 'text'
    },
    legend: {
        position: 'right',
        offsetY: 40
    },
    fill: {
        opacity: 1
    }
};

var stackedbar = new ApexCharts(document.querySelector("#stackedbar"), options);
stackedbar.render();